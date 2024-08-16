import re
from typing import Literal, overload

import torch
import torch.nn as nn
from jaxtyping import Float, Int
from torch import Tensor
from transformer_lens import HookedTransformer, utils
from transformer_lens.hook_points import HookPoint

DTYPES = {
    "float32": torch.float32,
    "float16": torch.float16,
    "bfloat16": torch.bfloat16,
}


# # ==============================================================
# # ! TRANSFORMERS
# # This returns the activations & resid_pre as well (optionally)
# # ==============================================================


class TransformerLensWrapper(nn.Module):
    """
    This class wraps around & extends the TransformerLens model, so that we can make sure things like the forward
    function have a standardized signature.
    """

    def __init__(self, model: HookedTransformer, hook_point: str):
        super().__init__()
        assert (
            hook_point in model.hook_dict
        ), f"Error: hook_point={hook_point!r} must be in model.hook_dict"
        self.model = model
        self.hook_point = hook_point

        # Get the layer (so we can do the early stopping in our forward pass)
        layer_match = re.match(r"blocks\.(\d+)\.", hook_point)
        assert (
            layer_match
        ), f"Error: expecting hook_point to be 'blocks.{{layer}}.{{...}}', but got {hook_point!r}"
        self.hook_layer = int(layer_match.group(1))

        # Get the hook names for the residual stream (final) and residual stream (immediately after hook_point)
        self.hook_point_resid = utils.get_act_name("resid_post", self.hook_layer)
        self.hook_point_resid_final = utils.get_act_name(
            "resid_post", self.model.cfg.n_layers - 1
        )
        assert self.hook_point_resid in model.hook_dict
        assert self.hook_point_resid_final in model.hook_dict

    @overload
    def forward(
        self,
        tokens: Tensor,
        return_logits: Literal[True],
    ) -> tuple[Tensor, Tensor]: ...

    @overload
    def forward(
        self,
        tokens: Tensor,
        return_logits: Literal[False],
    ) -> Tensor: ...

    def forward(  # type: ignore
        self,
        tokens: Int[Tensor, "batch seq"],
        return_logits: bool = True,
    ):
        """
        Inputs:
            tokens: Int[Tensor, "batch seq"]
                The input tokens, shape (batch, seq)
            return_logits: bool
                If True, returns (logits, residual, activation)
                If False, returns (residual, activation)
        """

        # Run with hook functions to store the activations & final value of residual stream
        # If return_logits is False, then we compute the last residual stream value but not the logits
        output: Tensor = self.model.run_with_hooks(
            tokens,
            stop_at_layer=self.hook_layer + 1,
            # stop_at_layer = (None if return_logits else self.hook_layer),
            fwd_hooks=[
                (self.hook_point, self.hook_fn_store_act),
                (self.hook_point_resid_final, self.hook_fn_store_act),
            ],
        )

        # The hook functions work by storing data in model's hook context, so we pop them back out
        activation: Tensor = self.model.hook_dict[self.hook_point].ctx.pop("activation")

        if "hook_z" in self.hook_point:
            activation = activation.flatten(-2, -1)

        # if self.hook_point_resid_final == self.hook_point:
        #     residual: Tensor = activation
        # else:
        #     residual: Tensor = self.model.hook_dict[
        #         self.hook_point_resid_final
        #     ].ctx.pop("activation")

        if return_logits:
            return output, activation
        return activation

    def hook_fn_store_act(self, activation: torch.Tensor, hook: HookPoint):
        hook.ctx["activation"] = activation

    @property
    def tokenizer(self):  # type: ignore
        return self.model.tokenizer

    @property
    def W_U(self):
        return self.model.W_U

    @property
    def W_out(self):
        return self.model.W_out

    @property
    def W_O(self):
        return self.model.W_O


def to_resid_dir(dir: Float[Tensor, "feats d_in"], model: TransformerLensWrapper):
    """
    Takes a direction (eg. in the post-ReLU MLP activations) and returns the corresponding dir in the residual stream.

    Args:
        dir:
            The direction in the activations, i.e. shape (feats, d_in) where d_in could be d_model, d_mlp, etc.
        model:
            The model, which should be a HookedTransformerWrapper or similar.
    """
    # If this SAE was trained on the residual stream or attn/mlp out, then we don't need to do anything
    if "resid" in model.hook_point or "_out" in model.hook_point:
        return dir

    # If it was trained on the MLP layer, then we apply the W_out map
    elif ("pre" in model.hook_point) or ("post" in model.hook_point):
        return dir @ model.W_out[model.hook_layer]

    elif "hook_z" in model.hook_point:
        return dir @ model.W_O[model.hook_layer].flatten(0, 1).to(dir.dtype)

    # Others not yet supported
    else:
        raise NotImplementedError(
            "The hook your SAE was trained on isn't yet supported"
        )

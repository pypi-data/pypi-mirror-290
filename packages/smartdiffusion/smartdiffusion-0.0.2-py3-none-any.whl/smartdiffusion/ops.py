"""
    This file is part of smartdiffusion and derived from ComfyUI.
    Copyright (C) 2024 Stability AI & John Slegers

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from torch import float16, bfloat16

from torch.nn import (
    Linear as nn_Linear,
    Conv1d as nn_Conv1d,
    Conv2d as nn_Conv2d,
    Conv3d as nn_Conv3d,
    GroupNorm as nn_GroupNorm,
    LayerNorm as nn_LayerNorm,
    ConvTranspose2d as nn_ConvTranspose2d,
    ConvTranspose1d as nn_ConvTranspose1d,
    Embedding as nn_Embedding,
)
from torch.nn.functional import (
    linear,
    group_norm,
    layer_norm,
    conv_transpose2d,
    conv_transpose1d,
    embedding,
)
from smartdiffusion.model_management import device_should_use_non_blocking


def cast_to(weight, dtype=None, device=None, non_blocking=False):
    return weight.to(device=device, dtype=dtype, non_blocking=non_blocking)


def cast_to_input(weight, input, non_blocking=False):
    return cast_to(weight, input.dtype, input.device, non_blocking=non_blocking)


def cast_bias_weight(s, input=None, dtype=None, device=None):
    if input is not None:
        if dtype is None:
            dtype = input.dtype
        if device is None:
            device = input.device
    bias = None
    non_blocking = device_should_use_non_blocking(device)
    if s.bias is not None:
        bias = cast_to(s.bias, dtype, device, non_blocking=non_blocking)
        if s.bias_function is not None:
            bias = s.bias_function(bias)
    weight = cast_to(s.weight, dtype, device, non_blocking=non_blocking)
    if s.weight_function is not None:
        weight = s.weight_function(weight)
    return weight, bias


class CastWeightBiasOp:
    smartdiffusion_cast_weights = False
    weight_function = None
    bias_function = None


class disable_weight_init:
    class Linear(nn_Linear, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input):
            weight, bias = cast_bias_weight(self, input)
            return linear(input, weight, bias)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class Conv1d(nn_Conv1d, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input):
            weight, bias = cast_bias_weight(self, input)
            return self._conv_forward(input, weight, bias)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class Conv2d(nn_Conv2d, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input):
            weight, bias = cast_bias_weight(self, input)
            return self._conv_forward(input, weight, bias)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class Conv3d(nn_Conv3d, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input):
            weight, bias = cast_bias_weight(self, input)
            return self._conv_forward(input, weight, bias)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class GroupNorm(nn_GroupNorm, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input):
            weight, bias = cast_bias_weight(self, input)
            return group_norm(input, self.num_groups, weight, bias, self.eps)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class LayerNorm(nn_LayerNorm, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input):
            if self.weight is not None:
                weight, bias = cast_bias_weight(self, input)
            else:
                weight = None
                bias = None
            return layer_norm(input, self.normalized_shape, weight, bias, self.eps)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class ConvTranspose2d(nn_ConvTranspose2d, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input, output_size=None):
            num_spatial_dims = 2
            output_padding = self._output_padding(
                input,
                output_size,
                self.stride,
                self.padding,
                self.kernel_size,
                num_spatial_dims,
                self.dilation,
            )

            weight, bias = cast_bias_weight(self, input)
            return conv_transpose2d(
                input,
                weight,
                bias,
                self.stride,
                self.padding,
                output_padding,
                self.groups,
                self.dilation,
            )

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class ConvTranspose1d(nn_ConvTranspose1d, CastWeightBiasOp):
        def reset_parameters(self):
            return None

        def forward_smartdiffusion_cast_weights(self, input, output_size=None):
            num_spatial_dims = 1
            output_padding = self._output_padding(
                input,
                output_size,
                self.stride,
                self.padding,
                self.kernel_size,
                num_spatial_dims,
                self.dilation,
            )

            weight, bias = cast_bias_weight(self, input)
            return conv_transpose1d(
                input,
                weight,
                bias,
                self.stride,
                self.padding,
                output_padding,
                self.groups,
                self.dilation,
            )

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                return super().forward(*args, **kwargs)

    class Embedding(nn_Embedding, CastWeightBiasOp):
        def reset_parameters(self):
            self.bias = None
            return None

        def forward_smartdiffusion_cast_weights(self, input, out_dtype=None):
            output_dtype = out_dtype
            if self.weight.dtype == float16 or self.weight.dtype == bfloat16:
                out_dtype = None
            weight, bias = cast_bias_weight(self, device=input.device, dtype=out_dtype)
            return embedding(
                input,
                weight,
                self.padding_idx,
                self.max_norm,
                self.norm_type,
                self.scale_grad_by_freq,
                self.sparse,
            ).to(dtype=output_dtype)

        def forward(self, *args, **kwargs):
            if self.smartdiffusion_cast_weights:
                return self.forward_smartdiffusion_cast_weights(*args, **kwargs)
            else:
                if "out_dtype" in kwargs:
                    kwargs.pop("out_dtype")
                return super().forward(*args, **kwargs)

    @classmethod
    def conv_nd(s, dims, *args, **kwargs):
        if dims == 2:
            return s.Conv2d(*args, **kwargs)
        elif dims == 3:
            return s.Conv3d(*args, **kwargs)
        else:
            raise ValueError(f"unsupported dimensions: {dims}")


class manual_cast(disable_weight_init):
    class Linear(disable_weight_init.Linear):
        smartdiffusion_cast_weights = True

    class Conv1d(disable_weight_init.Conv1d):
        smartdiffusion_cast_weights = True

    class Conv2d(disable_weight_init.Conv2d):
        smartdiffusion_cast_weights = True

    class Conv3d(disable_weight_init.Conv3d):
        smartdiffusion_cast_weights = True

    class GroupNorm(disable_weight_init.GroupNorm):
        smartdiffusion_cast_weights = True

    class LayerNorm(disable_weight_init.LayerNorm):
        smartdiffusion_cast_weights = True

    class ConvTranspose2d(disable_weight_init.ConvTranspose2d):
        smartdiffusion_cast_weights = True

    class ConvTranspose1d(disable_weight_init.ConvTranspose1d):
        smartdiffusion_cast_weights = True

    class Embedding(disable_weight_init.Embedding):
        smartdiffusion_cast_weights = True

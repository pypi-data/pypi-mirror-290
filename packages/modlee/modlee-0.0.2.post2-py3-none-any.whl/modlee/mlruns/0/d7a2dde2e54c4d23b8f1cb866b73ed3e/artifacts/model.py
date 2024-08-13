
import torch
import torch.nn as nn
from torch.nn import functional as F
import lightning
import lightning.pytorch as pl

import torch
import torch.nn as nn
import inspect

import numpy
import numpy as np

try:
    from torchmetrics.functional import accuracy
except ImportError:
    from pytorch_lightning.metrics.functional import accuracy

#ptorch out-of-box libs needed
from torchvision.utils import _log_api_usage_once

from functools import partial
from typing import Any, Callable, List, Optional, Sequence, Literal

import torch
from torch import nn, Tensor
from torch.nn import functional as F

from torchvision import models
import torchvision
import torchmetrics

# from torchvision.ops.misc import Conv2dNormActivation, Permute
# from torchvision.ops.stochastic_depth import StochasticDepth
# from torchvision.transforms._presets import ImageClassification
# from torchvision.utils import _log_api_usage_once
# from torchvision.models._api import register_model, Weights, WeightsEnum
# from torchvision.models._meta import _IMAGENET_CATEGORIES
# from torchvision.models._utils import _ovewrite_named_param, handle_legacy_interface

# from torchvision.models.convnext import *
# from torchvision.models.convnext import CNBlockConfig

# Modlee imports
import modlee


class ModleeModel(modlee.model.model.ModleeModel):

    def __init__(self, model, loss_fn=F.cross_entropy, *args, **kwargs):
        """
        Constructor for a recommended model.
        """
        super().__init__(*args, **kwargs)
        self.model = model
        self.loss_fn = loss_fn

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx, *args, **kwargs):
        x, y = batch
        y_out = self(x)
        loss = self.loss_fn(y_out, y)
        return {"loss": loss}

    def validation_step(self, val_batch, batch_idx, *args, **kwargs):
        x, y = val_batch
        y_out = self(x)
        loss = self.loss_fn(y_out, y)
        return {"val_loss": loss}

    def configure_optimizers(
        self,
    ):
        """
        Configure a default AdamW optimizer with learning rate decay.
        """
        optimizer = torch.optim.AdamW(self.parameters(), lr=0.001)
        self.scheduler = lr_scheduler.ReduceLROnPlateau(
            optimizer, factor=0.8, patience=5
        )
        return optimizer



class GraphModule(torch.fx.graph_module.GraphModule):

    @compatibility(is_backward_compatible=True)
    def __init__(
        self,
        root: Union[torch.nn.Module, Dict[str, Any]],
        graph: Graph,
        class_name: str = "GraphModule",
    ):
        """
        Construct a GraphModule.

        Args:

            root (Union[torch.nn.Module, Dict[str, Any]):
                ``root`` can either be an nn.Module instance or a Dict mapping strings to any attribute type.
                In the case that ``root`` is a Module, any references to Module-based objects (via qualified
                name) in the Graph's Nodes' ``target`` field will be copied over from the respective place
                within ``root``'s Module hierarchy into the GraphModule's module hierarchy.
                In the case that ``root`` is a dict, the qualified name found in a Node's ``target`` will be
                looked up directly in the dict's keys. The object mapped to by the Dict will be copied
                over into the appropriate place within the GraphModule's module hierarchy.

            graph (Graph): ``graph`` contains the nodes this GraphModule should use for code generation

            class_name (str): ``name`` denotes the name of this GraphModule for debugging purposes. If it's unset, all
                error messages will report as originating from ``GraphModule``. It may be helpful to set this
                to ``root``'s original name or a name that makes sense within the context of your transform.
        """
        super().__init__()
        self.__class__.__name__ = class_name
        if isinstance(root, torch.nn.Module):
            if hasattr(root, "training"):
                self.training = root.training

            # When we pickle/unpickle graph module, we don't want to drop any module or attributes.
            if isinstance(root, _CodeOnlyModule):
                for k, _ in root.named_children():
                    _copy_attr(root, self, k)

                for k, _ in root.named_buffers():
                    _copy_attr(root, self, k)

                for k, _ in root.named_parameters():
                    _copy_attr(root, self, k)

            for node in graph.nodes:
                if node.op in ["get_attr", "call_module"]:
                    assert isinstance(node.target, str)
                    _copy_attr(root, self, node.target)
        elif isinstance(root, dict):
            targets_to_copy = []
            for node in graph.nodes:
                if node.op in ["get_attr", "call_module"]:
                    assert isinstance(node.target, str)
                    if node.target not in root:
                        raise RuntimeError(
                            "Node "
                            + str(node)
                            + " referenced target "
                            + node.target
                            + " but that target was not provided in ``root``!"
                        )
                    targets_to_copy.append(node.target)
            # Sort targets in ascending order of the # of atoms.
            # This will ensure that less deeply nested attributes are assigned
            # before more deeply nested attributes. For example, foo.bar
            # will be assigned before foo.bar.baz. Otherwise, we might assign
            # the user-provided ``foo.bar`` and wipe out the previously-assigned
            # ``foo.bar.baz``
            targets_to_copy.sort(key=lambda t: t.count("."))
            for target_to_copy in targets_to_copy:
                _assign_attr(root[target_to_copy], self, target_to_copy)
        else:
            raise RuntimeError("Unsupported type " + str(root) + " passed for root!")

        self.graph = graph

        # Store the Tracer class responsible for creating a Graph separately as part of the
        # GraphModule state, except when the Tracer is defined in a local namespace.
        # Locally defined Tracers are not pickleable. This is needed because torch.package will
        # serialize a GraphModule without retaining the Graph, and needs to use the correct Tracer
        # to re-create the Graph during deserialization.
        self._tracer_cls = None
        if (
            self.graph._tracer_cls
            and "<locals>" not in self.graph._tracer_cls.__qualname__
        ):
            self._tracer_cls = self.graph._tracer_cls

        self._tracer_extras = {}
        if self.graph._tracer_extras:
            self._tracer_extras = self.graph._tracer_extras

        # Dictionary to store metadata
        self.meta: Dict[str, Any] = {}
        self._replace_hook = None

def forward(self, input_1):
    conv = self.Conv(input_1);  input_1 = None
    conv_1 = self.Conv_1(conv);  conv = None
    relu = self.Relu(conv_1);  conv_1 = None
    max_pool = self.MaxPool(relu);  relu = None
    conv_2 = self.Conv_2(max_pool)
    relu_1 = self.Relu_1(conv_2);  conv_2 = None
    conv_3 = self.Conv_3(relu_1);  relu_1 = None
    add = self.Add(conv_3, max_pool);  conv_3 = max_pool = None
    relu_2 = self.Relu_2(add);  add = None
    conv_4 = self.Conv_4(relu_2)
    relu_3 = self.Relu_3(conv_4);  conv_4 = None
    conv_5 = self.Conv_5(relu_3);  relu_3 = None
    add_1 = self.Add_1(conv_5, relu_2);  conv_5 = relu_2 = None
    relu_4 = self.Relu_4(add_1);  add_1 = None
    conv_6 = self.Conv_6(relu_4)
    relu_5 = self.Relu_5(conv_6);  conv_6 = None
    conv_7 = self.Conv_7(relu_5);  relu_5 = None
    conv_8 = self.Conv_8(relu_4);  relu_4 = None
    add_2 = self.Add_2(conv_7, conv_8);  conv_7 = conv_8 = None
    relu_6 = self.Relu_6(add_2);  add_2 = None
    conv_9 = self.Conv_9(relu_6)
    relu_7 = self.Relu_7(conv_9);  conv_9 = None
    conv_10 = self.Conv_10(relu_7);  relu_7 = None
    add_3 = self.Add_3(conv_10, relu_6);  conv_10 = relu_6 = None
    relu_8 = self.Relu_8(add_3);  add_3 = None
    conv_11 = self.Conv_11(relu_8)
    relu_9 = self.Relu_9(conv_11);  conv_11 = None
    conv_12 = self.Conv_12(relu_9);  relu_9 = None
    conv_13 = self.Conv_13(relu_8);  relu_8 = None
    add_4 = self.Add_4(conv_12, conv_13);  conv_12 = conv_13 = None
    relu_10 = self.Relu_10(add_4);  add_4 = None
    conv_14 = self.Conv_14(relu_10)
    relu_11 = self.Relu_11(conv_14);  conv_14 = None
    conv_15 = self.Conv_15(relu_11);  relu_11 = None
    add_5 = self.Add_5(conv_15, relu_10);  conv_15 = relu_10 = None
    relu_12 = self.Relu_12(add_5);  add_5 = None
    conv_16 = self.Conv_16(relu_12)
    relu_13 = self.Relu_13(conv_16);  conv_16 = None
    conv_17 = self.Conv_17(relu_13);  relu_13 = None
    conv_18 = self.Conv_18(relu_12);  relu_12 = None
    add_6 = self.Add_6(conv_17, conv_18);  conv_17 = conv_18 = None
    relu_14 = self.Relu_14(add_6);  add_6 = None
    conv_19 = self.Conv_19(relu_14)
    relu_15 = self.Relu_15(conv_19);  conv_19 = None
    conv_20 = self.Conv_20(relu_15);  relu_15 = None
    add_7 = self.Add_7(conv_20, relu_14);  conv_20 = relu_14 = None
    relu_16 = self.Relu_16(add_7);  add_7 = None
    global_average_pool = self.GlobalAveragePool(relu_16);  relu_16 = None
    flatten = self.Flatten(global_average_pool);  global_average_pool = None
    gemm = self.Gemm(flatten);  flatten = None
    gemm_1 = self.Gemm_1(gemm);  gemm = None
    return gemm_1



class OnnxGlobalAveragePoolWithKnownInputShape(torch.nn.modules.module.Module):

    def __init__(self, input_shape: List[int]):
        super().__init__()
        self.input_shape = input_shape
        self._x_dims = list(range(2, len(self.input_shape)))

    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:  # pylint: disable=missing-function-docstring
        forward_lambda = lambda: torch.mean(input_tensor, dim=self._x_dims, keepdim=True)

        if torch.onnx.is_in_onnx_export():
            return DefaultExportToOnnx.export(forward_lambda, 'GlobalAveragePool', input_tensor, {})

        return forward_lambda()



class OnnxBinaryMathOperation(torch.nn.modules.module.Module):

    def __init__(self, operation_type: str, broadcast: Optional[int] = None, axis: Optional[int] = None):
        super().__init__()
        self.operation_type = operation_type
        self.broadcast = broadcast
        self.axis = axis
        self.operation_type = operation_type
        self.math_op_function = _TORCH_FUNCTION_FROM_ONNX_TYPE[self.operation_type]

    def forward(  # pylint: disable=missing-function-docstring
        self,
        first: torch.Tensor,
        second: torch.Tensor,
    ) -> torch.Tensor:
        if self.broadcast == 1 and self.axis is not None:
            second = old_style_broadcast(first, second, self.axis)

        return self.math_op_function(first, second)



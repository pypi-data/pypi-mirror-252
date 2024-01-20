"""
"""
# pyright: reportPrivateImportUsage=false

from __future__ import annotations

import importlib
from contextlib import contextmanager
from ctypes import CDLL
from typing import TYPE_CHECKING, Any
from typing import Tuple

from .utils import cuda_unavailable
from .utils import maybe_import_torch
from .utils import maybe_import_bitsandbytes

if TYPE_CHECKING:
    import torch as Torch


if (torch := maybe_import_torch()) and (bnb := maybe_import_bitsandbytes()):

    from torch.utils.weak import WeakTensorKeyDictionary

    with cuda_unavailable(torch):
        from bitsandbytes import cextension
        from bitsandbytes import functional
        from bitsandbytes.cuda_setup.main import CUDASetup
        from bitsandbytes.nn import Int8Params
        from bitsandbytes.nn import Params4bit

    _param_to_8bit   = Int8Params.to     # type: ignore
    _param_cuda_8bit = Int8Params.cuda
    _param_to_4bit   = Params4bit.to     # type: ignore
    _param_cuda_4bit = Params4bit.cuda

    TensorToArgs = Tuple[torch.device, torch.dtype, bool, torch.memory_format]

    to_ops_8bit: dict[Int8Params, TensorToArgs | None] = WeakTensorKeyDictionary() # type: ignore
    to_ops_4bit: dict[Params4bit, TensorToArgs | None] = WeakTensorKeyDictionary() # type: ignore

    def _to_op_register_8bit(self: Int8Params, *args, **kwargs):
        parsed = torch._C._nn._parse_to(*args, **kwargs)
        device, *_ = parsed
        if not isinstance(device, torch.device): # pragma: no cover
            return _param_to_8bit(self, *args, **kwargs)
        if device.type != 'cuda':
            return _param_to_8bit(self, *args, **kwargs)
        to_ops_8bit[self] = parsed
        return self

    def _to_op_register_4bit(self: Params4bit, *args, **kwargs):
        parsed = torch._C._nn._parse_to(*args, **kwargs)
        device, *_ = parsed
        if not isinstance(device, torch.device): # pragma: no cover
            return _param_to_4bit(self, *args, **kwargs)
        if device.type != 'cuda':
            return _param_to_4bit(self, *args, **kwargs)
        to_ops_4bit[self] = parsed
        return self

    def _cuda_op_arg_check(device: Torch.device | int | str | None) -> bool:
        if device is None: # pragma: no cover
            return True
        if isinstance(device, int):
            return True
        if isinstance(device, str): # pragma: no cover
            device = torch.device(device)
        return device.type == 'cuda' # pragma: no cover

    def _cuda_op_register_8bit(self: Int8Params, device: Torch.device | int | str | None = None, **kwargs):
        if not _cuda_op_arg_check(device): # pragma: no cover
            # Let PyTorch handle the fail
            return _param_cuda_8bit(self, device, **kwargs)
        to_ops_8bit[self] = None
        return self

    def _cuda_op_register_4bit(self: Params4bit, device: Torch.device | int | str | None = None, **kwargs):
        if not _cuda_op_arg_check(device): # pragma: no cover
            # Let PyTorch handle the fail
            return _param_cuda_4bit(self, device, **kwargs)
        to_ops_4bit[self] = None
        return self

    def _patch():
        Int8Params.to   = _to_op_register_8bit   # type: ignore
        Int8Params.cuda = _cuda_op_register_8bit # type: ignore
        Params4bit.to   = _to_op_register_4bit   # type: ignore
        Params4bit.cuda = _cuda_op_register_4bit # type: ignore

    def _unpatch():
        Int8Params.to   = _param_to_8bit   # type: ignore
        Int8Params.cuda = _param_cuda_8bit
        Params4bit.to   = _param_to_4bit   # type: ignore
        Params4bit.cuda = _param_cuda_4bit

    def _move():
        CUDASetup._instance = None
        importlib.reload(cextension)
        functional.lib = cextension.lib
        for op in to_ops_8bit.items():
            tensor, parsed_args = op
            if parsed_args:
                _, dtype, _, memory_format = parsed_args
            else:
                dtype, memory_format = None, None
            tensor.data = _param_to_8bit(tensor,
                device='cuda',
                dtype=dtype,
                memory_format=memory_format,
            ) # type: ignore
        for op in to_ops_4bit.items():
            tensor, parsed_args = op
            if parsed_args:
                _, dtype, _, memory_format = parsed_args
            else:
                dtype, memory_format = None, None
            tensor.data = _param_to_4bit(tensor,
                device='cuda',
                dtype=dtype,
                memory_format=memory_format,
            ) # type: ignore

else:

    _patch = lambda: None
    _unpatch = lambda: None
    _move = lambda: None


patch = _patch
unpatch = _unpatch
move = _move

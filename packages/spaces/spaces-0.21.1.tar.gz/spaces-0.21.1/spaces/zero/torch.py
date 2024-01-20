"""
"""
# pyright: reportPrivateImportUsage=false

from __future__ import annotations

import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING
from typing import Any
from typing import Tuple

from . import bitsandbytes
from .utils import maybe_import_torch

if TYPE_CHECKING:
    import torch as Torch


CUDA_MEM_GET_INFO = (23156817920, 23836033024) # Nvidia A10G (drivers 510) / Torch 2.0.1


if (torch := maybe_import_torch()):

    from torch.utils.weak import WeakTensorKeyDictionary

    _tensor_to         = torch.Tensor.to
    _tensor_cuda       = torch.Tensor.cuda
    _tensor            = torch.tensor
    _cuda_init         = torch._C._cuda_init
    _cuda_available    = torch.cuda.is_available
    _cuda_device_count = torch.cuda.device_count
    _cuda_mem_get_info = torch.cuda.mem_get_info

    TensorToArgs = Tuple[torch.device, torch.dtype, bool, torch.memory_format]

    to_ops: dict[Torch.Tensor, TensorToArgs | None] = WeakTensorKeyDictionary() # type: ignore

    def _to_op_register(self: Torch.Tensor, *args, **kwargs):
        parsed = torch._C._nn._parse_to(*args, **kwargs)
        device, *_ = parsed
        if not isinstance(device, torch.device):
            return _tensor_to(self, *args, **kwargs)
        if device.type != 'cuda':
            return _tensor_to(self, *args, **kwargs)
        to_ops[self] = parsed
        return self

    def _cuda_op_arg_check(device: Torch.device | int | str | None) -> bool:
        if device is None:
            return True
        if isinstance(device, int):
            return True
        if isinstance(device, str):
            device = torch.device(device)
        return device.type == 'cuda'

    def _cuda_op_register(self: Torch.Tensor, device: Torch.device | int | str | None = None, **kwargs):
        if not _cuda_op_arg_check(device):
            # Let PyTorch handle the fail
            return _tensor_cuda(self, device, **kwargs)
        to_ops[self] = None
        return self

    def _cuda_init_raise():
        raise RuntimeError(
            "CUDA must not be initialized in the main process "
            "on Spaces with Stateless GPU environment.\n"
            "You can look at this Stacktrace to find out "
            "which part of your code triggered a CUDA init"
        )

    def _tensor_register(*args: Any, **kwargs: Any):
        try:
            device = torch.device(kwargs.get('device', "cpu"))
        except Exception:
            return _tensor(*args, **kwargs)
        if device.type != 'cuda':
            return _tensor(*args, **kwargs)
        tensor = _tensor(*args, **{**kwargs, 'device': "cpu"})
        to_ops[tensor] = None
        return tensor

    def _patch():
        torch.Tensor.to         = _to_op_register   # type: ignore
        torch.Tensor.cuda       = _cuda_op_register # type: ignore
        torch.tensor            = _tensor_register
        torch._C._cuda_init     = _cuda_init_raise
        torch.cuda.is_available = lambda: True
        torch.cuda.device_count = lambda: 1
        torch.cuda.mem_get_info = lambda *args, **kwargs: CUDA_MEM_GET_INFO
        bitsandbytes.patch()

    def _unpatch():
        torch.Tensor.to         = _tensor_to
        torch.Tensor.cuda       = _tensor_cuda
        torch.tensor            = _tensor
        torch._C._cuda_init     = _cuda_init
        torch.cuda.is_available = _cuda_available
        torch.cuda.device_count = _cuda_device_count
        torch.cuda.mem_get_info = _cuda_mem_get_info
        bitsandbytes.unpatch()

    def _move(nvidia_uuid: str):
        os.environ['CUDA_VISIBLE_DEVICES'] = nvidia_uuid
        for op in to_ops.items():
            tensor, parsed_args = op
            if parsed_args:
                _, dtype, _, memory_format = parsed_args
            else:
                dtype, memory_format = None, None
            tensor.data = _tensor_to(tensor,
                device='cuda',
                dtype=dtype,
                memory_format=memory_format,
            ) # type: ignore
        torch.cuda.init()
        bitsandbytes.move()

    def _is_in_bad_fork():
        with ProcessPoolExecutor(mp_context=multiprocessing.get_context('fork')) as e:
            f = e.submit(torch.cuda._is_in_bad_fork)
            return f.result()

    def _disable_cuda_intercept():
        torch.Tensor.to   = _tensor_to
        torch.Tensor.cuda = _tensor_cuda

else:

    _patch = lambda: None
    _unpatch = lambda: None
    _move = lambda nvidia_uuid: None
    _is_in_bad_fork = lambda: False
    _disable_cuda_intercept = lambda: None


patch = _patch
unpatch = _unpatch
move = _move
is_in_bad_fork = _is_in_bad_fork
disable_cuda_intercept = _disable_cuda_intercept

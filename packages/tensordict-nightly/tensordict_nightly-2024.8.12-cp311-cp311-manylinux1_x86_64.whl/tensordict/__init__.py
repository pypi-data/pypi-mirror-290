# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import tensordict._reductions
from tensordict._lazy import LazyStackedTensorDict
from tensordict._td import is_tensor_collection, TensorDict
from tensordict.base import (
    get_defaults_to_none,
    set_get_defaults_to_none,
    TensorDictBase,
)
from tensordict.functional import (
    dense_stack_tds,
    make_tensordict,
    merge_tensordicts,
    pad,
    pad_sequence,
)
from tensordict.memmap import MemoryMappedTensor
from tensordict.persistent import PersistentTensorDict
from tensordict.tensorclass import NonTensorData, NonTensorStack, tensorclass
from tensordict.utils import (
    assert_allclose_td,
    assert_close,
    is_batchedtensor,
    is_tensorclass,
    lazy_legacy,
    NestedKey,
    set_lazy_legacy,
)
from tensordict._pytree import *
from tensordict._C import (  # @manual=//pytorch/tensordict:_C
    unravel_key,
    unravel_key_list,
)
from tensordict.nn import TensorDictParams

try:
    from tensordict.version import __version__  # @manual=//pytorch/tensordict:version
except ImportError:
    __version__ = None

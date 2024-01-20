from typing import Any, Dict, Hashable, List, NamedTuple, Tuple, Union

import jax.numpy as jnp
import numpy.typing as npt

# JAX types
FloatJax = Union[jnp.float16, jnp.float32, jnp.float64]
IntJax = Union[
    jnp.int8,
    jnp.int16,
    jnp.int32,
    jnp.int64,
    jnp.uint8,
    jnp.uint16,
    jnp.uint32,
    jnp.uint64,
]
ArrayJax = jnp.ndarray
TensorJax = jnp.ndarray
VectorJax = ArrayJax
MatrixJax = ArrayJax
PyTree = Union[
    TensorJax,
    Dict[Hashable, "PyTree"],
    List["PyTree"],
    NamedTuple,
    Tuple["PyTree"],
    None,
    Any,
]

# Mixed JAX / NumPy types
Array = Union[npt.NDArray, ArrayJax]
Tensor = Union[npt.NDArray, ArrayJax]
Vector = Array
Matrix = Array
Bool = Union[bool, ArrayJax]
Int = Union[int, IntJax]
Float = Union[float, FloatJax]

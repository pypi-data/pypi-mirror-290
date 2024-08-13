# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/datatypes/tensor_dimension_index_slider.fbs".

# You can extend this class by creating a "TensorDimensionIndexSliderExt" class in "tensor_dimension_index_slider_ext.py".

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa
from attrs import define, field

from ..._baseclasses import (
    BaseBatch,
    BaseExtensionType,
)
from .tensor_dimension_index_slider_ext import TensorDimensionIndexSliderExt

__all__ = [
    "TensorDimensionIndexSlider",
    "TensorDimensionIndexSliderArrayLike",
    "TensorDimensionIndexSliderBatch",
    "TensorDimensionIndexSliderLike",
    "TensorDimensionIndexSliderType",
]


@define(init=False)
class TensorDimensionIndexSlider(TensorDimensionIndexSliderExt):
    """**Datatype**: Defines a slider for the index of some dimension."""

    def __init__(self: Any, dimension: TensorDimensionIndexSliderLike):
        """
        Create a new instance of the TensorDimensionIndexSlider datatype.

        Parameters
        ----------
        dimension:
            The dimension number.

        """

        # You can define your own __init__ function as a member of TensorDimensionIndexSliderExt in tensor_dimension_index_slider_ext.py
        self.__attrs_init__(dimension=dimension)

    dimension: int = field(converter=int)
    # The dimension number.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    def __array__(self, dtype: npt.DTypeLike = None) -> npt.NDArray[Any]:
        # You can define your own __array__ function as a member of TensorDimensionIndexSliderExt in tensor_dimension_index_slider_ext.py
        return np.asarray(self.dimension, dtype=dtype)

    def __int__(self) -> int:
        return int(self.dimension)

    def __hash__(self) -> int:
        return hash(self.dimension)


if TYPE_CHECKING:
    TensorDimensionIndexSliderLike = Union[TensorDimensionIndexSlider, int]
else:
    TensorDimensionIndexSliderLike = Any

TensorDimensionIndexSliderArrayLike = Union[
    TensorDimensionIndexSlider, Sequence[TensorDimensionIndexSliderLike], npt.ArrayLike
]


class TensorDimensionIndexSliderType(BaseExtensionType):
    _TYPE_NAME: str = "rerun.blueprint.datatypes.TensorDimensionIndexSlider"

    def __init__(self) -> None:
        pa.ExtensionType.__init__(
            self, pa.struct([pa.field("dimension", pa.uint32(), nullable=False, metadata={})]), self._TYPE_NAME
        )


class TensorDimensionIndexSliderBatch(BaseBatch[TensorDimensionIndexSliderArrayLike]):
    _ARROW_TYPE = TensorDimensionIndexSliderType()

    @staticmethod
    def _native_to_pa_array(data: TensorDimensionIndexSliderArrayLike, data_type: pa.DataType) -> pa.Array:
        return TensorDimensionIndexSliderExt.native_to_pa_array_override(data, data_type)

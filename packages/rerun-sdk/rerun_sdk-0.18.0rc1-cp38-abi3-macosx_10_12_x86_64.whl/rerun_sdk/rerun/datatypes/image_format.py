# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/datatypes/image_format.fbs".

# You can extend this class by creating a "ImageFormatExt" class in "image_format_ext.py".

from __future__ import annotations

from typing import Any, Sequence, Union

import numpy as np
import pyarrow as pa
from attrs import define, field

from .. import datatypes
from .._baseclasses import (
    BaseBatch,
    BaseExtensionType,
)
from .image_format_ext import ImageFormatExt

__all__ = ["ImageFormat", "ImageFormatArrayLike", "ImageFormatBatch", "ImageFormatLike", "ImageFormatType"]


@define(init=False)
class ImageFormat(ImageFormatExt):
    """**Datatype**: The metadata describing the contents of a [`components.ImageBuffer`][rerun.components.ImageBuffer]."""

    def __init__(
        self: Any,
        width: int,
        height: int,
        pixel_format: datatypes.PixelFormatLike | None = None,
        color_model: datatypes.ColorModelLike | None = None,
        channel_datatype: datatypes.ChannelDatatypeLike | None = None,
    ):
        """
        Create a new instance of the ImageFormat datatype.

        Parameters
        ----------
        width:
            The width of the image in pixels.
        height:
            The height of the image in pixels.
        pixel_format:
            Used mainly for chroma downsampled formats and differing number of bits per channel.

            If specified, this takes precedence over both [`datatypes.ColorModel`][rerun.datatypes.ColorModel] and [`datatypes.ChannelDatatype`][rerun.datatypes.ChannelDatatype] (which are ignored).
        color_model:
            L, RGB, RGBA, …

            Also requires a [`datatypes.ChannelDatatype`][rerun.datatypes.ChannelDatatype] to fully specify the pixel format.
        channel_datatype:
            The data type of each channel (e.g. the red channel) of the image data (U8, F16, …).

            Also requires a [`datatypes.ColorModel`][rerun.datatypes.ColorModel] to fully specify the pixel format.

        """

        # You can define your own __init__ function as a member of ImageFormatExt in image_format_ext.py
        self.__attrs_init__(
            width=width,
            height=height,
            pixel_format=pixel_format,
            color_model=color_model,
            channel_datatype=channel_datatype,
        )

    width: int = field(converter=int)
    # The width of the image in pixels.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    height: int = field(converter=int)
    # The height of the image in pixels.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    pixel_format: datatypes.PixelFormat | None = field(
        default=None,
        converter=ImageFormatExt.pixel_format__field_converter_override,  # type: ignore[misc]
    )
    # Used mainly for chroma downsampled formats and differing number of bits per channel.
    #
    # If specified, this takes precedence over both [`datatypes.ColorModel`][rerun.datatypes.ColorModel] and [`datatypes.ChannelDatatype`][rerun.datatypes.ChannelDatatype] (which are ignored).
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    color_model: datatypes.ColorModel | None = field(
        default=None,
        converter=ImageFormatExt.color_model__field_converter_override,  # type: ignore[misc]
    )
    # L, RGB, RGBA, …
    #
    # Also requires a [`datatypes.ChannelDatatype`][rerun.datatypes.ChannelDatatype] to fully specify the pixel format.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    channel_datatype: datatypes.ChannelDatatype | None = field(
        default=None,
        converter=ImageFormatExt.channel_datatype__field_converter_override,  # type: ignore[misc]
    )
    # The data type of each channel (e.g. the red channel) of the image data (U8, F16, …).
    #
    # Also requires a [`datatypes.ColorModel`][rerun.datatypes.ColorModel] to fully specify the pixel format.
    #
    # (Docstring intentionally commented out to hide this field from the docs)


ImageFormatLike = ImageFormat
ImageFormatArrayLike = Union[
    ImageFormat,
    Sequence[ImageFormatLike],
]


class ImageFormatType(BaseExtensionType):
    _TYPE_NAME: str = "rerun.datatypes.ImageFormat"

    def __init__(self) -> None:
        pa.ExtensionType.__init__(
            self,
            pa.struct([
                pa.field("width", pa.uint32(), nullable=False, metadata={}),
                pa.field("height", pa.uint32(), nullable=False, metadata={}),
                pa.field("pixel_format", pa.uint8(), nullable=True, metadata={}),
                pa.field("color_model", pa.uint8(), nullable=True, metadata={}),
                pa.field("channel_datatype", pa.uint8(), nullable=True, metadata={}),
            ]),
            self._TYPE_NAME,
        )


class ImageFormatBatch(BaseBatch[ImageFormatArrayLike]):
    _ARROW_TYPE = ImageFormatType()

    @staticmethod
    def _native_to_pa_array(data: ImageFormatArrayLike, data_type: pa.DataType) -> pa.Array:
        from rerun.datatypes import ChannelDatatypeBatch, ColorModelBatch, PixelFormatBatch

        if isinstance(data, ImageFormat):
            data = [data]

        return pa.StructArray.from_arrays(
            [
                pa.array(np.asarray([x.width for x in data], dtype=np.uint32)),
                pa.array(np.asarray([x.height for x in data], dtype=np.uint32)),
                PixelFormatBatch([x.pixel_format for x in data]).as_arrow_array().storage,  # type: ignore[misc, arg-type]
                ColorModelBatch([x.color_model for x in data]).as_arrow_array().storage,  # type: ignore[misc, arg-type]
                ChannelDatatypeBatch([x.channel_datatype for x in data]).as_arrow_array().storage,  # type: ignore[misc, arg-type]
            ],
            fields=list(data_type),
        )

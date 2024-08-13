# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/components/space_view_origin.fbs".

# You can extend this class by creating a "SpaceViewOriginExt" class in "space_view_origin_ext.py".

from __future__ import annotations

from ... import datatypes
from ..._baseclasses import (
    ComponentBatchMixin,
    ComponentMixin,
)

__all__ = ["SpaceViewOrigin", "SpaceViewOriginBatch", "SpaceViewOriginType"]


class SpaceViewOrigin(datatypes.EntityPath, ComponentMixin):
    """**Component**: The origin of a `SpaceView`."""

    _BATCH_TYPE = None
    # You can define your own __init__ function as a member of SpaceViewOriginExt in space_view_origin_ext.py

    # Note: there are no fields here because SpaceViewOrigin delegates to datatypes.EntityPath
    pass


class SpaceViewOriginType(datatypes.EntityPathType):
    _TYPE_NAME: str = "rerun.blueprint.components.SpaceViewOrigin"


class SpaceViewOriginBatch(datatypes.EntityPathBatch, ComponentBatchMixin):
    _ARROW_TYPE = SpaceViewOriginType()


# This is patched in late to avoid circular dependencies.
SpaceViewOrigin._BATCH_TYPE = SpaceViewOriginBatch  # type: ignore[assignment]

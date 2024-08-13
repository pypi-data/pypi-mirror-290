# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/views/text_log.fbs".

from __future__ import annotations

from typing import Union

__all__ = ["TextLogView"]


from ... import datatypes
from ..._baseclasses import AsComponents, ComponentBatchLike
from ...datatypes import EntityPathLike, Utf8Like
from ..api import SpaceView, SpaceViewContentsLike


class TextLogView(SpaceView):
    """
    **View**: A view of a text log, for use with [`archetypes.TextLog`][rerun.archetypes.TextLog].

    Example
    -------
    ### Use a blueprint to show a TextLogView.:
    ```python
    import rerun as rr
    import rerun.blueprint as rrb

    rr.init("rerun_example_text_log", spawn=True)

    rr.set_time_sequence("time", 0)
    rr.log("log/status", rr.TextLog("Application started.", level=rr.TextLogLevel.INFO))
    rr.set_time_sequence("time", 5)
    rr.log("log/other", rr.TextLog("A warning.", level=rr.TextLogLevel.WARN))
    for i in range(10):
        rr.set_time_sequence("time", i)
        rr.log("log/status", rr.TextLog(f"Processing item {i}.", level=rr.TextLogLevel.INFO))

    # Create a text view that displays all logs.
    blueprint = rrb.Blueprint(rrb.TextLogView(origin="/log", name="Text Logs"), collapse_panels=True)

    rr.send_blueprint(blueprint)
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/text_log/457ab91ec42a481bacae4146c0fc01eee397bb86/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/text_log/457ab91ec42a481bacae4146c0fc01eee397bb86/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/text_log/457ab91ec42a481bacae4146c0fc01eee397bb86/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/text_log/457ab91ec42a481bacae4146c0fc01eee397bb86/1200w.png">
      <img src="https://static.rerun.io/text_log/457ab91ec42a481bacae4146c0fc01eee397bb86/full.png" width="640">
    </picture>
    </center>

    """

    def __init__(
        self,
        *,
        origin: EntityPathLike = "/",
        contents: SpaceViewContentsLike = "$origin/**",
        name: Utf8Like | None = None,
        visible: datatypes.BoolLike | None = None,
        defaults: list[Union[AsComponents, ComponentBatchLike]] = [],
        overrides: dict[EntityPathLike, list[ComponentBatchLike]] = {},
    ) -> None:
        """
        Construct a blueprint for a new TextLogView view.

        Parameters
        ----------
        origin:
            The `EntityPath` to use as the origin of this view.
            All other entities will be transformed to be displayed relative to this origin.
        contents:
            The contents of the view specified as a query expression.
            This is either a single expression, or a list of multiple expressions.
            See [rerun.blueprint.archetypes.SpaceViewContents][].
        name:
            The display name of the view.
        visible:
            Whether this view is visible.

            Defaults to true if not specified.
        defaults:
            List of default components or component batches to add to the space view. When an archetype
            in the view is missing a component included in this set, the value of default will be used
            instead of the normal fallback for the visualizer.
        overrides:
            Dictionary of overrides to apply to the space view. The key is the path to the entity where the override
            should be applied. The value is a list of component or component batches to apply to the entity.

            Important note: the path must be a fully qualified entity path starting at the root. The override paths
            do not yet support `$origin` relative paths or glob expressions.
            This will be addressed in: [https://github.com/rerun-io/rerun/issues/6673][].

        """

        properties: dict[str, AsComponents] = {}
        super().__init__(
            class_identifier="TextLog",
            origin=origin,
            contents=contents,
            name=name,
            visible=visible,
            properties=properties,
            defaults=defaults,
            overrides=overrides,
        )

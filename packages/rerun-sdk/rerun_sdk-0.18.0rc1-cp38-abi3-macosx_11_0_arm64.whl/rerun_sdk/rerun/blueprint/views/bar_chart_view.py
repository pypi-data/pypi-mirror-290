# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/views/bar_chart.fbs".

from __future__ import annotations

from typing import Union

__all__ = ["BarChartView"]


from ... import datatypes
from ..._baseclasses import AsComponents, ComponentBatchLike
from ...datatypes import EntityPathLike, Utf8Like
from .. import archetypes as blueprint_archetypes, components as blueprint_components
from ..api import SpaceView, SpaceViewContentsLike


class BarChartView(SpaceView):
    """
    **View**: A bar chart view.

    Example
    -------
    ### Use a blueprint to create a BarChartView.:
    ```python
    import rerun as rr
    import rerun.blueprint as rrb

    rr.init("rerun_example_bar_chart", spawn=True)
    # It's recommended to log bar charts with the `rr.BarChart` archetype,
    # but single dimensional tensors can also be used if a `BarChartView` is created explicitly.
    rr.log("tensor", rr.Tensor([8, 4, 0, 9, 1, 4, 1, 6, 9, 0]))

    # Create a bar chart view to display the chart.
    blueprint = rrb.Blueprint(rrb.BarChartView(origin="tensor", name="Bar Chart"), collapse_panels=True)

    rr.send_blueprint(blueprint)
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/bar_chart_view/74fa45af3c7310b51cd283c37439ed8f8ca9356d/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/bar_chart_view/74fa45af3c7310b51cd283c37439ed8f8ca9356d/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/bar_chart_view/74fa45af3c7310b51cd283c37439ed8f8ca9356d/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/bar_chart_view/74fa45af3c7310b51cd283c37439ed8f8ca9356d/1200w.png">
      <img src="https://static.rerun.io/bar_chart_view/74fa45af3c7310b51cd283c37439ed8f8ca9356d/full.png" width="640">
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
        plot_legend: blueprint_archetypes.PlotLegend | blueprint_components.Corner2D | None = None,
    ) -> None:
        """
        Construct a blueprint for a new BarChartView view.

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
        plot_legend:
            Configures the legend of the plot.

        """

        properties: dict[str, AsComponents] = {}
        if plot_legend is not None:
            if not isinstance(plot_legend, blueprint_archetypes.PlotLegend):
                plot_legend = blueprint_archetypes.PlotLegend(plot_legend)
            properties["PlotLegend"] = plot_legend

        super().__init__(
            class_identifier="BarChart",
            origin=origin,
            contents=contents,
            name=name,
            visible=visible,
            properties=properties,
            defaults=defaults,
            overrides=overrides,
        )

from typing import Optional, Any
from pathlib import Path
from functools import partial
import panel as pn
import xarray as xr
from param import Parameter
from bencher.results.bench_result_base import BenchResultBase, ReduceType
from bencher.variables.results import (
    ResultVideo,
    ResultContainer,
    ResultReference,
    PANEL_TYPES,
)


class PanelResult(BenchResultBase):
    def to_video(self, **kwargs):
        return self.map_plots(partial(self.to_video_multi, **kwargs))

    def to_video_multi(self, result_var: Parameter, **kwargs) -> Optional[pn.Column]:
        if isinstance(result_var, (ResultVideo, ResultContainer)):
            vid_p = []

            xr_dataset = self.to_hv_dataset(ReduceType.SQUEEZE)

            def to_video_da(da, **kwargs):
                if da is not None and Path(da).exists():
                    vid = pn.pane.Video(da, autoplay=True, **kwargs)
                    vid.loop = True
                    vid_p.append(vid)
                    return vid
                return pn.pane.Markdown(f"video does not exist {da}")

            plot_callback = partial(self.ds_to_container, container=partial(to_video_da, **kwargs))

            panes = self.to_panes_multi_panel(
                xr_dataset, result_var, plot_callback=plot_callback, target_dimension=0
            )

            def play_vid(_):  # pragma: no cover
                for r in vid_p:
                    r.paused = False
                    r.loop = False

            def pause_vid(_):  # pragma: no cover
                for r in vid_p:
                    r.paused = True

            def reset_vid(_):  # pragma: no cover
                for r in vid_p:
                    r.paused = False
                    r.time = 0

            def loop_vid(_):  # pragma: no cover
                for r in vid_p:
                    r.paused = False
                    r.time = 0
                    r.loop = True

            button_names = ["Play Videos", "Pause Videos", "Loop Videos", "Reset Videos"]
            buttom_cb = [play_vid, pause_vid, reset_vid, loop_vid]
            buttons = pn.Row()

            for name, cb in zip(button_names, buttom_cb):
                button = pn.widgets.Button(name=name)
                pn.bind(cb, button, watch=True)
                buttons.append(button)

            return pn.Column(buttons, panes)
        return None

    def zero_dim_da_to_val(self, da_ds: xr.DataArray | xr.Dataset) -> Any:
        # todo this is really horrible, need to improve
        dim = None
        if isinstance(da_ds, xr.Dataset):
            dim = list(da_ds.keys())[0]
            da = da_ds[dim]
        else:
            da = da_ds

        for k in da.coords.keys():
            dim = k
            break
        if dim is None:
            return da_ds.values.squeeze().item()
        return da.expand_dims(dim).values[0]

    def ds_to_container(
        self, dataset: xr.Dataset, result_var: Parameter, container, **kwargs
    ) -> Any:
        val = self.zero_dim_da_to_val(dataset[result_var.name])
        if isinstance(result_var, ResultReference):
            ref = self.object_index[val]
            val = ref.obj
            if ref.container is not None:
                return ref.container(val, **kwargs)
        if container is not None:
            return container(val, styles={"background": "white"}, **kwargs)
        return val

    def to_panes(
        self, result_var: Parameter = None, target_dimension: int = 0, container=None, **kwargs
    ) -> Optional[pn.pane.panel]:
        if container is None:
            container = pn.pane.panel
        return self.map_plot_panes(
            partial(self.ds_to_container, container=container),
            hv_dataset=self.to_hv_dataset(ReduceType.SQUEEZE),
            target_dimension=target_dimension,
            result_var=result_var,
            result_types=PANEL_TYPES,
            **kwargs,
        )

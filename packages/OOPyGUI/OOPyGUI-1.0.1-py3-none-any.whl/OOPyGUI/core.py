from __future__ import annotations
from typing import Any, List, Tuple, Callable
from functools import partial
import dearpygui.dearpygui as dpg


def dpg_setup_start():
    dpg.create_context()
    dpg.setup_dearpygui()


def dpg_setup_finish():
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


class Item:
    add_item_func: Callable = lambda: None

    def __init__(self):
        self.add_item_func = self.__class__.add_item_func
        self.id = None
        self.parent = None
        self.window = None

    def add(self, item: Item):
        item.accept_add(self)
    
    def accept_add(self, parent: Item):
        self.parent = parent

        prev_parent = parent
        while prev_parent and not isinstance(parent, Window):
            prev_parent = prev_parent.parent
        
        if isinstance(prev_parent, Window):
            self.window = prev_parent
        
        self.id = self.add_item_func(parent=parent.id, user_data=self.window)

    def remove(self):
        dpg.delete_item(self.id)
    
    @property
    def visible(self):
        return dpg.is_item_visible(self.id)
    
    @visible.setter
    def visible(self, value: bool):
        if value:
            dpg.show_item(self.id)
        else:
            dpg.hide_item(self.id)
    
    @property
    def label(self):
        return dpg.get_item_label(self.id)
    
    @label.setter
    def label(self, value: str):
        dpg.set_item_label(self.id, value)

    @property
    def pos(self):
        return dpg.get_item_pos(self.id)
    
    @pos.setter
    def pos(self, value: List[float]):
        dpg.set_item_pos(self.id, value)
    
    @property
    def width(self):
        return dpg.get_item_width(self.id)

    @width.setter
    def width(self, value: int):
        dpg.set_item_width(self.id, value)

    @property
    def height(self):
        return dpg.get_item_height(self.id)
    
    @height.setter
    def height(self, value: int):
        dpg.set_item_height(self.id, value)
    
    @property
    def indent(self):
        return dpg.get_item_indent(self.id)
    
    @indent.setter
    def indent(self, value: int):
        dpg.set_item_indent(self.id, value)

    
class ViewportMetaClass(type):
    @property
    def title(cls):
        return dpg.get_viewport_title()
    
    @title.setter
    def title(cls, value: str):
        dpg.set_viewport_title(value)
    
    @property
    def width(cls):
        return dpg.get_viewport_width()
    
    @width.setter
    def width(cls, value: int):
        dpg.set_viewport_width(value)
    
    @property
    def height(cls):
        return dpg.get_viewport_height()
    
    @height.setter
    def height(cls, value: int):
        dpg.set_viewport_height(value)
    
    @property
    def pos(cls):
        return dpg.get_viewport_pos()

    @pos.setter
    def pos(cls, value: List[float]):
        dpg.set_viewport_pos(value)

    @property
    def x_pos(cls):
        return dpg.get_viewport_pos()[0]
    
    @x_pos.setter
    def x_pos(cls, value: int):
        dpg.set_viewport_pos(value, cls.y_pos)
    
    @property
    def y_pos(cls):
        return dpg.get_viewport_pos()[1]
    
    @y_pos.setter
    def y_pos(cls, value: int):
        dpg.set_viewport_pos(cls.x_pos, value)
    
    @property
    def min_width(cls):
        return dpg.get_viewport_min_width()
    
    @min_width.setter
    def min_width(cls, value: int):
        dpg.set_viewport_min_width(value)
    
    @property
    def max_width(cls):
        return dpg.get_viewport_max_width()
    
    @max_width.setter
    def max_width(cls, value: int):
        dpg.set_viewport_max_width(value)
    
    @property
    def min_height(cls):
        return dpg.get_viewport_min_height()
    
    @min_height.setter
    def min_height(cls, value: int):
        dpg.set_viewport_min_height(value)
    
    @property
    def max_height(cls):
        return dpg.get_viewport_max_height()
    
    @max_height.setter
    def max_height(cls, value: int):
        dpg.set_viewport_max_height(value)
    
    @property
    def resizable(cls):
        return dpg.is_viewport_resizable()
    
    @resizable.setter
    def resizable(cls, value: bool):
        dpg.set_viewport_resizable(value)
    
    @property
    def vsync(cls):
        return dpg.is_viewport_vsync_on()
    
    @vsync.setter
    def vsync(cls, value: bool):
        dpg.set_viewport_vsync(value)
    
    @property
    def always_on_top(cls):
        return dpg.is_viewport_always_top()
    
    @always_on_top.setter
    def always_on_top(cls, value: bool):
        dpg.set_viewport_always_top(value)
    
    @property
    def decorated(cls):
        return dpg.is_viewport_decorated()
    
    @decorated.setter
    def decorated(cls, value: bool):
        dpg.set_viewport_decorated(value)
    
    @property
    def clear_color(cls):
        return dpg.get_viewport_clear_color()
    
    @clear_color.setter
    def clear_color(cls, value: List[float] | Tuple[float, ...]):
        dpg.set_viewport_clear_color(value)


class Viewport(metaclass=ViewportMetaClass):
    @classmethod
    def create(
        cls,
        title: str = 'Title', small_icon: str = '', large_icon: str = '',
        width: int = 1280, height: int = 800, x_pos: int = 0, y_pos: int = 0,
        min_width: int = 250, max_width: int = 10000, min_height: int = 250, max_height: int = 10000,
        resizable: bool = True, vsync: bool = True, always_on_top: bool = False,
        decorated: bool = True, clear_color: List[float] | Tuple[float, ...] = (0, 0, 0, 255),
        disable_close: bool = False
    ):
        dpg.create_viewport(
            title=title, small_icon=small_icon, large_icon=large_icon,
            width=width, height=height, x_pos=x_pos, y_pos=y_pos,
            min_width=min_width, max_width=max_width, min_height=min_height, max_height=max_height,
            resizable=resizable, vsync=vsync, always_on_top=always_on_top,
            decorated=decorated, clear_color=clear_color, disable_close=disable_close
        )
    
    @classmethod
    def add(cls, window: Window, name: str | None = None):
        window.accept_add()
        if name:
            setattr(cls, name, window)
    
    @classmethod
    def maximize(cls):
        dpg.maximize_viewport()

    @classmethod
    def set_primary_window(cls, window: Window):
        dpg.set_primary_window(window.id, True)
        
    @classmethod
    def set_small_icon(cls, icon: str = ''):
        dpg.set_viewport_small_icon(icon)
    
    @classmethod
    def set_large_icon(cls, icon: str = ''):
        dpg.set_viewport_large_icon(icon)


class CommonItem(Item):
    def __init__(self, label: str | None = None, indent: int = -1, show: bool = True, pos: List[int] | Tuple[int] = (0, 0)):
        super().__init__()
        self.add_item_func = partial(self.add_item_func, label=label, indent=indent, show=show, pos=pos)


class FixedHeightItemMixin:
    def __init__(self, width: int = 0):
        self.add_item_func = partial(self.add_item_func, width=width)


class FixedWidthItemMixin:
    def __init__(self, height: int = 0):
        self.add_item_func = partial(self.add_item_func, height=height)


class AnyDimensionsItemMixin:
    def __init__(self, width: int = 0, height: int = 0):
        self.add_item_func = partial(self.add_item_func, width=width, height=height)


class ContainableItemMixin:
    def __init__(self, before: Item | None = None):
        before = 0 if before is None else before.id
        self.add_item_func = partial(self.add_item_func, before=before)


class TrackableItemMixin:
    def __init__(self, tracked: bool = False, track_offset: float = 0.5):
        self.add_item_func = partial(self.add_item_func, tracked=tracked, track_offset=track_offset)
    
    @property
    def tracked(self):
        return dpg.is_item_tracked(self.id)
    
    @tracked.setter
    def tracked(self, value: bool):
        if value:
            dpg.track_item(self.id)
        else:
            dpg.untrack_item(self.id)
    
    @property
    def track_offset(self):
        return dpg.get_item_track_offset(self.id)
    
    @track_offset.setter
    def track_offset(self, value: float):
        dpg.set_item_track_offset(self.id, value)


class CallbackableItemMixin:
    def __init__(self, callback: Callable | None = None):
        self.add_item_func = partial(self.add_item_func, callback=callback)
    
    @property
    def callback(self):
        return dpg.get_item_callback(self.id)
    
    @callback.setter
    def callback(self, value: Callable):
        dpg.set_item_callback(self.id, value)


class EnablableItemMixin:
    def __init__(self, enabled: bool = True):
        self.add_item_func = partial(self.add_item_func, enabled=enabled)
    
    @property
    def enabled(self):
        return dpg.is_item_enabled(self.id)
    
    @enabled.setter
    def enabled(self, value: bool):
        if value:
            dpg.enable_item(self.id)
        else:
            dpg.disable_item(self.id)


class DragDropItemMixin:
    def __init__(self, drag_callback: Callable | None, drop_callback: Callable | None):
        self.add_item_func = partial(self.add_item_func, drag_callback=drag_callback, drop_callback=drop_callback)
    
    @property
    def drag_callback(self):
        return dpg.get_item_drag_callback(self.id)
    
    @drag_callback.setter
    def drag_callback(self, value: Callable):
        dpg.set_item_drag_callback(self.id, value)
    
    @property
    def drop_callback(self):
        return dpg.get_item_drop_callback(self.id)
    
    @drop_callback.setter
    def drop_callback(self, value: Callable):
        dpg.set_item_drop_callback(self.id, value)


class FilterableItemMixin:
    def __init__(self, filter_key: str = ''):
        self.add_item_func = partial(self.add_item_func, filter_key=filter_key)


class SourcedItemMixin:
    def __init__(self, source: Item | None = None):
        source = 0 if source is None else source.id
        self.add_item_func = partial(self.add_item_func, source=source)
    
    @property
    def source(self):
        return dpg.get_item_source(self.id)
    
    @source.setter
    def source(self, value: Item):
        dpg.set_item_source(self.id, value.id)


class DefaultValueItemMixin:
    def __init__(self, default_value: Any):
        self.add_item_func = partial(self.add_item_func, default_value=default_value)


class RangedItemMixin:
    def __init__(self, min_value: float = 0, max_value: float = 100):
        self.add_item_func = partial(self.add_item_func, min_value=min_value, max_value=max_value)


class ListItemMixin:
    def __init__(self, items: List[str] | Tuple[str] = ()):
        self.add_item_func = partial(self.add_item_func, items=items)


class Window(CommonItem, AnyDimensionsItemMixin):
    add_item_func = dpg.add_window

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        show: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        delay_search: bool = True,
        min_size: List[int] | Tuple[int] = (300, 300),
        max_size: List[int] | Tuple[int] = (30_000, 30_000),
        menubar: bool = False,
        collapsed: bool = False,
        autosize: bool = False,
        no_resize: bool = False,
        no_title_bar: bool = False,
        no_move: bool = False,
        no_scrollbar: bool = False,
        no_collapse: bool = False,
        horizontal_scrollbar: bool = False,
        no_focus_on_appearing: bool = False,
        no_bring_to_front_on_focus: bool = False,
        no_close: bool = False,
        no_background: bool = False,
        modal: bool = False,
        popup: bool = False,
        no_saved_settings: bool = False,
        no_open_over_existing_popup: bool = True,
        no_scroll_with_mouse: bool = False,
        on_close: Callable | None = None
    ):
        super().__init__(label, indent, show, pos)
        AnyDimensionsItemMixin.__init__(self, width, height)

        self.add_item_func = partial(
            self.add_item_func,
            delay_search=delay_search, min_size=min_size, max_size=max_size,
            menubar=menubar, collapsed=collapsed, autosize=autosize, no_resize=no_resize,
            no_title_bar=no_title_bar, no_move=no_move, no_scrollbar=no_scrollbar,
            no_collapse=no_collapse, horizontal_scrollbar=horizontal_scrollbar,
            no_focus_on_appearing=no_focus_on_appearing, no_bring_to_front_on_focus=no_bring_to_front_on_focus,
            no_close=no_close, no_background=no_background, modal=modal, popup=popup, no_saved_settings=no_saved_settings,
            no_open_over_existing_popup=no_open_over_existing_popup, no_scroll_with_mouse=no_scroll_with_mouse,
            on_close=on_close
        )
    
    def add(self, item: Item, name: str | None = None):
        super().add(item)
        
        if name:
            setattr(self, name, item)

    def accept_add(self):
        self.id = self.add_item_func()


class Text(
    CommonItem, ContainableItemMixin, SourcedItemMixin,
    DragDropItemMixin, FilterableItemMixin, TrackableItemMixin
):
    add_item_func = dpg.add_text

    def __init__(
        self,
        value: str = '',
        label: str | None = None,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        wrap: int = -1,
        bullet: bool = False,
        color: List[int] | Tuple[int, ...] = (-255, 0, 0, 255),
        show_label: bool = False
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        SourcedItemMixin.__init__(self, source)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        FilterableItemMixin.__init__(self, filter_key)
        TrackableItemMixin.__init__(self, tracked, track_offset)

        self.add_item_func = partial(self.add_item_func,
            default_value=value, show_label=show_label, wrap=wrap, bullet=bullet, color=color
        )


class Button(
    CommonItem, ContainableItemMixin, AnyDimensionsItemMixin, TrackableItemMixin,
    EnablableItemMixin, CallbackableItemMixin, DragDropItemMixin, FilterableItemMixin
):
    add_item_func = dpg.add_button

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        before: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        small: bool = False,
        arrow: bool = False,
        direction: int = 0
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        AnyDimensionsItemMixin.__init__(self, width, height)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        FilterableItemMixin.__init__(self, filter_key)

        self.add_item_func = partial(self.add_item_func, small=small, arrow=arrow, direction=direction)


class Checkbox(
    CommonItem, ContainableItemMixin, EnablableItemMixin, CallbackableItemMixin, DragDropItemMixin,
    TrackableItemMixin, FilterableItemMixin, SourcedItemMixin, DefaultValueItemMixin
):
    add_item_func = dpg.add_checkbox

    def __init__(
        self,
        label: str | None = None,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: bool = False
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        FilterableItemMixin.__init__(self, filter_key)
        SourcedItemMixin.__init__(self, source)
        DefaultValueItemMixin.__init__(self, default_value)


class Slider(
    CommonItem, ContainableItemMixin, AnyDimensionsItemMixin, EnablableItemMixin, CallbackableItemMixin,
    TrackableItemMixin, DragDropItemMixin, FilterableItemMixin, SourcedItemMixin, DefaultValueItemMixin, RangedItemMixin
):
    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: float = 0.0,
        min_value: float = 0.0,
        max_value: float = 100.0,
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        AnyDimensionsItemMixin.__init__(self, width, height)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        FilterableItemMixin.__init__(self, filter_key)
        SourcedItemMixin.__init__(self, source)
        DefaultValueItemMixin.__init__(self, default_value)
        RangedItemMixin.__init__(self, min_value, max_value)


class LinearSlider(Slider):
    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: Any = 0.0,
        vertical: bool = False,
        no_input: bool = False,
        clamped: bool = False,
        min_value: Any = 0.0,
        max_value: Any = 100.0,
        format: str ='%g'
    ):
        super().__init__(
            label, width, height, indent, before, source, callback, drag_callback, drop_callback,
            show, enabled, pos, filter_key, tracked, track_offset, default_value, min_value, max_value
        )

        self.add_item_func = partial(self.add_item_func, vertical=vertical, no_input=no_input, clamped=clamped, format=format)


class IntLinearSlider(LinearSlider):
    add_item_func = dpg.add_slider_int

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: int = 0,
        vertical: bool = False,
        no_input: bool = False,
        clamped: bool = False,
        min_value: int = 0,
        max_value: int = 100,
        format: str = '%d'
    ):
        super().__init__(
            label, width, height, indent, before, source, callback, drag_callback, drop_callback,
            show, enabled, pos, filter_key, tracked, track_offset, default_value, vertical, no_input,
            clamped, min_value, max_value, format
        )


class RealLinearSlider(LinearSlider):
    add_item_func = dpg.add_slider_float

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: float = 0.0,
        vertical: bool = False,
        no_input: bool = False,
        clamped: bool = False,
        min_value: float = 0.0,
        max_value: float = 100.0,
        format: str = '%.3f'
    ):
        super().__init__(
            label, width, height, indent, before, source, callback, drag_callback, drop_callback,
            show, enabled, pos, filter_key, tracked, track_offset, default_value, vertical, no_input,
            clamped, min_value, max_value, format
        )


class FloatLinearSlider(RealLinearSlider):
    add_item_func = dpg.add_slider_float


class DoubleLinearSlider(RealLinearSlider):
    add_item_func = dpg.add_slider_double


class Knob(Slider):
    add_item_func = dpg.add_knob_float


class RadioGroup(
    CommonItem, ContainableItemMixin, SourcedItemMixin, EnablableItemMixin, CallbackableItemMixin,
    DragDropItemMixin, FilterableItemMixin, TrackableItemMixin, DefaultValueItemMixin, ListItemMixin
):
    add_item_func = dpg.add_radio_button

    def __init__(
        self,
        items: List[str] | Tuple[str] = (),
        label: str | None = None,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: str = '',
        horizontal: bool = False
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        SourcedItemMixin.__init__(self, source)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        FilterableItemMixin.__init__(self, filter_key)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        DefaultValueItemMixin.__init__(self, default_value)
        ListItemMixin.__init__(self, items)

        self.add_item_func = partial(self.add_item_func, horizontal=horizontal)


class ListBox(
    CommonItem, ContainableItemMixin, SourcedItemMixin, EnablableItemMixin, CallbackableItemMixin, FixedHeightItemMixin,
    DragDropItemMixin, FilterableItemMixin, TrackableItemMixin, DefaultValueItemMixin, ListItemMixin
):
    add_item_func = dpg.add_listbox

    def __init__(
        self,
        items: List[str] | Tuple[str] = (),
        num_items_to_show: int = 3,
        label: str | None = None,
        width: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: str = ''
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        SourcedItemMixin.__init__(self, source)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        FixedHeightItemMixin.__init__(self, width)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        FilterableItemMixin.__init__(self, filter_key)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        DefaultValueItemMixin.__init__(self, default_value)
        ListItemMixin.__init__(self, items)

        self.add_item_func = partial(self.add_item_func, num_items=num_items_to_show)


class ComboBox(
    CommonItem, ContainableItemMixin, SourcedItemMixin, EnablableItemMixin, CallbackableItemMixin, FixedHeightItemMixin,
    DragDropItemMixin, FilterableItemMixin, TrackableItemMixin, DefaultValueItemMixin, ListItemMixin
):
    add_item_func = dpg.add_combo

    def __init__(
        self,
        items: List[str] | Tuple[str] = (),
        label: str | None = None,
        width: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: str = '',
        popup_align_left: bool = False,
        no_arrow_button: bool = False,
        no_preview: bool = False,
        height_mode: int = 1
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        SourcedItemMixin.__init__(self, source)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        FixedHeightItemMixin.__init__(self, width)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        FilterableItemMixin.__init__(self, filter_key)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        DefaultValueItemMixin.__init__(self, default_value)
        ListItemMixin.__init__(self, items)

        self.add_item_func = partial(
            self.add_item_func,
            popup_align_left=popup_align_left, no_arrow_button=no_arrow_button,
            no_preview=no_preview, height_mode=height_mode
        )


DropDown = ComboBox


class Input(
    CommonItem, ContainableItemMixin, SourcedItemMixin, EnablableItemMixin, CallbackableItemMixin,
    FixedHeightItemMixin, DragDropItemMixin, FilterableItemMixin, TrackableItemMixin, DefaultValueItemMixin
):
    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: Any = None,
        run_callback_on_enter: bool = False,
        readonly: bool = False
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        SourcedItemMixin.__init__(self, source)
        EnablableItemMixin.__init__(self, enabled)
        CallbackableItemMixin.__init__(self, callback)
        FixedHeightItemMixin.__init__(self, width)
        DragDropItemMixin.__init__(self, drag_callback, drop_callback)
        FilterableItemMixin.__init__(self, filter_key)
        TrackableItemMixin.__init__(self, tracked, track_offset)
        DefaultValueItemMixin.__init__(self, default_value)

        self.add_item_func = partial(self.add_item_func, on_enter=run_callback_on_enter, readonly=readonly)


class NumericInput(Input, RangedItemMixin):
    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: float = 0.0,
        min_value: Any = 0.0,
        max_value: Any = 100.0,
        step: Any = 0.1,
        step_fast: Any = 1.0,
        min_clamped: bool = False,
        max_clamped: bool = False,
        run_callback_on_enter: bool = False,
        readonly: bool = False
    ):
        super().__init__(
            label, width, indent, before, source, callback, drag_callback, drop_callback, show,
            enabled, pos, filter_key, tracked, track_offset, default_value, run_callback_on_enter, readonly
        )
        RangedItemMixin.__init__(self, min_value, max_value)

        self.add_item_func = partial(
            self.add_item_func,
            step=step, step_fast=step_fast,
            min_clamped=min_clamped, max_clamped=max_clamped
        )


class IntInput(NumericInput):
    add_item_func = dpg.add_input_int

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: float = 0.0,
        min_value: int = 0,
        max_value: int = 100,
        step: int = 1,
        step_fast: int = 100,
        min_clamped: bool = False,
        max_clamped: bool = False,
        run_callback_on_enter: bool = False,
        readonly: bool = False
    ):
        super().__init__(
            label, width, indent, before, source, callback, drag_callback, drop_callback, show,
            enabled, pos, filter_key, tracked, track_offset, default_value, min_value, max_value,
            step, step_fast, min_clamped, max_clamped, run_callback_on_enter, readonly
        )


class RealInput(NumericInput):
    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        drag_callback: Callable | None = None,
        drop_callback: Callable | None = None,
        show: bool = True,
        enabled: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        tracked: bool = False,
        track_offset: float = 0.5,
        default_value: float = 0.0,
        format: str = '%.3f',
        min_value: int = 0,
        max_value: int = 100,
        step: int = 1,
        step_fast: int = 100,
        min_clamped: bool = False,
        max_clamped: bool = False,
        run_callback_on_enter: bool = False,
        readonly: bool = False
    ):
        super().__init__(
            label, width, indent, before, source, callback, drag_callback, drop_callback, show,
            enabled, pos, filter_key, tracked, track_offset, default_value, min_value, max_value,
            step, step_fast, min_clamped, max_clamped, run_callback_on_enter, readonly
        )

        self.add_item_func = partial(self.add_item_func, format=format)


class FloatInput(RealInput):
    add_item_func = dpg.add_input_float


class DoubleInput(RealInput):
    add_item_func = dpg.add_input_double


class TableCell(Item, FixedWidthItemMixin, ContainableItemMixin, FilterableItemMixin):
    add_item_func = dpg.add_table_cell

    def __init__(self, label: str | None = None, height: int = 0, before: Item | None = None, show: bool = True, filter_key: str = ''):
        super().__init__()
        FixedWidthItemMixin.__init__(self, height)
        ContainableItemMixin.__init__(self, before)
        FilterableItemMixin.__init__(self, filter_key)

        self.add_item_func = partial(self.add_item_func, label=label, show=show)


class TableColumn(Item, FixedHeightItemMixin, ContainableItemMixin):
    add_item_func = dpg.add_table_column

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        before: Item | None = None,
        show: bool = True,
        enabled: bool = True,
        init_width_or_weight: float = 0.0,
        default_hide: bool = False,
        default_sort: bool = False,
        width_stretch: bool = False,
        width_fixed: bool = False,
        no_resize: bool = False,
        no_reorder: bool = False,
        no_hide: bool = False,
        no_clip: bool = False,
        no_sort: bool = False,
        no_sort_ascending: bool = False,
        no_sort_descending: bool = False,
        no_header_width: bool = False,
        prefer_sort_ascending: bool = True,
        prefer_sort_descending: bool = False,
        indent_enable: bool = False,
        indent_disable: bool = False,
    ):
        super().__init__()
        FixedHeightItemMixin.__init__(self, width)
        ContainableItemMixin.__init__(self, before)

        self.add_item_func = partial(
            self.add_item_func,
            label=label, show=show, enabled=enabled,
            init_width_or_weight=init_width_or_weight, default_hide=default_hide, default_sort=default_sort,
            width_stretch=width_stretch, width_fixed=width_fixed, no_resize=no_resize, no_reorder=no_reorder,
            no_hide=no_hide, no_clip=no_clip, no_sort=no_sort, no_sort_ascending=no_sort_ascending,
            no_sort_descending=no_sort_descending, no_header_width=no_header_width, prefer_sort_ascending=prefer_sort_ascending,
            prefer_sort_descending=prefer_sort_descending, indent_enable=indent_enable, indent_disable=indent_disable
        )


class TableRow(Item, FixedWidthItemMixin, ContainableItemMixin, FilterableItemMixin):
    add_item_func = dpg.add_table_row

    def __init__(self, label: str | None = None, height: int = 0, before: Item | None = None, show: bool = True, filter_key: str = ''):
        super().__init__()
        FixedWidthItemMixin.__init__(self, height)
        ContainableItemMixin.__init__(self, before)
        FilterableItemMixin.__init__(self, filter_key)

        self.add_item_func = partial(self.add_item_func, label=label, show=show)


class Table(CommonItem, ContainableItemMixin, AnyDimensionsItemMixin, CallbackableItemMixin, SourcedItemMixin, FilterableItemMixin):
    add_item_func = dpg.add_table

    def __init__(
        self,
        label: str | None = None,
        width: int = 0,
        height: int = 0,
        indent: int = -1,
        before: Item | None = None,
        source: Item | None = None,
        callback: Callable | None = None,
        show: bool = True,
        pos: List[int] | Tuple[int] = (0, 0),
        filter_key: str = '',
        delay_search: bool = False,
        show_headers: bool = True,
        clipper: bool = False,
        inner_width: int = 0,
        policy: int = 0,
        freeze_rows: int = 0,
        freeze_columns: int = 0,
        sort_multi: bool = False,
        sort_tristate: bool = False,
        resizable: bool = False,
        reorderable: bool = False,
        hideable: bool = False,
        sortable: bool = False,
        context_menu_in_body: bool = False,
        row_background: bool = False,
        borders_innerH: bool = False,
        borders_outerH: bool = False,
        borders_innerV: bool = False,
        borders_outerV: bool = False,
        no_host_extendX: bool = False,
        no_host_extendY: bool = False,
        no_keep_columns_visible: bool = False,
        precise_widths: bool = False,
        no_clip: bool = False,
        pad_outerX: bool = False,
        no_pad_outerX: bool = False,
        no_pad_innerX: bool = False,
        scrollX: bool = False,
        scrollY: bool = False,
        no_saved_settings: bool = False
    ):
        super().__init__(label, indent, show, pos)
        ContainableItemMixin.__init__(self, before)
        AnyDimensionsItemMixin.__init__(self, width, height)
        CallbackableItemMixin.__init__(self, callback)
        SourcedItemMixin.__init__(self, source)
        FilterableItemMixin.__init__(self, filter_key)

        self.add_item_func = partial(
            self.add_item_func,
            callback=callback, delay_search=delay_search, header_row=show_headers, clipper=clipper,
            inner_width=inner_width, policy=policy, freeze_rows=freeze_rows, freeze_columns=freeze_columns,
            sort_multi=sort_multi, sort_tristate=sort_tristate, resizable=resizable, reorderable=reorderable,
            hideable=hideable, sortable=sortable, context_menu_in_body=context_menu_in_body,
            row_background=row_background, borders_innerH=borders_innerH, borders_outerH=borders_outerH,
            borders_innerV=borders_innerV, borders_outerV=borders_outerV, no_host_extendX=no_host_extendX,
            no_host_extendY=no_host_extendY, no_keep_columns_visible=no_keep_columns_visible,
            precise_widths=precise_widths, no_clip=no_clip, pad_outerX=pad_outerX, no_pad_outerX=no_pad_outerX,
            no_pad_innerX=no_pad_innerX, scrollX=scrollX, scrollY=scrollY, no_saved_settings=no_saved_settings
        )
    
    def add_row(self, row: TableRow):
        self.add(row)
    
    def add_column(self, column: TableColumn):
        self.add(column)
    
    def delete_row(self, row: TableRow):
        row.remove()
    
    def delete_column(self, column: TableColumn):
        column.remove()
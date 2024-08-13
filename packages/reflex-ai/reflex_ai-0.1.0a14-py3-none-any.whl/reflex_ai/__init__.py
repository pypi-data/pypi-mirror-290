"""The local Reflex agent."""

import inspect
import os
import types
from types import FunctionType

import reflex as rx


def enable(app: rx.App):
    """Enable the agent on an app.

    Args:
        app: The app to enable the agent on.

    Note:
        For now, this must be called before add_page is called as
        we override the add_page method.
    """

    from .selection import clickable
    from .toolbar import playground

    # The base path is the directory where the app is defined.
    caller_frame = inspect.stack()[1]
    caller_path = caller_frame.filename
    base_paths = [os.path.dirname(caller_path)]

    def add_page(self, component, *args, **kwargs):
        if not isinstance(component, FunctionType):
            # Skip if the component is not a function.
            return
        route = kwargs.pop("route", rx.utils.format.format_route(component.__name__))

        rx.App.add_page(self, component, *args, route=route, **kwargs)
        rx.App.add_page(
            self,
            clickable(base_paths=base_paths)(lambda: playground(component)),
            route=f"/{route}/edit",
        )

    app.add_page = types.MethodType(add_page, app)

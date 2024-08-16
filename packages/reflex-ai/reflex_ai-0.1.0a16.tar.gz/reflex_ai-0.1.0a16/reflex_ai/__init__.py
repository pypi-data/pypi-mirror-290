"""The local Reflex agent."""

from contextlib import asynccontextmanager
import importlib
import inspect
import os
from pathlib import Path
import re
import shutil
import tempfile
import types
from types import FunctionType

import reflex as rx

from . import paths


class EditableState(rx.State):
    """Rewrite rx.State imports in copied modules to this new class to avoid conflicts."""

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the state.

        Returns:
            The name of the state.
        """
        module = cls.__module__.replace(".", "___")
        return rx.utils.format.to_snake_case(f"Editable___{module}___{cls.__name__}")


def enable(app: rx.App):
    """Enable the agent on an app.

    Args:
        app: The app to enable the agent on.

    Note:
        For now, this must be called before add_page is called as
        we override the add_page method.
    """
    from reflex.utils.exec import is_prod_mode

    # Skip if in production mode.
    if is_prod_mode():
        return

    from .selection import clickable
    from .toolbar import playground

    # The base path is the directory where the app is defined.
    caller_frame = inspect.stack()[1]
    caller_path = caller_frame.filename
    base_paths = [Path(caller_path).parent]

    # Copy the app directory to a temporary path for modifications
    #tmp_root_path = Path(tempfile.mkdtemp(dir=base_paths[0]))
    tmp_root_path = base_paths[0] / "reflex_ai_tmp"
    if not tmp_root_path.exists():
        shutil.copytree(
            base_paths[0].parent,
            tmp_root_path,
            ignore=lambda _, names: [tmp_root_path.name, ".web", "assets", "__pycache__"],
            dirs_exist_ok=True,
        )

    @asynccontextmanager
    async def cleanup_tmp_dir():
        yield
        # Can't clean up here because hot reload will delete the diff
        # print("cleaning up", tmp_root_path)
        # shutil.rmtree(tmp_root_path)
    app.register_lifespan_task(cleanup_tmp_dir)
    # app._enable_state()
    paths.base_paths = base_paths
    paths.tmp_root_path = tmp_root_path

    def add_page(self, component, *args, **kwargs):
        if not isinstance(component, FunctionType):
            # Skip if the component is not a function.
            return
        route = kwargs.pop("route", rx.utils.format.format_route(component.__name__))

        rx.App.add_page(self, component, *args, route=route, **kwargs)

        # Determine which module the component came from
        module = inspect.getmodule(component)
        if module is None:
            # Skip if the component does not come from a known module.
            return

        module_path = inspect.getfile(component)
        new_module_path = Path(module_path.replace(str(base_paths[0].parent), str(tmp_root_path)))
        
        # Rewrite `rx.State` base classes to `EditableState` in the copied module
        module_code = new_module_path.read_text().replace("(rx.State)", "(EditableState)")
        # Remove calls to App and add_page
        module_code = re.sub(r"^.*=rx.App\(.*$", "", module_code, flags=re.MULTILINE)
        module_code = re.sub(r"^.*add_page\(.*$", "", module_code, flags=re.MULTILINE)
        module_code = re.sub(r"^.*enable\(app\).*$", "", module_code, flags=re.MULTILINE)
        if "from reflex_ai import EditableState" not in module_code:
            new_module_path.write_text(
                f"from reflex_ai import EditableState\n{module_code}"
            )

        # Import the tmp module
        new_module_path = Path(module_path.replace(str(base_paths[0].parent), str(tmp_root_path)))
        spec = importlib.util.spec_from_file_location(
            "tmp" + module.__name__,
            new_module_path,
        )
        new_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(new_module)
        rx.App.add_page(
            self,
            clickable(base_paths=base_paths)(lambda: playground(getattr(new_module, component.__name__))),
            route=f"/{route}/edit",
        )

    app.add_page = types.MethodType(add_page, app)

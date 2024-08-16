"""The agent that runs on the user's local client."""

import ast
import functools
import importlib
import importlib.util
import inspect
import filecmp
import difflib
from pathlib import Path

import black
from flexai import Agent
from flexai.message import Message, ToolResultMessage
from pydantic import BaseModel
from reflex_ai import paths


# NOTE: using BaseModel here instead of rx.Base due to FastAPI not liking the v1 models
class InternRequest(BaseModel):
    """The request to the AI intern."""

    prompt: str
    selected_code: str
    selected_module: str
    selected_function: str


class InternResponse(BaseModel):
    """The response from the AI intern."""

    request_id: str
    messages: list[Message]


class ToolRequestResponse(BaseModel):
    """The response from the tool to the AI intern."""

    request_id: str
    messages: list[ToolResultMessage]


def get_agent() -> Agent:
    """Get an instance of an intern."""
    return Agent(
        tools=[
            get_function_source,
            create_function,
            update_function,
        ],
    )


@functools.lru_cache
def import_module_from_tmp(module_name: str):
    """Import the module from the scratchpad."""
    module = importlib.import_module(module_name)
    module_file = inspect.getsourcefile(module)
    module_tmp_file = module_file.replace(str(paths.base_paths[0].parent), str(paths.tmp_root_path))
    spec = importlib.util.spec_from_file_location(
        module.__name__,
        module_tmp_file,
    )
    new_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(new_module)
    return new_module

def diff_directories(dir1, dir2):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.
    Returns a dictionary with file paths as keys and their diffs as values.
    """
    print("diffing", dir1, dir2)

    diffs = {}

    def compare_dirs(dcmp):
        for name in dcmp.diff_files:
            if not name.endswith(".py"):
                continue
            file1 = Path(dcmp.left) / name
            file2 = Path(dcmp.right) / name
            with file1.open() as f1, file2.open() as f2:
                f1_lines = f1.read().splitlines()
                f2_lines = f2.read().replace("EditableState", "rx.State").replace("from reflex_ai import rx.State\n", "").splitlines()
                diff = list(difflib.unified_diff(
                    f1_lines,
                    f2_lines,
                    fromfile=str(file1),
                    tofile=str(file2)
                ))
                diffs[file1] = diff
        for sub_dcmp in dcmp.subdirs.values():
            compare_dirs(sub_dcmp)

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    compare_dirs(dirs_cmp)

    return diffs

def directory_diff():
    """Diff the scratchpad and the base directories."""
    return diff_directories(paths.base_paths[0].parent, paths.tmp_root_path)

def get_module_ast(module_name: str) -> ast.Module:
    """Get the AST of a module.

    Args:
        module_name: The name of the module.

    Returns:
        The AST of the module.
    """
    # Import the module
    module = import_module_from_tmp(module_name)

    # Get the source code of the module
    module_file = inspect.getsourcefile(module)
    with open(module_file, "r") as file:
        module_source = file.read()

    # Parse the module source code into an AST
    module_ast = ast.parse(module_source)
    return module_ast


def write_module_source(module_name: str, source_code: str):
    """Write the source code of a module.

    Args:
        module_name: The name of the module.
        source_code: The source code of the module.
    """
    # Import the module.
    module = import_module_from_tmp(module_name)

    # Get the source code of the module.
    module_file = inspect.getsourcefile(module)

    # Format the source code using Black.
    source_code = black.format_str(source_code, mode=black.FileMode())

    # Write the new source code back to the module file.
    with open(module_file, "w") as file:
        file.write(source_code)


def get_function_source(module_name: str, function_name: str) -> str:
    """Get the source code of a function in a module.

    Args:
        module_name: The name of the module.
        function_name: The name of the function.

    Returns:
        The source code of the function.
    """
    # Import the module.
    module = import_module_from_tmp(module_name)

    # Get the function object using its name
    func_obj = getattr(module, function_name)

    # Get the source code of the function
    return inspect.getsource(func_obj)


def update_function(module_name: str, function_name: str, new_code: str):
    """Update the source code of a function in a module.

    Args:
        module_name: The name of the module.
        function_name: The name of the function.
        new_code: The new source code of the function.

    """
    module_ast = get_module_ast(module_name)

    # Parse the new function code and check for multiple function definitions
    new_code_ast = ast.parse(new_code)
    function_defs = [
        node for node in new_code_ast.body if isinstance(node, ast.FunctionDef)
    ]
    if len(function_defs) > 1:
        raise ValueError(
            "New function source must not contain more than one function definition."
        )

    # Define a class to visit and update the target function node
    class FunctionUpdater(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name == function_name:
                # Parse the new function code into an AST and replace the body
                node.body = function_defs[0].body
            return self.generic_visit(node)

    # Transform the AST
    updated_ast = FunctionUpdater().visit(module_ast)

    # Generate the new source code from the updated AST
    new_source_code = ast.unparse(updated_ast)

    # Validate the new source code. This is necessary to ensure the new code is valid Python syntax.
    env = {}
    exec(new_source_code, env, env)
    # Evaluate the new source code to ensure it is valid Python syntax.
    func = env.get(function_name)
    func()

    # Write the new source code back to the module file
    write_module_source(module_name, new_source_code)


def create_function(module_name: str, function_name: str, new_code: str):
    """Create a new component function in the module. Do this to create a new component before using it.

    Args:
        module_name: The name of the module to add the function to.
        function_name: The name of the new function.
        new_code: The source code of the new function.
    """
    module_ast = get_module_ast(module_name)

    # Create a new function definition node from the new code
    new_function_ast = ast.parse(new_code).body[0]

    # Ensure the parsed new code is a function definition
    if not isinstance(new_function_ast, ast.FunctionDef):
        raise ValueError("New code does not define a function.")

    # Update the function name if necessary
    new_function_ast.name = function_name

    # Add the new function to the module's AST
    module_ast.body.append(new_function_ast)

    # Generate the new source code from the updated AST
    new_source_code = ast.unparse(module_ast)
    write_module_source(module_name, new_source_code)

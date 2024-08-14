"""
Analyzing dependencies between apps in a Django project
"""

import ast
from collections import defaultdict
from dataclasses import dataclass
from glob import glob
from typing import Iterator

from django.apps import AppConfig, apps


MAX_DEPTH = 5
DEFAULT_IGNORE_DIRS = ["tests"]


@dataclass
class ModuleRef:
    """
    Module details necessary to build a dependency map
    """

    app_config: AppConfig
    module_name: str
    path: str

    # Implement hashing so that we can use module refs with sets.
    def __hash__(self):
        return hash(self.module_name)


class DependenciesMap(defaultdict):
    """
    Thin wrapper around `defaultdict` with dependencies-specific logic
    """

    def has_cycle(
        self,
        app_config: AppConfig,
        dependency: AppConfig,
        depth: int = 1,
        max_depth: int = MAX_DEPTH,
    ):
        if depth > max_depth:
            return False
        for dependency_of_dependency in self.get(dependency, []):
            if dependency_of_dependency == app_config:
                return True
            if self.has_cycle(app_config, dependency_of_dependency, depth + 1):
                return True
        return False


def get_project_app_configs(base_dir: str) -> list[AppConfig]:
    """
    Return the list of apps that are defined inside the project
    """
    return [
        app_config
        for app_config in apps.get_app_configs()
        if app_config.path.startswith(str(base_dir))
    ]


def is_path_ignored(path: str, ignore_dirs: list[str]) -> bool:
    """
    Return true if the path is inside one of the directories, otherwise false
    """
    for ignore_dir in ignore_dirs:
        if path.startswith(f"{ignore_dir}/"):
            return True
    return False


def iter_python_paths(app_config: AppConfig, ignore_dirs: list[str]) -> Iterator[str]:
    """
    Iterate through paths of all Python files inside the app, excluding given directories
    """
    for path in glob(f"**/*.py", recursive=True, root_dir=app_config.path):
        if not is_path_ignored(path, ignore_dirs):
            yield f"{app_config.path}/{path}"


def iter_module_refs(
    app_config: AppConfig, ignore_dirs: list[str]
) -> Iterator[ModuleRef]:
    """
    Iterate through all module refs from the given app
    """
    for path in iter_python_paths(app_config, ignore_dirs):
        module_name = app_config.name + path[len(app_config.path) :].rstrip(
            ".py"
        ).replace("/", ".")
        yield ModuleRef(app_config, module_name, path)


def find_imported_module_names(path: str) -> set[str]:
    """
    Return the list of model names imported at top level in the Python file
    """
    imported_module_names = set()
    with open(path, "r") as python_file:
        module = ast.parse(python_file.read())
        # Search only the top-level statements
        for node in module.body:
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_module_names.add(node.module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name:
                        imported_module_names.add(alias.name)
    return imported_module_names


def build_dependencies_map(
    base_dir: str, ignore_apps: list[str] = None, ignore_dirs: list[str] = None
) -> DependenciesMap:
    """
    Return a dictionary that maps app configs to configs of their dependencies
    """
    module_refs_by_app: dict[AppConfig, set[ModuleRef]] = defaultdict(set)
    module_refs_by_name: dict[str, ModuleRef] = dict()
    app_configs = get_project_app_configs(base_dir)
    dependencies_map: DependenciesMap[AppConfig, set[AppConfig]] = DependenciesMap(set)

    # Collect and map module refs
    for app_config in app_configs:
        if ignore_apps and app_config.name in ignore_apps:
            continue

        for module_ref in iter_module_refs(app_config, ignore_dirs):
            module_refs_by_app[app_config].add(module_ref)
            module_refs_by_name[module_ref.module_name] = module_ref

    # Find and collect dependencies
    for app_config in app_configs:
        for module_ref in module_refs_by_app[app_config]:
            for imported_module_name in find_imported_module_names(module_ref.path):
                imported_module_ref = module_refs_by_name.get(imported_module_name)
                if imported_module_ref and imported_module_ref.app_config != app_config:
                    dependencies_map[app_config].add(imported_module_ref.app_config)

    return dependencies_map

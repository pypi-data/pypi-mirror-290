from argparse import ArgumentParser
from functools import partial
from operator import attrgetter

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from django_deps.dependencies_map import DEFAULT_IGNORE_DIRS, build_dependencies_map


sorted_by_name = partial(sorted, key=attrgetter("name"))


class Command(BaseCommand):
    """
    Print the list of all project apps and their dependencies

    Any circular dependencies are highlighted in red.
    """

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--base-dir",
            default=settings.BASE_DIR,
            help="Root directory of your Django project, defaults to BASE_DIR.",
        )
        parser.add_argument(
            "--ignore-apps",
            nargs="*",
            default=None,
            help="Project apps to ignore when looking for dependencies.",
        )
        parser.add_argument(
            "--ignore-dirs",
            default=DEFAULT_IGNORE_DIRS,
            help=f"Directories to ignore when looking for dependencies, defaults to {DEFAULT_IGNORE_DIRS}.",
        )
        parser.add_argument(
            "--check",
            action="store_true",
            help="Instead of printing dependencies, only return error when a cycle is found.",
        )

    def handle(self, *args, **options):
        dependencies_map = build_dependencies_map(
            base_dir=options["base_dir"],
            ignore_dirs=options["ignore_dirs"],
            ignore_apps=options["ignore_apps"],
        )
        check = options["check"]
        found_cycles = False
        no_style = lambda text: text

        for app_config, dependencies in dependencies_map.items():
            if not check:
                self.stdout.write(self.style.SUCCESS(app_config.name))

            for dependency in sorted_by_name(dependencies):
                has_cycle = dependencies_map.has_cycle(app_config, dependency)

                if check:
                    if has_cycle:
                        self.stderr.write(
                            f"Found cycle in dependency: {app_config.name} -> {dependency.name}"
                        )
                        found_cycles = True
                else:
                    style = self.style.ERROR if has_cycle else no_style
                    self.stdout.write(style(f"    {dependency.name}"))

        if check and found_cycles:
            raise CommandError("Found cycle(s).")

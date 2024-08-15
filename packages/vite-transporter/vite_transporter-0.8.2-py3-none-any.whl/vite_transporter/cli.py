from .utilities import ArgumentParser
from .utilities import PyProjectConfig
from .utilities import compile_vite_apps
from .utilities import list_vite_apps
from .utilities import load_vite_apps
from .utilities import subparsers


def cli() -> None:
    from . import __version__

    parser = ArgumentParser(prog="vt", add_help=False)
    parser.add_argument(
        "--version", "-v", action="version", version=f"vite-transporter {__version__}"
    )
    parser.add_argument("--help", "-h", action="help")

    subparsers(parser)

    with PyProjectConfig() as pyproject_config:
        vite_apps_found = load_vite_apps(pyproject_config)
        parsed_args = parser.parse_args()

        if hasattr(parsed_args, "compile"):
            compile_vite_apps(pyproject_config, vite_apps_found, parsed_args)

        if hasattr(parsed_args, "list") or hasattr(parsed_args, "ls"):
            list_vite_apps(vite_apps_found)

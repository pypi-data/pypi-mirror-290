import sys

from .utilities import PyProjectConfig
from .utilities import Sprinkles
from .utilities import list_vite_apps
from .utilities import load_vite_apps
from .utilities import pack_vite_apps
from .utilities import print_help
from .utilities import transport_vite_apps
from .utilities import update_vite_apps


def cli() -> None:
    from . import __version__

    available_commands = [
        "vt",
        "pack",
        "transport",
        "staging",
        "development",
        "production",
        "list",
        "ls",
        "update",
        "-h",
        "--help",
        "help",
        "-v",
        "--version",
        "version",
    ]
    arg_list = sys.argv[1:]

    for arg in arg_list:
        if arg not in available_commands:
            print("\n\r" f" {Sprinkles.FAIL}Invalid argument > {arg} <{Sprinkles.END}")
            print_help()
            sys.exit(1)

    with PyProjectConfig() as pyproject_config:
        vite_apps_found = load_vite_apps(pyproject_config)

        if "update" in arg_list:
            update_vite_apps(pyproject_config, vite_apps_found)

            if "transport" not in arg_list or "pack" not in arg_list:
                sys.exit(0)

        if "pack" in arg_list:
            pack_vite_apps(pyproject_config, vite_apps_found, arg_list)

            if "transport" not in arg_list:
                sys.exit(0)

        if "transport" in arg_list:
            transport_vite_apps(pyproject_config, vite_apps_found)
            sys.exit(0)

        if "list" in arg_list or "ls" in arg_list:
            list_vite_apps(vite_apps_found)
            sys.exit(0)

        if "help" in arg_list or "-h" in arg_list or "--help" in arg_list:
            print_help()

        if "version" in arg_list or "-v" in arg_list or "--version" in arg_list:
            print(f"vite-transporter v{__version__}")
            sys.exit(0)

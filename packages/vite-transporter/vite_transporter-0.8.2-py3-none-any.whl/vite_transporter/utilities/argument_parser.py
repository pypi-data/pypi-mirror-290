import argparse
import typing as t

from .sprinkles import Sprinkles


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.vite_apps: t.List[t.Dict[str, t.Any]] = []

    def print_help(self, file: t.Optional[t.IO[str]] = None) -> None:
        print(
            "\n\r"
            "Usage: vt <option>"
            "\n\r\n\r"
            f" {Sprinkles.OKCYAN}list, ls{Sprinkles.END} => List all vite apps in pyproject.toml"
            "\n\r"
            f" {Sprinkles.OKCYAN}compile (-y){Sprinkles.END} => Attempt to compile all vite apps"
            "\n\r"
            f"  | {Sprinkles.OKCYAN}-y{Sprinkles.END} => Accept all prompts while compiling"
            "\n\r"
            f" {Sprinkles.OKCYAN}-h, --help{Sprinkles.END} => Show the help message and exit"
            "\n\r"
            f" {Sprinkles.OKCYAN}-v, --version{Sprinkles.END} => Show the version and exit"
        )
        print("")

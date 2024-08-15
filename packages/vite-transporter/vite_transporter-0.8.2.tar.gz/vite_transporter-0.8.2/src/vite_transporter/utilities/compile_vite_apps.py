import shutil
import subprocess
import sys
import typing as t
from argparse import Namespace

from .pyproject_config import PyProjectConfig
from .sprinkles import Sprinkles


def compile_vite_apps(
        pyproject_config: PyProjectConfig,
        vite_apps_found: t.List[t.Dict[str, t.Any]],
        parsed_args: Namespace,
) -> None:
    compiler(
        pyproject_config,
        vite_apps_found,
        replace=True if hasattr(parsed_args, "y") and parsed_args.y else False,
    )


def compiler(
        pyproject_config: PyProjectConfig,
        vite_apps_found: t.List[t.Dict[str, t.Any]],
        replace: bool = False,
) -> None:
    print("Compiling Vite apps...")
    vt_dir = pyproject_config.cwd / pyproject_config.serve_app / "vite"

    if vt_dir.exists():
        if not replace:
            prompt = input(
                f"Continuing will replace the contents of \n\r"
                f"{vt_dir} \n\r"
                f"Do you want to continue? (Y/n): "
            )
        else:
            prompt = "y"

        if prompt.lower() == "y" or prompt == "":
            for item in vt_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        else:
            print("Operation aborted.")
            sys.exit(0)

    else:
        vt_dir.mkdir()

    for app in vite_apps_found:
        va_path = pyproject_config.cwd / app.get("vite_app", "")
        va_node_modules = va_path / "node_modules"
        va_dist = va_path / "dist"
        va_assets = va_dist / "assets"

        va_vt_path = vt_dir / app.get("vite_app", "")

        if va_dist.exists() and va_dist.is_dir():
            shutil.rmtree(va_dist)

        if not va_vt_path.exists():
            va_vt_path.mkdir()

        if not va_node_modules.exists():
            subprocess.run([pyproject_config.npm_exec, "install"], cwd=va_path)

        subprocess.run([pyproject_config.npx_exec, "vite", "build", "--mode", "production"], cwd=va_path)

        for item in va_assets.iterdir():
            print(
                f"{Sprinkles.OKGREEN}Copying {item.name} to {va_vt_path}{Sprinkles.END}"
            )

            if item.suffix == ".js":
                with open(va_vt_path / item.name, "w") as f:
                    content = item.read_text()
                    f.write(
                        content.replace("assets/", f"--vite--/{app.get('vite_app')}/")
                    )
            else:
                shutil.copy(item, va_vt_path / item.name)

    print("Compilation complete.")

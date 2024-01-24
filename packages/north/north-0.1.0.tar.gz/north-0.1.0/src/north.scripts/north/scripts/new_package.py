import re
import shutil
from argparse import ArgumentParser
from pathlib import Path
from string import Template
from typing import cast

import json5 as json
from north.scripts import project_root

pyproject_template = Template(
    """\
[tool.poetry]
name = "north.${name}"
version = "0.1.0"
description = ""
authors = ["Adam Hitchcock <adam+python@northisup.com>"]
packages = [{ include = "north" }]

[tool.poetry.dependencies]
python = "^3.11"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
)


def insert_into_pyproject_toml(name: str, toml_path: Path):
    toml = (project_root / "pyproject.toml").read_text()

    for func in (
        insert_into_pyproject_packages,
        insert_into_pyproject_dev_dependencies,
    ):
        toml = func(name, toml)

    toml_path.write_text(toml)


def insert_into_pyproject_packages(name: str, toml: str) -> str:
    packages_entry = f'{{ include = "north.{name}", from = "src" }}'
    if packages_entry not in toml:
        finder = re.compile(r"packages = (\[((\n|.)*?)\])", re.MULTILINE)
        found = cast(str, finder.search(toml).group(1))

        packages = {p for _ in found.split("\n") if (p := _.strip(" [],"))}
        packages.add(packages_entry)
        packages = "\n".join(f"    {_}," for _ in sorted(packages))
        toml = finder.sub(f"packages = [\n{packages}\n]", toml)
    return toml


def insert_into_pyproject_dev_dependencies(name: str, toml: str) -> str:
    dev_dependency = f'"north.{name}" = {{ path = "src/north.{name}", develop = true }}'
    if dev_dependency not in toml:
        finder = re.compile(
            r"\[tool.poetry.dev-dependencies\]\n((\n|.)*?)\[", re.MULTILINE
        )
        found = cast(str, finder.search(toml).group(1))
        dependcies = {p for _ in found.split("\n") if (p := _.strip(" [],"))}
        dependcies.add(dev_dependency)

        toml = finder.sub(
            "[tool.poetry.dev-dependencies]\n"
            + "\n".join(sorted(dependcies))
            + "\n\n[",
            toml,
        )
    return toml


def insert_into_vscode_settings(name: str):
    settings_path = project_root / ".vscode/settings.json"
    settings = json.loads(settings_path.read_text())
    settings["python.analysis.extraPaths"] = sorted(
        set(settings["python.analysis.extraPaths"]) | {f"./src/north.{name}"}
    )

    settings_path.write_text(json.dumps(settings, indent=4))


def create_project(name: str, force: bool = False):
    pkg = Path(f"src/north.{name}")
    if force:
        shutil.rmtree(pkg)

    if pkg.exists():
        raise Exception(f"{pkg} already exists")
    (pkg / "north" / name).mkdir(parents=True, exist_ok=False)
    (pkg / "north" / name / "__init__.py").touch()
    (pkg / "pyproject.toml").write_text(pyproject_template.safe_substitute(name=name))

    insert_into_pyproject_toml(name, project_root / "pyproject.toml")
    insert_into_vscode_settings(name)


def main():
    parser = ArgumentParser()
    parser.add_argument("package_name")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    create_project(args.package_name, args.force)


if __name__ == "__main__":
    main()

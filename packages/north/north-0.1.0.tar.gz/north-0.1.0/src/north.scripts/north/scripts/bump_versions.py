from argparse import ArgumentParser
from pathlib import Path

from north.scripts import project_root

_home_trim = len(Path.home().as_posix()) + 1


def find_version(toml_text: str) -> tuple[int, int]:
    version_start = toml_text.find("version = ")
    version_end = toml_text.find("\n", version_start + 1)
    return version_start, version_end


def extract_version(toml_text: str) -> str:
    s, e = find_version(toml_text)
    return toml_text[s + 10 : e].strip('"')


def replace_version(toml_text: str, new_version: str) -> str:
    s, e = find_version(toml_text)
    return toml_text[:s] + f'version = "{new_version}"' + toml_text[e:]


def replace_version_for_path(toml: Path, new_version: str):
    toml_text = toml.read_text()
    new_toml_text = replace_version(toml_text, new_version)

    print(
        f"bumpped from {extract_version(toml_text)} to {extract_version(new_toml_text)} in {toml.as_posix()[_home_trim:]}"
    )
    toml.write_text(new_toml_text)


def bump_version(mode: str, version: str) -> str:
    major, minor, patch = map(int, version.split("."))

    match mode:
        case "new":
            version = version
        case "major":
            version = f"{major + 1}.0.0"
        case "minor":
            version = f"{major}.{minor + 1}.0"
        case "patch":
            version = f"{major}.{minor}.{patch + 1}"
    return version


def main():
    parser = ArgumentParser()
    parser.add_argument("mode", choices=("new", "major", "minor", "patch"))
    args, _unparsed = parser.parse_known_args()

    root_version = extract_version((project_root / "pyproject.toml").read_text())
    match args.mode:
        case "new":
            parser.add_argument("version")
            args = parser.parse_args()
            new_version = bump_version("new", args.version)
            print(f"setting {args.mode} version {new_version}")

        case "major" | "minor" | "patch":
            new_version = bump_version(args.mode, root_version)
            print(f"bumping {args.mode} version {root_version} to {new_version}")
        case _:
            raise Exception("unreachable")

    for toml in project_root.glob("**/pyproject.toml"):
        replace_version_for_path(toml, new_version)


if __name__ == "__main__":
    main()

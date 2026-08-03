"""Solution 01.4 — Environment diagnostic tool.

Keep this. Run it any time an import does something you did not expect.

    python ex04_env_report_solution.py
    python ex04_env_report_solution.py --json
"""

from __future__ import annotations

import json
import site
import sys
from importlib import metadata
from pathlib import Path

BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def interpreter_info() -> dict[str, str]:
    """TODO 1 solved."""
    v = sys.version_info
    return {
        "implementation": sys.implementation.name,
        "version": f"{v.major}.{v.minor}.{v.micro}",
        "executable": sys.executable,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
    }


def in_virtualenv() -> bool:
    """TODO 2 solved.

    sys.prefix is where THIS interpreter's libraries live. sys.base_prefix is
    where the interpreter it was created from lives. In a venv they differ; in
    a system interpreter they are identical. This is the definition, straight
    out of PEP 405.

    Why not check the VIRTUAL_ENV environment variable? Because it is set by
    the `activate` shell script, not by the interpreter. It is:
      - absent when you invoke .venv/bin/python directly without activating,
        even though you ARE in the venv;
      - stale and misleading when you activate an env and then invoke a
        different interpreter by absolute path;
      - absent when a tool (tox, uv run, an IDE) runs the venv interpreter
        directly, which is the common case in CI.
    The prefix comparison asks the interpreter about itself and is always true.
    """
    return sys.prefix != sys.base_prefix


def site_packages_dirs() -> list[str]:
    try:
        return list(site.getsitepackages())
    except AttributeError:  # some embedded builds
        return []


def installed_count() -> int:
    """TODO 5 solved."""
    return sum(1 for _ in metadata.distributions())


def check_shadowing(directory: Path | None = None) -> list[tuple[str, str]]:
    """TODO 4 solved. The most valuable function here.

    Returns a list of (filename, shadowed_module) for every .py file in the
    directory whose stem collides with a standard library module name.

    sys.stdlib_module_names (3.10+) is a frozenset of every stdlib module name
    for this interpreter, including ones not currently imported. That makes it
    strictly better than iterating sys.modules, which only sees what has
    already been loaded.
    """
    directory = directory or Path.cwd()
    found: list[tuple[str, str]] = []
    for py in sorted(directory.glob("*.py")):
        if py.stem in sys.stdlib_module_names:
            found.append((py.name, py.stem))
    # Packages shadow too: a directory with an __init__.py counts.
    for pkg in sorted(p for p in directory.iterdir() if p.is_dir()):
        if (pkg / "__init__.py").exists() and pkg.name in sys.stdlib_module_names:
            found.append((f"{pkg.name}/", pkg.name))
    return found


def render_text() -> int:
    info = interpreter_info()

    print(f"\n{BOLD}Interpreter{RESET}")
    print(f"  implementation : {info['implementation']} {info['version']}")
    print(f"  executable     : {info['executable']}")
    print(f"  prefix         : {info['prefix']}")
    print(f"  base_prefix    : {info['base_prefix']}")

    print(f"\n{BOLD}Environment{RESET}")
    if in_virtualenv():
        print(f"  virtualenv     : {GREEN}YES{RESET} ({Path(sys.prefix).name})")
    else:
        print(f"  virtualenv     : {RED}NO - you are using the system interpreter{RESET}")
        print(f"{DIM}                   installs will go system-wide; create a venv{RESET}")
    for sp in site_packages_dirs():
        print(f"  site-packages  : {sp}")
    print(f"  installed      : {installed_count()} distributions")

    print(f"\n{BOLD}Import path (sys.path){RESET}")
    for i, p in enumerate(sys.path):
        note = ""
        if i == 0:
            note = f"{DIM}  <- searched FIRST: script dir / cwd{RESET}"
        print(f"  [{i}] {p or '(empty = cwd)'}{note}")

    print(f"\n{BOLD}Shadowing check{RESET}")
    clashes = check_shadowing()
    if not clashes:
        print(f"  {GREEN}OK{RESET}   no local files shadow a standard library module")
        return 0
    for filename, module in clashes:
        print(f"  {RED}WARN{RESET} {filename} shadows the stdlib module '{module}'")
    print(f"{DIM}       rename these files, then delete __pycache__{RESET}")
    return 1


def render_json() -> int:
    clashes = check_shadowing()
    payload = {
        "interpreter": interpreter_info(),
        "virtualenv": in_virtualenv(),
        "site_packages": site_packages_dirs(),
        "installed_distributions": installed_count(),
        "sys_path": sys.path,
        "shadowing": [{"file": f, "shadows": m} for f, m in clashes],
    }
    print(json.dumps(payload, indent=2))
    return 1 if clashes else 0


def main(argv: list[str]) -> int:
    """TODO 6 solved: non-zero exit on shadowing makes this usable in CI."""
    if "--json" in argv:
        return render_json()
    return render_text()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

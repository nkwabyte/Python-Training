"""The ONLY module allowed to print, read argv, or choose an exit code.

Verify that claim at any time with:

    grep -rn "print(\\|sys.exit\\|argparse\\|os.environ" src/inventory/ \\
        --include="*.py" | grep -v cli.py

It should return nothing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from inventory import __version__, operations, reporting, serialization
from inventory.errors import InventoryError
from inventory.models import Item
from inventory.store import Store

DEFAULT_FILE = Path.home() / ".local" / "share" / "inventory" / "inventory.json"

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_DATA = 3


# --- output helpers -----------------------------------------------------------
def out(text: str) -> None:
    print(text)                                   # DATA goes to stdout


def err(text: str) -> None:
    print(text, file=sys.stderr)                  # MESSAGES go to stderr
    # This split is what makes `inv list | grep widget` work and
    # `inv list 2>/dev/null` show only data. Printing errors to stdout
    # corrupts every pipeline the tool is used in.


def render_items(items: list[Item], as_json: bool) -> str:
    if as_json:
        return serialization.to_json(items)
    if not items:
        return "no items"
    w_sku = max(len("SKU"), max(len(i.sku) for i in items))
    w_name = max(len("NAME"), max(len(i.name) for i in items))
    lines = [f"{'SKU':<{w_sku}}  {'NAME':<{w_name}}  {'QTY':>5}  "
             f"{'PRICE':>10}  {'VALUE':>12}  LOC   TAGS"]
    for i in items:
        lines.append(
            f"{i.sku:<{w_sku}}  {i.name:<{w_name}}  {i.quantity:>5}  "
            f"{str(i.unit_price):>10}  {str(i.total_value):>12}  "
            f"{i.location:<5} {','.join(i.tags)}"
        )
    return "\n".join(lines)


# --- command handlers ---------------------------------------------------------
def cmd_add(store: Store, args: argparse.Namespace) -> int:
    tags = tuple(t.strip() for t in (args.tags or "").split(",") if t.strip())
    item, _change = operations.add_item(
        store, args.sku, args.name, quantity=args.qty, price=args.price,
        location=args.location, tags=tags,
    )
    err(f"added {item.sku}: {item.name} x{item.quantity} @ {item.location}")
    return EXIT_OK


def cmd_list(store: Store, args: argparse.Namespace) -> int:
    items = operations.filtered(
        store, location_prefix=args.location, tag=args.tag,
        min_qty=args.min_qty, max_qty=args.max_qty,
        sort_by=args.sort, descending=args.desc, limit=args.limit,
    )
    out(render_items(items, args.json))
    return EXIT_OK


def cmd_search(store: Store, args: argparse.Namespace) -> int:
    fields = tuple(f.strip() for f in args.in_fields.split(",") if f.strip())
    items = operations.search(store, args.query, fields)
    out(render_items(items, args.json))
    return EXIT_OK if items else EXIT_FAILED


def cmd_move(store: Store, args: argparse.Namespace) -> int:
    _items, changes = operations.move(store, args.sku, args.to.upper(), args.qty)
    err(f"moved {abs(changes[0].delta)} of {args.sku} to {args.to.upper()}")
    return EXIT_OK


def cmd_adjust(store: Store, args: argparse.Namespace) -> int:
    item, _change = operations.adjust(store, args.sku, args.delta, args.reason)
    err(f"{args.sku} is now {item.quantity}")
    return EXIT_OK


def cmd_remove(store: Store, args: argparse.Namespace) -> int:
    operations.remove_item(store, args.sku, force=args.force)
    err(f"removed {args.sku}")
    return EXIT_OK


def cmd_history(store: Store, args: argparse.Namespace) -> int:
    store.get(args.sku)                      # raises NotFoundError if absent
    changes = store.history_for(args.sku)
    if args.json:
        out(json.dumps([{"at": c.at.isoformat(), "action": c.action,
                         "delta": c.delta, "reason": c.reason,
                         "detail": c.detail} for c in changes], indent=2))
    else:
        out("\n".join(str(c) for c in changes) or "no history")
    return EXIT_OK


def cmd_report(store: Store, args: argparse.Namespace) -> int:
    if args.kind == "low-stock":
        rows = reporting.low_stock(store, args.threshold)
        if args.json:
            out(json.dumps([r.__dict__ for r in rows], indent=2))
        else:
            out("\n".join(f"{r.quantity:>5}  {r.sku:<12} {r.name} @{r.location}"
                          for r in rows) or "nothing below threshold")
    elif args.kind == "value":
        rows = reporting.value_by(store, args.group_by)
        if args.json:
            out(json.dumps([{"group": r.group, "items": r.items,
                             "units": r.units,
                             "value": str(r.value)} for r in rows], indent=2))
        else:
            out("\n".join(f"{r.group:<12} {r.items:>4} items  {r.units:>6} units"
                          f"  {str(r.value):>14}" for r in rows) or "empty")
    else:
        items = reporting.dead_stock(store, args.days)
        out(render_items(items, args.json))
    return EXIT_OK


def cmd_export(store: Store, args: argparse.Namespace) -> int:
    items = operations.filtered(store)
    out(serialization.to_csv(items) if args.format == "csv"
        else serialization.to_json(items))
    return EXIT_OK


def cmd_import(store: Store, args: argparse.Namespace) -> int:
    text = (sys.stdin.read() if args.path == "-"
            else Path(args.path).read_text(encoding="utf-8"))
    plan = serialization.plan_import(store, text)

    for problem in plan.errors:
        err(f"error: {problem}")
    err(plan.summary())

    if args.dry_run:
        for item in plan.to_add:
            err(f"  + {item.sku} {item.name}")
        for existing, incoming in plan.to_update:
            err(f"  ~ {existing.sku} qty {existing.quantity} -> {incoming.quantity}")
        return EXIT_OK if plan.ok else EXIT_FAILED

    changed = serialization.apply_import(store, plan)
    err(f"imported {changed} records")
    return EXIT_OK


HANDLERS: dict[str, Callable[[Store, argparse.Namespace], int]] = {
    "add": cmd_add, "list": cmd_list, "search": cmd_search, "move": cmd_move,
    "adjust": cmd_adjust, "remove": cmd_remove, "history": cmd_history,
    "report": cmd_report, "export": cmd_export, "import": cmd_import,
}
# A dispatch dict rather than an if/elif chain: adding a command touches one
# line here and one parser definition, and the mapping is inspectable.

WRITING_COMMANDS = frozenset({"add", "move", "adjust", "remove", "import"})


# --- parser -------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="inv", description="warehouse inventory")
    p.add_argument("--version", action="version", version=f"inv {__version__}")
    p.add_argument("--file", type=Path, default=None,
                   help="data file (default: $INVENTORY_FILE, else "
                        f"{DEFAULT_FILE})")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add")
    a.add_argument("sku")
    a.add_argument("name")
    a.add_argument("--qty", type=int, required=True)
    a.add_argument("--price", required=True)
    a.add_argument("--location", required=True)
    a.add_argument("--tags")

    ls = sub.add_parser("list")
    ls.add_argument("--location")
    ls.add_argument("--tag")
    ls.add_argument("--min-qty", type=int, dest="min_qty")
    ls.add_argument("--max-qty", type=int, dest="max_qty")
    ls.add_argument("--sort", default="sku",
                    choices=["sku", "name", "qty", "value", "location", "updated"])
    ls.add_argument("--desc", action="store_true")
    ls.add_argument("--limit", type=int)

    se = sub.add_parser("search")
    se.add_argument("query")
    se.add_argument("--in", dest="in_fields", default="name,sku,tags")

    mv = sub.add_parser("move")
    mv.add_argument("sku")
    mv.add_argument("--to", required=True)
    mv.add_argument("--qty", type=int)

    ad = sub.add_parser("adjust")
    ad.add_argument("sku")
    ad.add_argument("--delta", type=int, required=True)
    ad.add_argument("--reason", required=True)

    rm = sub.add_parser("remove")
    rm.add_argument("sku")
    rm.add_argument("--force", action="store_true")

    hi = sub.add_parser("history")
    hi.add_argument("sku")

    rep = sub.add_parser("report")
    rep.add_argument("kind", choices=["low-stock", "value", "dead-stock"])
    rep.add_argument("--threshold", type=int, default=10)
    rep.add_argument("--group-by", dest="group_by", default="location",
                     choices=["location", "tag", "none"])
    rep.add_argument("--days", type=int, default=90)

    ex = sub.add_parser("export")
    ex.add_argument("--format", default="csv", choices=["csv", "json"])

    im = sub.add_parser("import")
    im.add_argument("path", help="a CSV file, or - for stdin")
    im.add_argument("--dry-run", action="store_true", dest="dry_run")

    return p


def resolve_path(explicit: Path | None, env: dict[str, str]) -> Path:
    """--file, then $INVENTORY_FILE, then the default. env is a PARAMETER."""
    if explicit is not None:
        return explicit
    from_env = env.get("INVENTORY_FILE")
    return Path(from_env) if from_env else DEFAULT_FILE


# --- entry point --------------------------------------------------------------
def main(argv: Sequence[str] | None = None,
         env: dict[str, str] | None = None) -> int:
    """argv and env are PARAMETERS with defaults.

    That is what lets a test call main(["list", "--json"], env={...}) and assert
    on the exit code, with no monkeypatching of sys.argv or os.environ -- both
    of which are process-global state shared by every other test in the run.
    """
    env = os.environ.copy() if env is None else env
    parser = build_parser()
    args = parser.parse_args(argv)                # argparse exits 2 on bad usage

    path = resolve_path(args.file, env)

    try:
        store = Store.load(path)
        exit_code = HANDLERS[args.command](store, args)
        if args.command in WRITING_COMMANDS and not getattr(args, "dry_run", False):
            store.save(path)
    except InventoryError as exc:
        # ONE except clause for everything the package raises deliberately,
        # because they all inherit from one base and each carries its own
        # exit_code. Adding an error type cannot forget to add its code.
        if args.json:
            err(json.dumps(exc.as_dict()))
        else:
            err(f"error: {exc}")
        return exc.exit_code
    except KeyboardInterrupt:
        err("interrupted")
        return 130                                # 128 + SIGINT
    except BrokenPipeError:
        # `inv list | head -3` closes the pipe early. Without this the user sees
        # a traceback for using their shell correctly.
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return EXIT_OK

    return exit_code


def run() -> None:
    """The console_scripts entry point named in pyproject.toml."""
    raise SystemExit(main())


if __name__ == "__main__":
    run()

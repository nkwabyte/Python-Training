# Exercise 06.3 — From script to package

`bookmarks.py` in this directory is a working 300-line tool that has outgrown
being one file. Convert it into a proper distributable package.

## Target structure

```
bookmarks/
├── pyproject.toml
├── README.md
├── src/
│   └── bookmarks/
│       ├── __init__.py          curated public API + __version__
│       ├── __main__.py          thin shim: python -m bookmarks
│       ├── cli.py               argument parsing, exit codes, and nothing else
│       ├── models.py            the Bookmark type
│       ├── storage.py           load/save, atomic writes
│       ├── search.py            querying and filtering
│       └── errors.py            the package's exception hierarchy
└── tests/
    ├── conftest.py
    ├── test_storage.py
    ├── test_search.py
    └── test_cli.py
```

## Requirements

1. **`python -m bookmarks --help` works** without installing anything.
2. **`pip install -e .` then `bookmarks --help` works**, via a
   `[project.scripts]` entry point.
3. **No module does I/O at import time.** Verify with:
   `python -c "import bookmarks"` completing instantly and printing nothing.
4. **`cli.py` contains no business logic** — it parses arguments, calls into the
   package, formats output, and returns an exit code. Everything it calls must
   be testable without touching `argv` or stdout.
5. **Tests import `bookmarks`, never a relative path**, and must pass against
   the installed package. Since `src/` is not on `sys.path`, a forgotten module
   will fail your own test run.
6. **The data file location is configurable** via `--file` or the
   `BOOKMARKS_FILE` environment variable, with a documented default. Not
   hardcoded, and not relative to `__file__`.
7. **Errors are the package's own types**, defined in `errors.py`, all
   inheriting from one base. `cli.py` catches that base and maps it to exit
   codes; nothing else prints.

## Questions to answer in your README

- Which functions did you have to change to remove hidden I/O, and what did the
  change look like?
- Where did the argument parsing end and the logic begin? Was that boundary
  obvious in the original script?
- What would break if you used the flat layout instead of `src/`?
- Which exit codes did you choose, and why? (Convention: 0 success, 1 general
  failure, 2 usage error.)

## Stretch

- Add `py.typed` and make `mypy --strict src/` pass.
- Make the storage layer swappable: a `Protocol` with a JSON implementation and
  a SQLite one (Module 10 covers `Protocol` properly; try it now anyway).

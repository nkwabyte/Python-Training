#!/usr/bin/env python3
"""bookmarks.py -- a single-file bookmark manager that has outgrown one file.

Works. Untestable. Convert it into a package (see README.md).

    python bookmarks.py add https://example.com --tags ref,tools --title "Example"
    python bookmarks.py list --tag tools
    python bookmarks.py search example
    python bookmarks.py remove 1
    python bookmarks.py stats
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

# PROBLEM 1: I/O at import time. This runs on `import bookmarks`.
DB_PATH = os.path.expanduser("~/.bookmarks.json")
if os.path.exists(DB_PATH):
    with open(DB_PATH) as fh:
        DB = json.load(fh)
else:
    DB = {"next_id": 1, "items": []}


def save():
    # PROBLEM 2: not atomic. A crash mid-write truncates the user's data.
    with open(DB_PATH, "w") as fh:
        json.dump(DB, fh, indent=2)


def add(url, title=None, tags=None):
    # PROBLEM 3: prints AND mutates AND saves. Cannot be tested without a disk.
    if not url.startswith(("http://", "https://")):
        print(f"error: {url} is not a valid URL", file=sys.stderr)
        sys.exit(1)
    for item in DB["items"]:
        if item["url"] == url:
            print(f"error: already bookmarked as #{item['id']}", file=sys.stderr)
            sys.exit(1)
    item = {
        "id": DB["next_id"],
        "url": url,
        "title": title or url,
        "tags": [t.strip() for t in (tags or "").split(",") if t.strip()],
        "added": datetime.now(timezone.utc).isoformat(),
    }
    DB["items"].append(item)
    DB["next_id"] += 1
    save()
    print(f"added #{item['id']}: {item['title']}")


def remove(bookmark_id):
    for i, item in enumerate(DB["items"]):
        if item["id"] == bookmark_id:
            DB["items"].pop(i)
            save()
            print(f"removed #{bookmark_id}")
            return
    print(f"error: no bookmark #{bookmark_id}", file=sys.stderr)
    sys.exit(1)


def list_items(tag=None):
    # PROBLEM 4: filtering and formatting are tangled together.
    items = DB["items"]
    if tag:
        items = [i for i in items if tag in i["tags"]]
    if not items:
        print("no bookmarks")
        return
    width = max(len(i["title"]) for i in items)
    for item in items:
        tags = ",".join(item["tags"])
        print(f"{item['id']:>4}  {item['title']:<{width}}  {item['url']}  [{tags}]")


def search(query):
    q = query.lower()
    hits = [
        i for i in DB["items"]
        if q in i["title"].lower() or q in i["url"].lower()
        or any(q in t.lower() for t in i["tags"])
    ]
    if not hits:
        print(f"no matches for {query!r}")
        return
    for item in hits:
        print(f"{item['id']:>4}  {item['title']}  {item['url']}")


def stats():
    items = DB["items"]
    tags = {}
    for item in items:
        for t in item["tags"]:
            tags[t] = tags.get(t, 0) + 1
    print(f"{len(items)} bookmarks, {len(tags)} tags")
    for tag, n in sorted(tags.items(), key=lambda kv: (-kv[1], kv[0]))[:10]:
        print(f"  {n:>4}  {tag}")


def main():
    parser = argparse.ArgumentParser(description="bookmark manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("url")
    p_add.add_argument("--title")
    p_add.add_argument("--tags")

    p_rm = sub.add_parser("remove")
    p_rm.add_argument("id", type=int)

    p_ls = sub.add_parser("list")
    p_ls.add_argument("--tag")

    p_se = sub.add_parser("search")
    p_se.add_argument("query")

    sub.add_parser("stats")

    args = parser.parse_args()
    if args.command == "add":
        add(args.url, args.title, args.tags)
    elif args.command == "remove":
        remove(args.id)
    elif args.command == "list":
        list_items(args.tag)
    elif args.command == "search":
        search(args.query)
    elif args.command == "stats":
        stats()


if __name__ == "__main__":
    main()

"""Exercise 10.2 — Five levels deep, three LSP violations.

A hierarchy that grew one class at a time and is now unmaintainable. Find the
violations, then convert it to composition.

Run:  python ex02_refactor.py
"""

from __future__ import annotations

from typing import Any


class Document:
    def __init__(self, title: str, body: str) -> None:
        self.title, self.body = title, body

    def render(self) -> str:
        return f"{self.title}\n{'=' * len(self.title)}\n{self.body}"

    def save(self, path: str) -> None:
        print(f"    writing {len(self.render())} bytes to {path}")

    def word_count(self) -> int:
        return len(self.body.split())


class FormattedDocument(Document):
    def __init__(self, title: str, body: str, style: str = "plain") -> None:
        super().__init__(title, body)
        self.style = style

    def render(self) -> str:
        text = super().render()
        return text.upper() if self.style == "shout" else text


class VersionedDocument(FormattedDocument):
    def __init__(self, title: str, body: str, style: str = "plain") -> None:
        super().__init__(title, body, style)
        self.versions: list[str] = [body]

    def edit(self, new_body: str) -> None:
        self.versions.append(new_body)
        self.body = new_body


class ReadOnlyDocument(VersionedDocument):
    """VIOLATION 1. Find it."""

    def edit(self, new_body: str) -> None:
        raise NotImplementedError("this document is read-only")

    def save(self, path: str) -> None:
        raise PermissionError("cannot save a read-only document")


class EncryptedDocument(ReadOnlyDocument):
    """VIOLATION 2 and 3. Find them."""

    def __init__(self, title: str, body: str, key: str) -> None:
        super().__init__(title, body)
        self.key = key

    def render(self) -> str:
        return "".join(chr(ord(c) ^ 7) for c in super().render())

    def word_count(self) -> str:            # type: ignore[override]
        return "unavailable for encrypted documents"


def summarise(doc: Document) -> str:
    """Written against Document. Must work for every subclass -- that is what
    inheritance PROMISED. Run it against each and see which promises broke."""
    return f"{doc.word_count()} words, {len(doc.render())} chars"


# TODO 1 -----------------------------------------------------------------------
# Name each violation precisely. For each, say which of these it is:
#   - raises where the base did not
#   - changes the RETURN TYPE
#   - strengthens a precondition
#   - weakens a postcondition
#   - changes the __init__ signature incompatibly
# And for each, say what a caller written against Document actually experiences.

# TODO 2 -----------------------------------------------------------------------
# Redesign with composition. A sketch to start from -- adapt it:
#
#   @dataclass(frozen=True)
#   class Content:            title, body           (data only)
#
#   class Renderer(Protocol): def render(Content) -> str
#     PlainRenderer, ShoutRenderer, EncryptedRenderer
#
#   class Store(Protocol):    def save(str, path) -> None
#     FileStore, ReadOnlyStore  (raises on save -- and that is FINE here; why?)
#
#   class History:            versions, edit()      (optional, composed in)
#
#   class DocumentV2:         holds Content + Renderer + Store + optional History
#
# The interesting question, which you must answer in a comment: ReadOnlyStore
# raising on save() looks like exactly the same violation as
# ReadOnlyDocument.save(). Why is it acceptable in the composed design and not
# in the inherited one?

# TODO 3 -----------------------------------------------------------------------
# Make summarise_v2(doc: DocumentV2) work for EVERY combination, with no
# special cases and no isinstance checks.

# TODO 4 -----------------------------------------------------------------------
# Count and compare:
#   - lines of code, both versions
#   - number of classes
#   - how many classes must change to add "encrypted AND versioned AND saveable"
# The last number is the real argument.


def demo_the_violations() -> None:
    docs = [
        ("Document", Document("Title", "hello world")),
        ("Formatted", FormattedDocument("Title", "hello world", "shout")),
        ("Versioned", VersionedDocument("Title", "hello world")),
        ("ReadOnly", ReadOnlyDocument("Title", "hello world")),
        ("Encrypted", EncryptedDocument("Title", "hello world", "k")),
    ]
    for label, doc in docs:
        try:
            print(f"  {label:<12} {summarise(doc)}")
        except Exception as exc:
            print(f"  {label:<12} BROKE: {type(exc).__name__}: {exc}")

    print("\n  now try editing and saving each:")
    for label, doc in docs:
        for action in ("edit", "save"):
            try:
                if action == "edit" and hasattr(doc, "edit"):
                    doc.edit("new body")     # type: ignore[attr-defined]
                elif action == "save":
                    doc.save("/tmp/out.txt")
            except Exception as exc:
                print(f"  {label:<12} {action}: {type(exc).__name__}")


if __name__ == "__main__":
    demo_the_violations()

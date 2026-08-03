"""Exercise 01.5 — Traceback triage.

Five broken functions. For each one, IN THIS ORDER:

  1. Read the code and WRITE DOWN your prediction: which exception type, and
     which line raises it. Do this before running. Predicting first is the
     entire point of the exercise; running first teaches you nothing.
  2. Run it (uncomment the call at the bottom, one at a time).
  3. Read the traceback bottom-up and write down which frame was ACTUALLY at
     fault, which is often not the frame that raised.
  4. Fix it.

Record your answers in the ANSWERS block at the bottom of this file.

The distinction being trained here: the frame that RAISES an exception is often
not the frame that CONTAINS the mistake. In case 2 the mistake is two frames
up. In case 4 it is in the caller's data, not the callee's code. Learning to
scan upward for the first frame you actually wrote is the skill that makes
library tracebacks stop being intimidating.
"""

from __future__ import annotations


# --- case 1 -----------------------------------------------------------------
def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)


def case1() -> float:
    readings: list[float] = []
    return average(readings)


# --- case 2 -----------------------------------------------------------------
def parse_row(row: str) -> dict[str, str]:
    name, age, city = row.split(",")
    return {"name": name, "age": age, "city": city}


def load(rows: list[str]) -> list[dict[str, str]]:
    return [parse_row(r) for r in rows]


def case2() -> list[dict[str, str]]:
    return load(["ada,36,london", "grace,45", "alan,41,cambridge"])


# --- case 3 -----------------------------------------------------------------
def get_setting(config: dict[str, object], key: str) -> object:
    return config[key]


def case3() -> object:
    config = {"host": "localhost", "port": 8080}
    return get_setting(config, "timeout")


# --- case 4 -----------------------------------------------------------------
def total_price(items: list[dict[str, object]]) -> float:
    return sum(item["price"] * item["qty"] for item in items)  # type: ignore[operator]


def case4() -> float:
    cart = [
        {"price": 9.99, "qty": 2},
        {"price": "19.99", "qty": 1},  # came from a form, never converted
    ]
    return total_price(cart)


# --- case 5 -----------------------------------------------------------------
def fetch(url: str) -> str:
    raise ConnectionError(f"could not reach {url}")


def fetch_with_fallback(url: str) -> str:
    try:
        return fetch(url)
    except ConnectionError:
        return fetch(url.replace("https", "http"))


def case5() -> str:
    return fetch_with_fallback("https://example.invalid/data")


if __name__ == "__main__":
    # Uncomment ONE at a time, after writing your prediction.
    # print(case1())
    # print(case2())
    # print(case3())
    # print(case4())
    # print(case5())
    pass


ANSWERS = """
case 1
  predicted exception :
  predicted line      :
  actual              :
  frame at fault      :
  fix                 :

case 2
  predicted exception :
  predicted line      :
  actual              :
  frame at fault      :
  fix                 :
  NOTE: which ROW of the input caused it? How did you know from the traceback,
        and what would you add to the code so the traceback tells you next time?

case 3
  predicted exception :
  actual              :
  fix                 :
  NOTE: name two different correct fixes and say when each is right.

case 4
  predicted exception :
  actual              :
  frame at fault      :
  NOTE: the exception is raised inside total_price, but the MISTAKE is in
        case4. Explain the difference in one sentence.

case 5
  predicted exception :
  actual              :
  NOTE: the traceback shows TWO exceptions joined by a sentence. Quote that
        sentence and explain what it means. Which of the two is the real story
        for someone debugging this?
"""

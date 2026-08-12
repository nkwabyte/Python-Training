"""Exercise 12.1 — Six Java-style designs to rewrite.

For each: write the idiomatic Python version, count the lines and classes
removed, and name the language feature that made the pattern unnecessary.

Run:  python ex01_depatternise.py
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import Any


# --- 1: Strategy --------------------------------------------------------------
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]: ...


class AscendingSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)


class DescendingSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data, reverse=True)


class ByAbsoluteValueSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data, key=abs)


class Sorter:
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self._strategy.sort(data)


# --- 2: Singleton -------------------------------------------------------------
class ConfigSingleton:
    _instance: ConfigSingleton | None = None
    _lock = threading.Lock()

    def __new__(cls) -> ConfigSingleton:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:      # double-checked locking
                    cls._instance = super().__new__(cls)
                    cls._instance._data = {"debug": False}
        return cls._instance

    def get(self, key: str) -> Any:
        return self._data.get(key)             # type: ignore[attr-defined]


# --- 3: Factory ---------------------------------------------------------------
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...


class Dog(Animal):
    def speak(self) -> str: return "woof"


class Cat(Animal):
    def speak(self) -> str: return "meow"


class AnimalFactory:
    @staticmethod
    def create(kind: str) -> Animal:
        if kind == "dog":
            return Dog()
        if kind == "cat":
            return Cat()
        raise ValueError(f"unknown animal: {kind}")


# --- 4: Observer --------------------------------------------------------------
class Observer(ABC):
    @abstractmethod
    def update(self, event: str) -> None: ...


class EmailObserver(Observer):
    def update(self, event: str) -> None:
        print(f"    email: {event}")


class LogObserver(Observer):
    def update(self, event: str) -> None:
        print(f"    log: {event}")


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str) -> None:
        for observer in self._observers:
            observer.update(event)


# --- 5: Template Method -------------------------------------------------------
class DataProcessor(ABC):
    def process(self, raw: str) -> str:
        data = self.parse(raw)
        data = self.transform(data)
        return self.render(data)

    @abstractmethod
    def parse(self, raw: str) -> list[str]: ...

    def transform(self, data: list[str]) -> list[str]:
        return data

    @abstractmethod
    def render(self, data: list[str]) -> str: ...


class CsvProcessor(DataProcessor):
    def parse(self, raw: str) -> list[str]:
        return raw.split(",")

    def transform(self, data: list[str]) -> list[str]:
        return [d.strip().upper() for d in data]

    def render(self, data: list[str]) -> str:
        return " | ".join(data)


# --- 6: Builder ---------------------------------------------------------------
class Pizza:
    def __init__(self) -> None:
        self.size = ""
        self.toppings: list[str] = []
        self.extra_cheese = False


class PizzaBuilder:
    def __init__(self) -> None:
        self._pizza = Pizza()

    def size(self, size: str) -> PizzaBuilder:
        self._pizza.size = size
        return self

    def topping(self, topping: str) -> PizzaBuilder:
        self._pizza.toppings.append(topping)
        return self

    def extra_cheese(self) -> PizzaBuilder:
        self._pizza.extra_cheese = True
        return self

    def build(self) -> Pizza:
        if not self._pizza.size:
            raise ValueError("size is required")
        return self._pizza


# TODO -------------------------------------------------------------------------
# Rewrite all six. For each, fill in this table in a comment:
#
#   pattern   | classes before | classes after | lines before | lines after
#             | the Python feature that replaced it
#
# Then answer two questions:
#
# Q1. Which of the six is the ONLY one where the Java-style version has a real
#     advantage over the idiomatic Python version? What is that advantage, and
#     under what circumstances would it be worth the extra classes?
#
# Q2. The Builder exists to validate that required fields are present before
#     construction. Which Python feature makes that unnecessary, and what is the
#     one thing Builder does that it cannot do?


def demo() -> None:
    print("1 Strategy:  ", Sorter(ByAbsoluteValueSort()).sort([-5, 2, -1]))
    print("2 Singleton: ", ConfigSingleton() is ConfigSingleton())
    print("3 Factory:   ", AnimalFactory.create("dog").speak())
    s = Subject(); s.attach(EmailObserver()); s.attach(LogObserver())
    print("4 Observer:"); s.notify("order placed")
    print("5 Template:  ", CsvProcessor().process("a, b, c"))
    p = PizzaBuilder().size("large").topping("olive").extra_cheese().build()
    print("6 Builder:   ", p.size, p.toppings, p.extra_cheese)


if __name__ == "__main__":
    demo()

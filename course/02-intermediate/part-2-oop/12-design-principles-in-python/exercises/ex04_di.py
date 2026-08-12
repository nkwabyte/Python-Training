"""Exercise 12.4 — Invert the dependencies until nothing touches I/O.

OrderService below cannot be tested without a database, a mail server, a
payment gateway, a real clock, and a random number generator. Fix that without
a framework.

Run:  python ex04_di.py
"""

from __future__ import annotations

import random
import smtplib
import sqlite3
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any


class PaymentGateway:
    def charge(self, card: str, amount: Decimal) -> str:
        raise RuntimeError("this would hit a real payment provider")


class OrderService:
    """Five hidden dependencies. Find all five before reading the TODOs."""

    def __init__(self, db_path: str = "orders.db") -> None:
        self.conn = sqlite3.connect(db_path)          # 1
        self.gateway = PaymentGateway()               # 2
        self.mail = smtplib.SMTP("localhost")         # 3

    def place_order(self, customer_email: str, items: list[dict[str, Any]],
                    card: str) -> dict[str, Any]:
        order_id = str(uuid.uuid4())                   # 4
        created = datetime.now()                       # 5
        total = sum(Decimal(str(i["price"])) * i["qty"] for i in items)

        if random.random() < 0.01:                     # 5 again
            raise RuntimeError("simulated flakiness")

        charge_id = self.gateway.charge(card, total)

        self.conn.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?)",
            (order_id, customer_email, str(total), created.isoformat()),
        )
        self.conn.commit()

        self.mail.sendmail(
            "orders@example.com", customer_email,
            f"Subject: Order {order_id}\n\nTotal: {total}",
        )
        return {"id": order_id, "total": total, "charge": charge_id}


# TODO 1 -----------------------------------------------------------------------
# Define a Protocol for each dependency, as NARROW as OrderService actually
# needs (interface segregation -- do not define "a database", define "something
# that can save an order").

# TODO 2 -----------------------------------------------------------------------
# Rewrite OrderService to RECEIVE its dependencies, with production defaults so
# that real callers are not inconvenienced.
#
# Include the clock and the ID generator. Those two are the ones people forget,
# and they are why tests become flaky rather than merely slow.

# TODO 3 -----------------------------------------------------------------------
# Write fakes: InMemoryOrderRepo, FakeGateway (recording charges, able to fail
# on demand), FakeMailer (recording messages), a fixed clock, and a counting ID
# generator.
#
# Prefer FAKES (working implementations) over MOCKS (assertion recorders). A
# fake that stores orders in a dict lets you assert on OUTCOMES; a mock only
# lets you assert that a method was called. Module 18 argues this properly --
# form the habit now.

# TODO 4 -----------------------------------------------------------------------
# Write these tests, all of which must run with no I/O and produce identical
# results on every run:
#   - a successful order is stored, charged and emailed
#   - the order id and timestamp are exactly what the injected generators gave
#   - a declined payment stores nothing and sends no email
#   - a mail failure does NOT roll back a successful charge (decide what SHOULD
#     happen here and write down the reasoning -- this is the transfer problem
#     from Module 08 again)
#   - the total is exact for prices like 19.99 x 3

# TODO 5 -----------------------------------------------------------------------
# Answer:
#   - how many of the five dependencies did you find before reading the numbers?
#   - which was hardest to notice, and why?
#   - what would a DI framework have added here, and what would it have cost?
#   - the constructor now has five parameters. Is that worse than the original
#     one? Argue both sides, then decide.


def verify() -> None:
    raise NotImplementedError("build OrderServiceV2 and its fakes first")


if __name__ == "__main__":
    verify()

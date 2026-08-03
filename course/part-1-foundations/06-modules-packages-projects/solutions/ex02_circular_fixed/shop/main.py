from shop.models import Customer, Order


def main() -> int:
    c = Customer("Ada", tier="gold")
    o = Order(c, [("widget", 3, 9.99), ("gizmo", 1, 24.50)])
    c.place(o)
    print(f"{c.name} owes {o.total()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

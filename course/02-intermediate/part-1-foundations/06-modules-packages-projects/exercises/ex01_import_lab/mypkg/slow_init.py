"""Does work at IMPORT time. Find it and move it."""

import time

print("connecting to the database...")
time.sleep(1.5)
CONNECTION = {"connected": True, "at": time.time()}
print("connected")


def query(sql: str) -> list[str]:
    return [f"result for {sql}"]

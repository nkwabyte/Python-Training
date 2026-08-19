# Solutions & Commentary — Module 25: Automation, Scripting, and the OS

## Key Takeaways
- Catch `SIGINT` / `SIGTERM` signals and set a boolean flag for graceful loop shutdown.
- Ensure scripts are idempotent: running twice must produce the same clean state.
- Return explicit exit codes (`0` for success, non-zero for error conditions).

# Solutions & Commentary — Module 19: Standard Library, Files, and Serialization

## Key Takeaways
- Use timezone-aware datetimes with `datetime.timezone.utc`.
- Prefer `pathlib.Path` for cross-platform filesystem operations.
- Avoid `pickle` for untrusted data due to remote code execution risks; use `json` or `tomllib`.

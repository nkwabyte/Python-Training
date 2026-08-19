# Solutions & Commentary — Module B08: Files and Folders

## Exercise B08.1: Read and Write with `with`
- **Why this way:** The `with open(...)` context manager guarantees file descriptor closure even if exceptions occur during I/O.

## Exercise B08.2: Pathlib Recipes
- **Why this way:** `pathlib.Path` provides an object-oriented, cross-platform interface over legacy `os.path` strings.

## Exercise B08.3: CSV Reports
- **Why this way:** `csv.DictReader` and `csv.DictWriter` map columns by header name, making code resilient to column order changes.

## Exercise B08.4: JSON State Persistence
- **Why this way:** `json.dump()` and `json.load()` serialize Python dictionaries and lists to portable JSON text.

## Exercise B08.5: Atomic File Writes
- **Why this way:** Writing to a temporary file (`file.tmp`) and renaming with `Path.replace()` prevents file corruption if the program is interrupted midway.

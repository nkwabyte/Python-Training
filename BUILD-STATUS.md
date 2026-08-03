# Build Status

The course is built module-by-module. This file records exactly what exists so
work can resume without re-deriving anything.

**Last updated:** 2026-08-03

---

## Complete and verified (Modules 01-24)

Parts 1-4 are finished. Every module has:

- `README.md` — the full lesson: concepts, annotated code, mental models,
  a common-mistakes table, a 10-question self-check quiz, exercises index,
  and further reading
- `VISUALS.prompt.md` — paste-ready NotebookLM prompts (video steering prompt,
  mind map, study guide, quiz, flashcards, the specific visuals to demand,
  analogies to use and refuse, accuracy guardrails, and a post-watch checklist)
- `exercises/` — hands-on files with TODOs and embedded tests
- `solutions/` — worked solutions and/or a `SOLUTIONS.md` discussion

| Part | Modules | State |
|---|---|---|
| 1 Foundations | 01-07 | **Complete.** All solution code executed and passing. Module 07's Inventory CLI reference implementation has 85 passing tests. |
| 2 Object-Oriented Python | 08-13 | **Complete.** All runnable solutions verified. |
| 3 Idiomatic and Advanced | 14-20 | **Complete.** All runnable solutions verified. |
| 4 Concurrency and Internals | 21-24 | **Complete.** Labs verified on 3.10; 3.11+ features flagged where used. |

Root files complete: `README.md`, `CURRICULUM.md`, `SETUP.md`, `PROGRESS.md`,
`pyproject.toml`, `requirements-dev.txt`, `.gitignore`, `setup/verify.py`,
`course/VISUAL-GUIDE.md`.

---

## Remaining

### Part 5 — Applied Python
| Module | State |
|---|---|
| 25 Automation and the OS | README + VISUALS **done**; exercises partial (ex02 written) |
| 26 HTTP, APIs, and Scraping | **not started** |
| 27 Databases and Persistence | **not started** |
| 28 Building APIs with FastAPI | **not started** |
| 29 Data and ML Foundations | **not started** |
| 30 Packaging, Deployment, Ops | **not started** |

### Part 6 — System Design with Python
| Module | State |
|---|---|
| 31 Design Fundamentals | **not started** |
| 32 Service Architecture | **not started** |
| 33 Caching, Queues, Jobs | **not started** |
| 34 Data at Scale | **not started** |
| 35 Reliability, Observability, Security | **not started** |
| 36 Capstone | **not started** |

### Appendix (`course/appendix/`) — all not started
`glossary.md`, `idioms-and-pitfalls.md`, `debugging-and-tooling.md`,
`testing.md`, `interview-questions.md`, `resources.md`, `cheatsheets.md`

Directory skeletons for all of the above already exist, and every one of them
is already linked from `CURRICULUM.md` and `course/VISUAL-GUIDE.md`, so adding
the files completes the cross-references with no other edits.

---

## The template each remaining module follows

Copy the shape of any completed module — Module 16 or 21 are good references.

**README.md**
1. Time budget, prerequisite, link to the visual companion
2. "Why this module" — the specific confusions it removes
3. 6-10 numbered concept sections with annotated code
4. A common-mistakes table (mistake / symptom / fix)
5. A 10-question self-check quiz
6. An exercises index linking each file
7. "Going deeper" with 4-5 real sources

**VISUALS.prompt.md**
1. Sources to add (module README + 2-4 authoritative URLs)
2. Cinematic Video Overview: format, visual style block, and a numbered
   steering prompt describing each scene to animate
3. Mind map prompt
4. Study guide, quiz, and flashcard prompts
5. "The specific visuals to insist on" — numbered
6. Analogies that work / analogies to refuse
7. Accuracy guardrails — a paste-in block of factual constraints
8. "After watching, you should be able to" checklist

---

## Conventions established (keep these)

- Course targets **Python 3.12**; anything needing 3.11+ or 3.12+ is flagged
  inline, and exercises degrade gracefully on 3.10 where practical.
- Every claim that is CPython-specific is labelled as such.
- Exercises embed their own tests and run with plain `python file.py`.
- Solutions carry the *reasoning*, not just the code — the comments explain why
  the alternative was rejected.
- Modules cross-reference each other explicitly ("Module 02's aliasing trap"),
  and later modules reuse earlier diagrams deliberately.
- Every measurement claim in the text was produced by actually running the
  benchmark, not estimated.

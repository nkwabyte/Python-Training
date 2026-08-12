# Build Status

The course is built module-by-module. This file records exactly what exists so
work can resume without re-deriving anything.

**Last updated:** 2026-08-12

---

## Structure

The course was reorganised from six flat parts into four levels, so that
learners can enter at the right point:

```
course/
├── 01-beginner/        B01-B12          curriculum outlines written, lessons pending
├── 02-intermediate/    01-13            complete
├── 03-advanced/        14-30            14-25 complete, 26-30 pending
└── 04-system-design/   D01-D10, 31-36   outlines written, lessons pending
```

Nothing was renumbered. Modules 01 to 36 keep the numbers they have always had,
and every cross-reference in the existing lessons still resolves. The two new
tracks use their own prefixes: `B` for beginner, `D` for data structures and
algorithms.

---

## Complete and verified (Modules 01-24)

Every module in Levels 02 and the first two parts of Level 03 has:

- `README.md` — the full lesson: concepts, annotated code, mental models,
  a common-mistakes table, a 10-question self-check quiz, exercises index,
  and further reading
- `VISUALS.prompt.md` — paste-ready NotebookLM prompts (video steering prompt,
  mind map, study guide, quiz, flashcards, the specific visuals to demand,
  analogies to use and refuse, accuracy guardrails, and a post-watch checklist)
- `exercises/` — hands-on files with TODOs and embedded tests
- `solutions/` — worked solutions and/or a `SOLUTIONS.md` discussion

| Level | Part | Modules | State |
|---|---|---|---|
| 02 Intermediate | 1 Foundations | 01-07 | **Complete.** All solution code executed and passing. Module 07's Inventory CLI reference implementation has 85 passing tests. |
| 02 Intermediate | 2 Object-Oriented Python | 08-13 | **Complete.** All runnable solutions verified. |
| 03 Advanced | 3 Idiomatic and Advanced | 14-20 | **Complete.** All runnable solutions verified. |
| 03 Advanced | 4 Concurrency and Internals | 21-24 | **Complete.** Labs verified on 3.10; 3.11+ features flagged where used. |

Root files complete: `README.md`, `CURRICULUM.md`, `SETUP.md`, `PROGRESS.md`,
`pyproject.toml`, `requirements-dev.txt`, `.gitignore`, `setup/verify.py`,
`course/VISUAL-GUIDE.md`, and a README for each of the four levels.

---

## Remaining

### Level 01 — Beginner (Modules B01-B12)

Every module has a **curriculum outline** in place: why the module exists, the
learning outcomes, the numbered concept sections, the exercise list with what
each drills, the common mistakes to address, the self-check questions, and the
further reading. What remains is writing the lesson prose, the exercise files,
and the solutions against those outlines.

| Module | State |
|---|---|
| B01 First Program and the Interpreter | outline **done**; lesson, exercises, solutions pending |
| B02 Data, Names, and Types | outline **done**; rest pending |
| B03 Making Decisions | outline **done**; rest pending |
| B04 Loops and Repetition | outline **done**; rest pending |
| B05 Collections | outline **done**; rest pending |
| B06 Functions | outline **done**; rest pending |
| B07 Working with Text | outline **done**; rest pending |
| B08 Files and Folders | outline **done**; rest pending |
| B09 Errors and Debugging | outline **done**; rest pending |
| B10 Organising Code | outline **done**; rest pending |
| B11 A First Look at Classes | outline **done**; rest pending |
| B12 Project: Expense Tracker CLI | outline **done**; six-stage build pending |

### Level 03 — Advanced, Part 5 Applied Python
| Module | State |
|---|---|
| 25 Automation and the OS | README + VISUALS **done**; exercises partial (ex02 written) |
| 26 HTTP, APIs, and Scraping | **not started** |
| 27 Databases and Persistence | **not started** |
| 28 Building APIs with FastAPI | **not started** |
| 29 Data and ML Foundations | **not started** |
| 30 Packaging, Deployment, Ops | **not started** |

### Level 04 — Part 6, Data Structures and Algorithms (D01-D10)

As with the beginner track, every module has a full curriculum outline, plus a
"The Python angle" section tying it to the modules the learner has already done
and a stated link forward into Part 7.

| Module | State |
|---|---|
| D01 Complexity and Measurement | outline **done**; rest pending |
| D02 Arrays and Dynamic Arrays | outline **done**; rest pending |
| D03 Hash Tables | outline **done**; rest pending |
| D04 Linked Structures | outline **done**; rest pending |
| D05 Trees and Heaps | outline **done**; rest pending |
| D06 Graphs | outline **done**; rest pending |
| D07 Sorting and Searching | outline **done**; rest pending |
| D08 Recursion and Divide and Conquer | outline **done**; rest pending |
| D09 Dynamic Programming and Greedy | outline **done**; rest pending |
| D10 Patterns and the Design Bridge | outline **done**; rest pending |

### Level 04 — Part 7, System Design with Python
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

## Suggested build order

1. **B01 to B06.** The beginner track is the reason for the restructure, and the
   first six modules are the ones a new learner hits first.
2. **B07 to B12.** Finish the level, project included, so it can be used.
3. **D01 to D03.** These are the modules Part 7 depends on for its vocabulary.
4. **26 to 30.** Finish Applied Python, which completes Level 03.
5. **D04 to D10**, then **31 to 36**, then the appendix.

---

## The template each remaining module follows

Copy the shape of any completed module — Module 16 or 21 are good references.
For beginner modules, keep the same structure but shorter sections, more code,
and no forward references to material the learner has not met.

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
- **Beginner modules teach nothing that must later be unlearned.** A name is a
  label, never a box. Type hints and narrow exception handling appear from the
  start.
- **DSA modules pair every complexity claim with a measurement**, because
  Python's constant factors are large enough that theory alone misleads.

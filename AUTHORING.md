# Authoring Standard for Exercise Notebooks

Every exercise in the outline levels is a notebook that teaches, not a stub that
asks. This file is the specification. Any session, human or otherwise, that
picks up the build should follow it exactly, because the value of the format is
that a learner meets the same shape every time and stops having to work out what
is expected of them.

The reference implementation is `course/01-beginner/b01-first-program-and-the-interpreter/exercises/ex01_hello.ipynb`.
When this document and that notebook disagree, the notebook wins and this file
should be corrected.

---

## The rule the whole format exists to enforce

**Nothing is asked before it is taught.**

The defect this standard replaced was an exercise that said "write, save, and run
a program that prints three lines" when no material anywhere had said what
`print` was. If a task uses a thing, the notebook has explained that thing, in
this notebook, above that task. No exceptions, no forward references, no "as you
know".

---

## Cell order

Every exercise notebook has this shape, in this order.

| # | Cell | Type | Contents |
|---|---|---|---|
| 1 | Title | markdown | Module label and title, exercise number and name, one paragraph on why this exercise exists, and a small table: time, what you need, what it comes after |
| 2 | Teaching sections | markdown and code, alternating | Numbered sections. Each explains one idea, then immediately shows it running |
| 3 | Deliberate failure | code and markdown | At least one cell that errors on purpose, followed by a cell that reads the error |
| 4 | `# Your turn` | markdown | A short line marking the change from reading to writing |
| 5 | Tasks | markdown and code, alternating | Each task is a markdown cell stating it, then a code cell containing the fill-in template |
| 6 | Self-check | markdown then code | The harness, described below |
| 7 | What you learned | markdown | Bullets, one per idea taught, in the order taught |
| 8 | Before you move on | markdown | Checkboxes, phrased as things done rather than things known |
| 9 | Next | markdown | One line naming the next exercise and what it covers |

---

## Teaching sections

- Number them. `## 1.`, `## 2.` and so on. Learners refer back by number.
- One idea per section. If a section needs the word "also", it is two sections.
- Explain, then run. The code cell that demonstrates an idea comes immediately
  after the prose that introduced it, never before.
- Take the syntax apart the first time it appears. The ASCII diagram in
  `ex01_hello.ipynb` that labels `print`, the brackets, and the quotes is the
  model. Beginners cannot see structure that has not been pointed at.
- Say what a thing does **not** do, when that is a common wrong belief. "`print`
  does not store anything" prevents a real misconception.
- Cross-reference forward by module, never by assumption: "module B02 makes this
  precise" is allowed and useful. "You already know this" is not.

## Deliberate failures

Every notebook contains at least one cell that fails on purpose, followed by
prose that reads the traceback line by line.

This is the part most courses omit and it does the most work. A learner who
first meets `SyntaxError` at midnight in their own project concludes they are
not cut out for this. A learner who met it in a cell that said "this will fail,
here is why" concludes it is Tuesday.

Never leave a deliberate failure unexplained, and never put one after the tasks.

## Tasks

- Three to five per notebook. Fewer is thin, more is a slog.
- Every task is a **fill-in template**, not an empty cell. Show the structure and
  leave `___` where the learner supplies the content. An empty cell is a test of
  memory; a template is a lesson in shape.
- The first code cell of each task starts with `# ANSWER n` where `n` is the task
  number. The self-check finds the learner's work by this marker, so it must be
  present, must be exact, and the notebook must tell the learner not to delete it.
- At least one task asks for a **prediction before running**. Write the
  prediction slot into the template as a comment ending in `___`.
- At least one task asks for a **judgement in prose**: which version would you
  maintain, what did you change and why. Taste develops by being made explicit.
- Later tasks combine what earlier ones drilled. The last task should produce
  something the learner would show somebody.

## The self-check harness

Every notebook ends with the same machinery, so it is learned once.

```python
def _answer(marker):
    """Find the most recent cell you ran that contains the given marker."""
    try:
        matches = [c for c in _ih if marker in c and "def _answer" not in c]
    except NameError:
        print("Run this in Jupyter or VS Code so the self-check can see your cells.")
        return ""
    return matches[-1] if matches else ""


def check(passed, message):
    print(("PASS  " if passed else "FAIL  ") + message)
    return bool(passed)
```

Then a `results` list of `check(...)` calls, then the footer that counts
failures. Rules for the checks themselves:

- **Check the specific thing, name it specifically.** "Task 2: three separate
  print instructions" tells the learner what to do. "Check 2 failed" does not.
- Five to eight checks per notebook, spread across tasks so a learner always
  knows which task is incomplete.
- Check that placeholders are gone (`"___" not in answer`), that required
  constructs appear, and that predictions were written.
- Never check for an exact answer where several are correct. The card in B01
  exercise 4 checks that borders survive, not what the border is.
- The markdown cell above the harness must say that the learner does not need to
  understand it. It is machinery, not material.

---

## Voice

- Address the learner as "you". Never "we", which is a lecturer's plural.
- Short sentences. The reader is doing two hard things at once.
- No exclamation marks, no encouragement that has not been earned, no "simply",
  "just", "easy", or "obviously". Every one of those words tells a struggling
  learner that the fault is theirs.
- State the cost of a mistake plainly rather than warning vaguely. "This will
  cost you an afternoon" is information; "be careful" is noise.
- British spelling, to match the rest of the course.
- No emoji.

---

## Formats by level

Every exercise in every level is a notebook. The learner meets one format from
their first hour to the capstone, and the explanation always sits next to the
code it explains.

| Level | Exercise format | Solutions |
|---|---|---|
| 01 Beginner | Notebooks | One solution notebook per exercise |
| 02 Intermediate | Notebooks | One solution notebook per exercise |
| 03 Advanced | Notebooks | One solution notebook per exercise |
| 04 System Design, Part 6 | Notebooks | One solution notebook per exercise |
| 05 Machine Learning | Notebooks | One `SOLUTIONS.md` per module |
| Written exercises, any level | `.md` worksheets | Worked answer in the module `SOLUTIONS.md` |

Support files that an exercise operates on rather than teaches from stay as
`.py`. Module 01's shadowing exercise needs a real file called `random.py` on
disk; module 06 needs real packages to import. Those are program files, not
lessons, and turning them into notebooks would destroy the exercise.

### Two states a notebook can be in

**Converted** means the exercise content is intact and split so each task is its
own runnable cell, with the module README still carrying the teaching. Notebook
metadata says `"authored_teaching": false`.

**Authored** means it meets the definition of done below: every construct taught
before it is asked for, a deliberate failure that is explained, fill-in
templates with `# ANSWER n` markers, and a self-check that names what is
missing. Metadata says `"authored_teaching": true`.

`CONVERSION-STATUS.md` tracks which modules are in which state and is the work
list for the authoring pass. Setting the metadata flag is part of finishing a
module, not an afterthought.

---|---|---|
| 01 Beginner | Notebooks | The learner needs explanation and execution interleaved |
| 02 Intermediate | Existing `.py` with embedded tests | Modules 01 to 13 already have full README lessons that teach |
| 03 Advanced | Existing `.py` with embedded tests | Same, for modules 14 to 25 |
| 04 System Design, Part 6 | Notebooks | Complexity claims are paired with measurements, which wants cells |
| 05 Machine Learning | Notebooks | Training, plots, and inspection are inherently iterative |
| Written exercises, any level | `.md` worksheets | Reasoning exercises where code would be the wrong response |

Written worksheets follow the same principles: the prompt, what a good answer
contains, numbered answer spaces, and a closing checklist.

---

## Definition of done, per notebook

- [ ] Every construct used in a task is taught above it, in the same notebook.
- [ ] At least one deliberate failure, explained immediately.
- [ ] Every task is a template with `___` placeholders and an `# ANSWER n` marker.
- [ ] At least one prediction task and one judgement task.
- [ ] Self-check present, checks named specifically, and it fails on a fresh copy.
- [ ] What you learned mirrors the teaching sections in order.
- [ ] Runs top to bottom on a fresh kernel with only the deliberate failures
      failing.

---

# Solutions

Every exercise has a solution file. Its job is **not** to supply the answer,
because the notebook already teaches and the self-check already verifies. Its
job is to supply the reasoning a reviewer would give, which is the part a
learner working alone has no other way to get.

A solution that is only correct code is close to worthless here. A learner who
compares their working answer against a different working answer, with no
commentary, learns nothing except that two answers exist.

## Shape

| # | Cell | Contents |
|---|---|---|
| 1 | Header | "Read this after your own attempt, not instead of it", and a line naming which tasks have definite answers and which are personal |
| 2 | Per task | The worked answer as a runnable code cell, then a markdown cell of commentary |
| 3 | If yours differs | The three questions: is mine wrong, merely different, or better |
| 4 | What this was testing | Two or three sentences naming the actual lesson, which is rarely the visible task |

## The commentary after each task

This is the whole value of the file. Include, as the task warrants:

- **Why this way.** The reason this form was chosen over the alternative.
- **Near misses.** Answers that are wrong in instructive ways, shown as a small
  table or code block, with what each one actually produces. The near miss that
  is *nearly right* teaches more than the answer.
- **The detail most people miss.** One specific thing, named.
- **Where the judgement flips.** If the recommendation depends on context, say
  what context reverses it. Rules given without their boundaries are learned as
  superstition.
- **What was not required.** If the worked answer uses something not yet taught,
  say so explicitly, so a learner who solved it with less does not conclude they
  fell short.

## Rules

- Use a consistent fictional learner for personal answers, so the shape is
  visible without pretending there is one right name or town. B01 uses Ada in
  Accra.
- Never imply a single correct answer where several are correct.
- Solution code must run. Every code cell is compiled in the build check.
- The "If yours differs" cell is identical across all solution notebooks. It
  should become familiar.
- Name the file `<exercise>_solution.ipynb`, beside the exercise it answers, in
  `solutions/`.

## Per level

| Level | Solution format |
|---|---|
| 01 Beginner | One solution notebook per exercise. Cell by cell comparison is worth the cost here |
| 04 Part 6, DSA | One solution notebook per exercise, since each pairs an implementation with a measurement |
| 05 Machine Learning | One `SOLUTIONS.md` per module, discussing all its exercises. Outputs vary too much between runs and machines for a notebook comparison to mean anything |
| Written worksheets | A worked answer inside the module's `SOLUTIONS.md`, not a separate file |

# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
  07:30 — Bean: Breakfast (high, open)
  08:00 — Mochi: Morning walk (high, open)
  08:00 — Mochi: Medication (high, open)
  18:30 — Bean: Evening play (medium, open)

Conflict warnings
  WARNING: Conflict at 08:00: Mochi — Morning walk; Mochi — Medication
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
5 passed in 0.03s
```

## 📐 Smarter Scheduling

PawPal+ uses `Scheduler` as the brain of the system. It retrieves every pet's tasks
through `Owner.get_all_tasks()`, then sorts, filters, recurs, and warns about conflicts.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Chronological `HH:MM` order |
| Filtering | `Scheduler.filter_tasks()` | Filter by pet and completion status |
| Conflict handling | `Scheduler.find_conflicts()` | Warns on exact time matches |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | Daily and weekly copies |

## Implementation summary

`Task` models an activity, `Pet` owns tasks, and `Owner` manages multiple pets.
`Scheduler` coordinates the owner's complete task list. Streamlit stores the Owner in
`st.session_state`, so the UI's pets and tasks survive reruns.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Add one or more pets from the sidebar.
2. Add care tasks with a time, priority, and recurrence.
3. View the multi-pet schedule in chronological order.
4. Read warning banners for exact-time conflicts.
5. Complete recurring tasks to create their next occurrence.

**Confidence level:** ★★★★☆ (4/5). Core behaviors are covered by automated tests;
future work would test overlapping durations and persistence beyond one session.

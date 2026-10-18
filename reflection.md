# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My UML has four classes: Owner manages pets, Pet owns tasks, Task represents one
  care activity, and Scheduler reads all tasks and organizes them.

**b. Design changes**

- I added due dates, duration, priority, and pet ownership to Task, plus
  Scheduler.complete_task(), to support recurrence and multi-pet messages.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- It considers time, pet identity, completion status, and recurrence. Time is primary
  because it creates the clearest daily view; priority remains available for display.

**b. Tradeoffs**

- Conflict detection checks exact matching start times, not overlapping durations.
  This is simple and suitable here, while a production version should compare intervals.

---

## 3. AI Collaboration

**a. How you used AI**

- AI helped brainstorm UML relationships, scaffold dataclasses, suggest sorting, and
  draft tests. Prompts that named behavior and verification criteria were most useful.

**b. Judgment and verification**

- I kept exact-time conflicts instead of accepting a complex interval scheduler. I
  verified that choice with a duplicate-time test and the CLI demo.

---

## 4. Testing and Verification

**a. What you tested**

- Tests cover completion, task addition, chronological sorting across pets, daily
  recurrence, and duplicate-time conflicts—the core user-visible promises.

**b. Confidence**

- I am 4/5 confident because all five tests pass and the CLI exercises multiple pets.
  Next I would test invalid times, weekly recurrence, and overlapping durations.

---

## 5. Reflection

**a. What went well**

- I am most satisfied that the UI and CLI share one backend, especially the multi-pet
  Owner-to-Scheduler relationship.

**b. What you would improve**

- I would add persistent storage, interval-aware scheduling, and edit/delete controls.

**c. Key takeaway**

- I learned that context engineering and verification make AI useful, but the human
  still owns interfaces, trade-offs, and final evidence.

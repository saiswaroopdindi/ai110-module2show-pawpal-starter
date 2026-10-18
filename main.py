from pawpal_system import Owner, Pet, Scheduler, Task


def format_task(task: Task) -> str:
    status = "done" if task.completed else "open"
    return f"{task.time} — {task.pet_name}: {task.description} ({task.priority}, {status})"


owner = Owner("Jordan")
mochi = Pet("Mochi", "dog")
bean = Pet("Bean", "cat")
owner.add_pet(mochi)
owner.add_pet(bean)
mochi.add_task(Task("Morning walk", "08:00", duration_minutes=30, priority="high"))
bean.add_task(Task("Breakfast", "07:30", duration_minutes=10, priority="high"))
mochi.add_task(Task("Medication", "08:00", frequency="daily", duration_minutes=5, priority="high"))
bean.add_task(Task("Evening play", "18:30", duration_minutes=20, priority="medium"))

scheduler = Scheduler(owner)
print("Today's Schedule")
for task in scheduler.sort_by_time():
    print(f"  {format_task(task)}")
print("\nConflict warnings")
for warning in scheduler.find_conflicts():
    print(f"  WARNING: {warning}")

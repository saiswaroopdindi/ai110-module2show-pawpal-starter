from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def setup_household():
    owner = Owner("Alex")
    pet = Pet("Luna", "dog")
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


def test_mark_complete_changes_status():
    task = Task("Feed", "08:00")
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    _, pet, _ = setup_household()
    pet.add_task(Task("Walk", "09:00"))
    assert len(pet.tasks) == 1


def test_scheduler_sorts_tasks_chronologically_across_pets():
    owner, pet, scheduler = setup_household()
    other = Pet("Milo", "cat")
    owner.add_pet(other)
    pet.add_task(Task("Late", "18:00"))
    other.add_task(Task("Early", "07:30"))
    assert [task.description for task in scheduler.sort_by_time()] == ["Early", "Late"]


def test_daily_completion_creates_next_day_task():
    owner, pet, scheduler = setup_household()
    task = Task("Medicine", "08:00", frequency="daily", due_date=date(2026, 10, 18))
    pet.add_task(task)
    next_task = scheduler.complete_task(task)
    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 19)
    assert next_task.completed is False
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_duplicate_times():
    _, pet, scheduler = setup_household()
    pet.add_task(Task("Walk", "09:00"))
    pet.add_task(Task("Feed", "09:00"))
    assert len(scheduler.find_conflicts()) == 1

"""Core domain objects and scheduling algorithms for PawPal+."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represent one pet-care activity."""

    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return the next daily or weekly task, if this task recurs."""
        offsets = {"daily": 1, "weekly": 7}
        if self.frequency.lower() not in offsets:
            return None
        return replace(
            self,
            completed=False,
            due_date=self.due_date + timedelta(days=offsets[self.frequency.lower()]),
        )


@dataclass
class Pet:
    """Store a pet and its care tasks."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task and associate it with this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """Manage an owner's pets and provide a unified task view."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return tasks from every pet."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Organize and analyze tasks belonging to an owner."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def all_tasks(self) -> List[Task]:
        """Retrieve tasks through the owner's multi-pet API."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks in chronological HH:MM order."""
        return sorted(tasks if tasks is not None else self.all_tasks(), key=lambda task: task.time)

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        tasks = self.all_tasks()
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return tasks

    def complete_task(self, task: Task) -> Optional[Task]:
        """Complete a task and append its next recurring occurrence when needed."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is None:
            return None
        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(next_task)
                return next_task
        return None

    def find_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Return warnings for tasks sharing an exact scheduled time."""
        chosen = self.sort_by_time(tasks)
        warnings = []
        for index, first in enumerate(chosen):
            for second in chosen[index + 1 :]:
                if first.time != second.time:
                    break
                warnings.append(
                    f"Conflict at {first.time}: {first.pet_name} — {first.description}; "
                    f"{second.pet_name} — {second.description}"
                )
        return warnings

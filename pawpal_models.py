from dataclasses import dataclass, field
from typing import List
from datetime import datetime, time


@dataclass
class Pet:
    """Represents a pet with care information and management methods."""
    name: str
    species: str
    breed: str
    age: int
    medications: List[str] = field(default_factory=list)
    feeding_schedule: List[time] = field(default_factory=list)
    grooming_interval: int = 30  # days
    
    def add_medication(self, med: str) -> None:
        """Adds a medication reminder."""
        pass
    
    def update_feeding_schedule(self, times: List[time]) -> None:
        """Sets meal times."""
        pass
    
    def get_care_summary(self) -> str:
        """Returns overview of pet's needs."""
        pass


@dataclass
class Task:
    """Represents a care task for a pet."""
    task_id: str
    title: str
    task_type: str  # walk / appointment / grooming / medication
    due_datetime: datetime
    is_completed: bool = False
    linked_pet: Pet = None
    
    def mark_complete(self) -> None:
        """Marks task as done."""
        pass
    
    def reschedule(self, new_datetime: datetime) -> None:
        """Updates the due time."""
        pass
    
    def is_overdue(self) -> bool:
        """Returns true if past due and not complete."""
        pass


@dataclass
class Schedule:
    """Manages tasks and time blocks for the owner."""
    owner_name: str
    tasks: List[Task] = field(default_factory=list)
    time_blocks: List[dict] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Adds a new task."""
        pass
    
    def add_time_block(self, start: time, end: time, label: str) -> None:
        """Blocks out time (e.g. 'Work 9–5')."""
        pass
    
    def get_tasks_for_day(self, date) -> List[Task]:
        """Filters tasks by date."""
        pass
    
    def prioritize_tasks(self) -> List[Task]:
        """Sorts tasks around blocked time."""
        pass


@dataclass
class Reminder:
    """Handles notifications for tasks."""
    reminder_id: str
    linked_task: Task
    trigger_time: datetime
    reminder_type: str  # feeding / medication / grooming / walk
    is_sent: bool = False
    
    def send_reminder(self) -> None:
        """Triggers the alert to the user."""
        pass
    
    def snooze(self, minutes: int) -> None:
        """Delays the reminder."""
        pass
    
    def generate_message(self) -> str:
        """Builds the reminder text (e.g. 'Time to feed Buddy!')."""
        pass

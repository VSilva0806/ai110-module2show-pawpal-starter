from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Task:
    """Represents a single activity with description, time, frequency, and completion status."""
    task_id: str
    description: str
    due_time: datetime
    frequency: str  # once / daily / weekly / monthly
    is_completed: bool = False
    
    def mark_complete(self) -> None:
        """Marks task as done."""
        pass
    
    def reschedule(self, new_time: datetime) -> None:
        """Updates the due time."""
        pass
    
    def get_details(self) -> str:
        """Returns task details."""
        pass


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    pet_id: str
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Adds a task to the pet."""
        pass
    
    def remove_task(self, task_id: str) -> None:
        """Removes a task from the pet."""
        pass
    
    def get_tasks(self) -> List[Task]:
        """Returns all tasks for this pet."""
        pass
    
    def get_pet_info(self) -> str:
        """Returns pet information."""
        pass


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    owner_id: str
    owner_name: str
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's collection."""
        pass
    
    def remove_pet(self, pet_id: str) -> None:
        """Removes a pet from the owner's collection."""
        pass
    
    def get_all_pets(self) -> List[Pet]:
        """Returns all pets owned."""
        pass
    
    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks across all pets."""
        pass
    
    def get_pet_tasks(self, pet_id: str) -> List[Task]:
        """Returns tasks for a specific pet."""
        pass


@dataclass
class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    owner: Owner
    tasks: List[Task] = field(default_factory=list)
    
    def retrieve_tasks(self) -> List[Task]:
        """Retrieves all tasks from the owner's pets."""
        pass
    
    def organize_tasks(self) -> List[Task]:
        """Organizes tasks by priority or due time."""
        pass
    
    def manage_tasks(self) -> None:
        """Manages task execution and scheduling."""
        pass
    
    def get_tasks_by_pet(self, pet_id: str) -> List[Task]:
        """Returns tasks for a specific pet."""
        pass

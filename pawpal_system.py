"""
PawPal+ System Implementation
Core functionality for managing pets, tasks, scheduling, and reminders.
"""

from dataclasses import dataclass, field
from typing import List, Optional
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
        self.is_completed = True
    
    def reschedule(self, new_time: datetime) -> None:
        """Updates the due time."""
        self.due_time = new_time
    
    def get_details(self) -> str:
        """Returns task details."""
        status = "✓ Complete" if self.is_completed else "⏳ Pending"
        return f"{self.description} | Due: {self.due_time} | Frequency: {self.frequency} | {status}"


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    pet_id: str
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> Task:
        """Adds a task to the pet and returns it."""
        self.tasks.append(task)
        return task
    
    def remove_task(self, task_id: str) -> bool:
        """Removes a task from the pet. Returns True if successful, False if not found."""
        task = self._find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def get_tasks(self) -> List[Task]:
        """Returns all tasks for this pet."""
        return self.tasks
    
    def get_pet_info(self) -> str:
        """Returns pet information."""
        return f"{self.name} ({self.species} - {self.breed}), Age: {self.age}"
    
    def _find_task_by_id(self, task_id: str) -> Optional[Task]:
        """Helper method to find a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    owner_id: str
    owner_name: str
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> Pet:
        """Adds a pet to the owner's collection and returns it."""
        self.pets.append(pet)
        return pet
    
    def remove_pet(self, pet_id: str) -> bool:
        """Removes a pet from the owner's collection. Returns True if successful, False if not found."""
        pet = self._find_pet_by_id(pet_id)
        if pet:
            self.pets.remove(pet)
            return True
        return False
    
    def get_all_pets(self) -> List[Pet]:
        """Returns all pets owned."""
        return self.pets
    
    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def get_pet_tasks(self, pet_id: str) -> Optional[List[Task]]:
        """Returns tasks for a specific pet, or None if pet not found."""
        pet = self._find_pet_by_id(pet_id)
        return pet.get_tasks() if pet else None
    
    def _find_pet_by_id(self, pet_id: str) -> Optional[Pet]:
        """Helper method to find a pet by ID."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None


@dataclass
class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    owner: Owner
    
    def retrieve_tasks(self) -> List[Task]:
        """Retrieves all tasks from the owner's pets."""
        return self.owner.get_all_tasks()
    
    def organize_tasks(self) -> List[Task]:
        """Organizes tasks by due time (earliest first), excluding completed tasks."""
        tasks = self.retrieve_tasks()
        pending_tasks = [task for task in tasks if not task.is_completed]
        return sorted(pending_tasks, key=lambda task: task.due_time)
    
    def manage_tasks(self) -> None:
        """Manages task execution and scheduling (placeholder for complex logic)."""
        pass
    
    def get_tasks_by_pet(self, pet_id: str) -> Optional[List[Task]]:
        """Returns tasks for a specific pet, or None if pet not found."""
        return self.owner.get_pet_tasks(pet_id)
    
    def get_overdue_tasks(self) -> List[Task]:
        """Returns all tasks that are past due and not completed."""
        current_time = datetime.now()
        return [task for task in self.retrieve_tasks() 
                if task.due_time < current_time and not task.is_completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Returns all completed tasks."""
        return [task for task in self.retrieve_tasks() if task.is_completed]
    
    def get_tasks_by_frequency(self, frequency: str) -> List[Task]:
        """Returns all pending tasks matching a specific frequency."""
        return [task for task in self.organize_tasks() if task.frequency == frequency]

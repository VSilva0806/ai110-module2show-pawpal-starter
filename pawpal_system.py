"""
PawPal+ System Implementation
Core functionality for managing pets, tasks, scheduling, and reminders.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class TaskStatus(Enum):
    """Enumeration of task statuses."""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"


@dataclass
class Task:
    """Represents a single activity with description, time, frequency, and completion status."""
    task_id: str
    description: str
    due_time: datetime
    frequency: str  # once / daily / weekly / monthly
    pet_id: str = ""  # Reference to the pet this task belongs to
    is_completed: bool = False
    parent_task_id: Optional[str] = None  # Reference to parent task if this is a recurring instance
    
    def mark_complete(self) -> None:
        """Marks task as done."""
        self.is_completed = True
    
    def reschedule(self, new_time: datetime) -> None:
        """Updates the due time."""
        self.due_time = new_time
    
    def is_recurring(self) -> bool:
        """Returns True if the task is recurring."""
        return self.frequency in ["daily", "weekly", "monthly"]
    
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
        task.pet_id = self.pet_id  # Set the pet_id reference
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
        return [task for pet in self.pets for task in pet.get_tasks()]
    
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
    
    # ==================== ADVANCED SORTING ====================
    
    def sort_tasks_by_time(self, ascending: bool = True) -> List[Task]:
        """
        Sorts all pending tasks by due time.
        
        Args:
            ascending: If True, sorts earliest first. If False, latest first.
            
        Returns:
            List of tasks sorted by time.
        """
        tasks = [task for task in self.retrieve_tasks() if not task.is_completed]
        return sorted(tasks, key=lambda task: task.due_time, reverse=not ascending)
    
    def get_today_tasks(self) -> List[Task]:
        """Returns all pending tasks due today."""
        today = datetime.now().date()
        return [task for task in self.organize_tasks() 
                if task.due_time.date() == today]
    
    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Returns all pending tasks due within the next N days."""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        return [task for task in self.organize_tasks() 
                if now <= task.due_time <= cutoff]
    
    # ==================== ADVANCED FILTERING ====================
    
    def filter_tasks(self, pet_id: Optional[str] = None, 
                     status: Optional[str] = None) -> List[Task]:
        """
        Filters tasks by pet ID and/or status using single-pass filtering for optimal performance.
        
        Args:
            pet_id: Filter by specific pet (optional)
            status: Filter by status - "pending", "completed", "overdue" (optional)
            
        Returns:
            List of tasks matching the filter criteria.
        """
        now = datetime.now()
        return [
            task for task in self.retrieve_tasks()
            if (not pet_id or task.pet_id == pet_id) and (
                not status or (
                    (status.lower() == "pending" and not task.is_completed and task.due_time >= now) or
                    (status.lower() == "completed" and task.is_completed) or
                    (status.lower() == "overdue" and not task.is_completed and task.due_time < now)
                )
            )
        ]
    
    def get_pet_status_summary(self, pet_id: str) -> dict:
        """
        Returns a summary of task statuses for a specific pet.
        Uses single-pass iteration for optimal performance.
        
        Returns:
            Dictionary with counts of pending, completed, and overdue tasks.
        """
        pet_tasks = self.filter_tasks(pet_id=pet_id)
        current_time = datetime.now()
        
        # Single-pass counting instead of iterating three times
        pending = completed = overdue = 0
        for task in pet_tasks:
            if task.is_completed:
                completed += 1
            elif task.due_time >= current_time:
                pending += 1
            else:
                overdue += 1
        
        return {
            "pet_id": pet_id,
            "pending": pending,
            "completed": completed,
            "overdue": overdue,
            "total": len(pet_tasks)
        }
    
    # ==================== RECURRING TASKS ====================
    
    def is_recurring_task(self, task_id: str) -> bool:
        """Checks if a task is recurring."""
        task = self._find_task_by_id(task_id)
        return task.is_recurring() if task else False
    
    def generate_recurring_instances(self, task_id: str, 
                                    num_instances: int = 4) -> List[Task]:
        """
        Generates future instances of a recurring task using dictionary-based frequency mapping.
        
        Args:
            task_id: ID of the recurring task
            num_instances: Number of instances to generate (default: 4)
            
        Returns:
            List of generated task instances.
        """
        original_task = self._find_task_by_id(task_id)
        if not original_task or not original_task.is_recurring():
            return []
        
        # Frequency to timedelta multiplier mapping for cleaner logic
        freq_multipliers = {"daily": 1, "weekly": 7, "monthly": 30}
        multiplier = freq_multipliers.get(original_task.frequency)
        
        if multiplier is None:
            return []
        
        return [
            Task(
                task_id=f"{task_id}_instance_{i}",
                description=original_task.description,
                due_time=original_task.due_time + timedelta(days=multiplier * i),
                frequency=original_task.frequency,
                pet_id=original_task.pet_id,
                is_completed=False,
                parent_task_id=task_id
            )
            for i in range(1, num_instances + 1)
        ]
    
    def reschedule_recurring_task(self, task_id: str, 
                                 new_frequency: str) -> bool:
        """
        Updates the frequency of a recurring task.
        
        Args:
            task_id: ID of the recurring task
            new_frequency: New frequency ("once", "daily", "weekly", "monthly")
            
        Returns:
            True if successful, False otherwise.
        """
        task = self._find_task_by_id(task_id)
        if not task:
            return False
        
        valid_frequencies = ["once", "daily", "weekly", "monthly"]
        if new_frequency not in valid_frequencies:
            return False
        
        task.frequency = new_frequency
        return True
    
    # ==================== SCHEDULING CONFLICTS ====================
    
    def detect_conflicts(self, pet_id: str, 
                        time_window_minutes: int = 30) -> List[Tuple[Task, Task]]:
        """
        Detects scheduling conflicts for a specific pet using O(n) algorithm.
        
        Only checks adjacent tasks since list is sorted by time.
        Conflicts are detected when two tasks are scheduled within 
        the specified time window of each other.
        
        Args:
            pet_id: Pet ID to check for conflicts
            time_window_minutes: Time window for conflict detection (default: 30)
            
        Returns:
            List of tuples containing conflicting task pairs.
        """
        pet_tasks = sorted(self.filter_tasks(pet_id=pet_id, status="pending"), 
                          key=lambda task: task.due_time)
        
        # O(n) algorithm: only check adjacent tasks
        return [
            (pet_tasks[i], pet_tasks[i+1])
            for i in range(len(pet_tasks) - 1)
            if (pet_tasks[i+1].due_time - pet_tasks[i].due_time).total_seconds() / 60 <= time_window_minutes
        ]
    
    def get_conflict_report(self, time_window_minutes: int = 30) -> dict:
        """
        Generates a conflict report for all pets.
        
        Returns:
            Dictionary with conflict information for each pet.
        """
        report = {}
        for pet in self.owner.get_all_pets():
            conflicts = self.detect_conflicts(pet.pet_id, time_window_minutes)
            if conflicts:
                report[pet.pet_id] = {
                    "pet_name": pet.name,
                    "conflict_count": len(conflicts),
                    "conflicts": [
                        {
                            "task1": conflict[0].description,
                            "task2": conflict[1].description,
                            "time1": conflict[0].due_time.isoformat(),
                            "time2": conflict[1].due_time.isoformat()
                        }
                        for conflict in conflicts
                    ]
                }
        
        return report
    
    def check_and_warn_conflicts(self, time_window_minutes: int = 30) -> bool:
        """
        Checks for scheduling conflicts across all pets and prints warning messages.
        Does NOT crash the program - only displays warnings.
        
        Args:
            time_window_minutes: Time window for conflict detection (default: 30)
            
        Returns:
            True if conflicts found, False otherwise.
        """
        conflicts_found = False
        
        for pet in self.owner.get_all_pets():
            conflicts = self.detect_conflicts(pet.pet_id, time_window_minutes)
            
            if conflicts:
                conflicts_found = True
                print(f"\n⚠️  SCHEDULING CONFLICT WARNING for {pet.name}!")
                print(f"   Found {len(conflicts)} conflict(s):")
                
                for task1, task2 in conflicts:
                    time_diff = abs((task1.due_time - task2.due_time).total_seconds() / 60)
                    print(f"   • '{task1.description}' at {task1.due_time.strftime('%H:%M')}")
                    print(f"     conflicts with")
                    print(f"     '{task2.description}' at {task2.due_time.strftime('%H:%M')}")
                    print(f"     (only {time_diff:.0f} minute(s) apart)\n")
        
        return conflicts_found
    
    def find_available_slot(self, pet_id: str, duration_minutes: int = 30, 
                           start_time: Optional[datetime] = None) -> Optional[datetime]:
        """
        Finds the next available time slot for a pet task.
        
        Args:
            pet_id: Pet ID
            duration_minutes: Duration needed for the task
            start_time: Time to start searching from (default: now)
            
        Returns:
            Available datetime slot, or None if not found.
        """
        if not start_time:
            start_time = datetime.now()
        
        pet_tasks = self.filter_tasks(pet_id=pet_id, status="pending")
        pet_tasks.sort(key=lambda task: task.due_time)
        
        # Search for a 2-hour window starting from start_time
        search_time = start_time
        search_end = start_time + timedelta(hours=24)
        
        while search_time < search_end:
            # Check if this slot is free
            is_free = True
            for task in pet_tasks:
                task_start = task.due_time
                task_end = task_start + timedelta(minutes=30)  # Assume 30-min default task duration
                
                if not (search_time + timedelta(minutes=duration_minutes) <= task_start or 
                        search_time >= task_end):
                    is_free = False
                    search_time = task_end
                    break
            
            if is_free:
                return search_time
            
            # Move to next 15-minute slot
            search_time += timedelta(minutes=15)
        
        return None
    
    # ==================== AUTOMATIC TASK RESCHEDULING ====================
    
    def complete_task_with_reschedule(self, task_id: str) -> bool:
        """
        Marks a task as complete and automatically reschedules it if it's a daily recurring task.
        
        For daily tasks, a new instance is created for the next day using timedelta 
        for accurate date calculation.
        
        Args:
            task_id: ID of the task to complete
            
        Returns:
            True if task was marked complete successfully, False if task not found.
        """
        task = self._find_task_by_id(task_id)
        if not task:
            return False
        
        # Mark the current task as complete
        task.mark_complete()
        
        # If it's a daily recurring task, create and add a new instance for tomorrow
        if task.frequency == "daily":
            # Calculate next day's due time using timedelta
            next_due_time = task.due_time + timedelta(days=1)
            
            # Create new task instance for tomorrow
            new_task = Task(
                task_id=f"{task_id}_next",
                description=task.description,
                due_time=next_due_time,
                frequency=task.frequency,
                pet_id=task.pet_id,
                is_completed=False,
                parent_task_id=task_id
            )
            
            # Find the pet and add the new task
            pet = self.owner._find_pet_by_id(task.pet_id)
            if pet:
                pet.add_task(new_task)
        
        return True
    
    # ==================== UTILITY METHODS ====================
    
    def _find_task_by_id(self, task_id: str) -> Optional[Task]:
        """Helper method to find a task by ID across all pets."""
        for task in self.retrieve_tasks():
            if task.task_id == task_id:
                return task
        return None

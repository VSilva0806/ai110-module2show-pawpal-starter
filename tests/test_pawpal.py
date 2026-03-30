"""
Unit tests for PawPal+ System
Tests core functionality of Task, Pet, Owner, and Scheduler classes.
"""

import unittest
from datetime import datetime
from sys import path
from os.path import dirname, abspath

# Add parent directory to path for imports
path.insert(0, abspath(dirname(__file__) + '/..'))

from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion(unittest.TestCase):
    """Test suite for Task completion functionality."""
    
    def setUp(self):
        """Create a task for testing."""
        self.task = Task(
            task_id="test_task_001",
            description="Test task",
            due_time=datetime(2026, 3, 29, 10, 0),
            frequency="daily",
            is_completed=False
        )
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's is_completed status."""
        # Initial state should be incomplete
        self.assertFalse(self.task.is_completed, "Task should initially be incomplete")
        
        # Mark task as complete
        self.task.mark_complete()
        
        # Verify status changed
        self.assertTrue(self.task.is_completed, "Task should be marked as complete")
    
    def test_task_details_reflect_completion(self):
        """Verify that task details update to show completion status."""
        # Get details before completion
        details_before = self.task.get_details()
        self.assertIn("⏳ Pending", details_before, "Pending task should show pending status")
        
        # Mark complete
        self.task.mark_complete()
        
        # Get details after completion
        details_after = self.task.get_details()
        self.assertIn("✓ Complete", details_after, "Completed task should show complete status")


class TestTaskAddition(unittest.TestCase):
    """Test suite for Task addition to Pet functionality."""
    
    def setUp(self):
        """Create a pet and tasks for testing."""
        self.pet = Pet(
            pet_id="test_pet_001",
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            age=3
        )
        
        self.task1 = Task(
            task_id="task_001",
            description="Feed Buddy",
            due_time=datetime(2026, 3, 29, 8, 0),
            frequency="daily"
        )
        
        self.task2 = Task(
            task_id="task_002",
            description="Walk Buddy",
            due_time=datetime(2026, 3, 29, 18, 0),
            frequency="daily"
        )
    
    def test_add_single_task_increases_count(self):
        """Verify that adding a task to a Pet increases the task count."""
        # Initial task count should be 0
        initial_count = len(self.pet.get_tasks())
        self.assertEqual(initial_count, 0, "Pet should have no tasks initially")
        
        # Add a task
        self.pet.add_task(self.task1)
        
        # Verify count increased
        new_count = len(self.pet.get_tasks())
        self.assertEqual(new_count, 1, "Pet should have 1 task after adding")
    
    def test_add_multiple_tasks_increases_count(self):
        """Verify that adding multiple tasks increases the count correctly."""
        # Add first task
        self.pet.add_task(self.task1)
        self.assertEqual(len(self.pet.get_tasks()), 1, "Pet should have 1 task")
        
        # Add second task
        self.pet.add_task(self.task2)
        self.assertEqual(len(self.pet.get_tasks()), 2, "Pet should have 2 tasks")
    
    def test_added_task_is_retrievable(self):
        """Verify that added tasks can be retrieved from the pet."""
        # Add task
        self.pet.add_task(self.task1)
        
        # Retrieve tasks
        tasks = self.pet.get_tasks()
        
        # Verify the task is in the list
        self.assertIn(self.task1, tasks, "Added task should be retrievable")
        self.assertEqual(tasks[0].task_id, "task_001", "Task ID should match")


class TestRemoveTask(unittest.TestCase):
    """Test suite for Task removal from Pet."""
    
    def setUp(self):
        """Create a pet with tasks for testing."""
        self.pet = Pet(
            pet_id="test_pet_001",
            name="Whiskers",
            species="Cat",
            breed="Siamese",
            age=2
        )
        
        self.task1 = Task(
            task_id="task_001",
            description="Feed Whiskers",
            due_time=datetime(2026, 3, 29, 8, 0),
            frequency="daily"
        )
        
        self.task2 = Task(
            task_id="task_002",
            description="Clean litter box",
            due_time=datetime(2026, 3, 29, 19, 0),
            frequency="daily"
        )
        
        self.pet.add_task(self.task1)
        self.pet.add_task(self.task2)
    
    def test_remove_task_decreases_count(self):
        """Verify that removing a task decreases the pet's task count."""
        # Initial count should be 2
        initial_count = len(self.pet.get_tasks())
        self.assertEqual(initial_count, 2, "Pet should have 2 tasks initially")
        
        # Remove a task
        success = self.pet.remove_task("task_001")
        
        # Verify removal was successful
        self.assertTrue(success, "Task removal should return True")
        
        # Verify count decreased
        new_count = len(self.pet.get_tasks())
        self.assertEqual(new_count, 1, "Pet should have 1 task after removal")
    
    def test_remove_nonexistent_task_returns_false(self):
        """Verify that removing a nonexistent task returns False."""
        success = self.pet.remove_task("nonexistent_task")
        self.assertFalse(success, "Removing nonexistent task should return False")


if __name__ == "__main__":
    unittest.main()

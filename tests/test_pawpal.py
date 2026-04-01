"""
Unit tests for PawPal+ System
Tests core functionality of Task, Pet, Owner, and Scheduler classes.
"""

import unittest
from datetime import datetime, timedelta
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


class TestSchedulerSorting(unittest.TestCase):
    """Test suite for Scheduler sorting functionality."""
    
    def setUp(self):
        """Create owner, pets, and tasks for sorting tests."""
        self.owner = Owner(owner_id="owner_001", owner_name="Alice")
        self.pet = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Lab",
            age=4
        )
        self.owner.add_pet(self.pet)
        self.scheduler = Scheduler(owner=self.owner)
    
    def test_sorting_chronological_order_ascending(self):
        """Verify tasks are returned in chronological order (earliest first)."""
        # Add tasks in non-chronological order
        task_3pm = Task(
            task_id="task_003",
            description="Afternoon walk",
            due_time=datetime(2026, 3, 29, 15, 0),
            frequency="once"
        )
        
        task_9am = Task(
            task_id="task_001",
            description="Morning feed",
            due_time=datetime(2026, 3, 29, 9, 0),
            frequency="once"
        )
        
        task_6pm = Task(
            task_id="task_004",
            description="Evening feed",
            due_time=datetime(2026, 3, 29, 18, 0),
            frequency="once"
        )
        
        task_noon = Task(
            task_id="task_002",
            description="Midday play",
            due_time=datetime(2026, 3, 29, 12, 0),
            frequency="once"
        )
        
        self.pet.add_task(task_3pm)
        self.pet.add_task(task_9am)
        self.pet.add_task(task_6pm)
        self.pet.add_task(task_noon)
        
        # Get organized tasks (sorted ascending)
        sorted_tasks = self.scheduler.organize_tasks()
        
        # Verify correct chronological order
        self.assertEqual(len(sorted_tasks), 4, "Should have 4 tasks")
        self.assertEqual(sorted_tasks[0].description, "Morning feed", "First task should be 9am")
        self.assertEqual(sorted_tasks[1].description, "Midday play", "Second task should be 12pm")
        self.assertEqual(sorted_tasks[2].description, "Afternoon walk", "Third task should be 3pm")
        self.assertEqual(sorted_tasks[3].description, "Evening feed", "Fourth task should be 6pm")
    
    def test_sorting_excludes_completed_tasks(self):
        """Verify that completed tasks are excluded from sorted results."""
        task1 = Task(
            task_id="task_001",
            description="Task 1",
            due_time=datetime(2026, 3, 29, 10, 0),
            frequency="once"
        )
        
        task2 = Task(
            task_id="task_002",
            description="Task 2",
            due_time=datetime(2026, 3, 29, 14, 0),
            frequency="once"
        )
        
        self.pet.add_task(task1)
        self.pet.add_task(task2)
        
        # Mark first task as completed
        task1.mark_complete()
        
        # Organize tasks
        sorted_tasks = self.scheduler.organize_tasks()
        
        # Verify only pending task is returned
        self.assertEqual(len(sorted_tasks), 1, "Should have 1 pending task")
        self.assertEqual(sorted_tasks[0].task_id, "task_002", "Only incomplete task should be included")
    
    def test_sorting_identical_times(self):
        """Verify that tasks with identical times are handled correctly."""
        task1 = Task(
            task_id="task_001",
            description="Task A",
            due_time=datetime(2026, 3, 29, 10, 0),
            frequency="once"
        )
        
        task2 = Task(
            task_id="task_002",
            description="Task B",
            due_time=datetime(2026, 3, 29, 10, 0),
            frequency="once"
        )
        
        self.pet.add_task(task1)
        self.pet.add_task(task2)
        
        # Sort tasks
        sorted_tasks = self.scheduler.organize_tasks()
        
        # Verify both are present
        self.assertEqual(len(sorted_tasks), 2, "Both tasks should be present")
        self.assertEqual(sorted_tasks[0].due_time, sorted_tasks[1].due_time, "Both should have same time")
    
    def test_sorting_empty_task_list(self):
        """Verify that sorting an empty task list returns an empty list."""
        sorted_tasks = self.scheduler.organize_tasks()
        
        self.assertEqual(len(sorted_tasks), 0, "Empty task list should return empty list")
        self.assertIsInstance(sorted_tasks, list, "Should return a list")


class TestRecurrenceLogic(unittest.TestCase):
    """Test suite for recurring task functionality."""
    
    def setUp(self):
        """Create owner, pets, and tasks for recurrence tests."""
        self.owner = Owner(owner_id="owner_001", owner_name="Bob")
        self.pet = Pet(
            pet_id="pet_001",
            name="Bella",
            species="Cat",
            breed="Persian",
            age=2
        )
        self.owner.add_pet(self.pet)
        self.scheduler = Scheduler(owner=self.owner)
    
    def test_generate_recurring_instances_daily_task(self):
        """Verify that daily recurring task generates correct instances with proper spacing."""
        daily_task = Task(
            task_id="daily_feed",
            description="Feed Bella",
            due_time=datetime(2026, 3, 29, 8, 0),
            frequency="daily"
        )
        
        self.pet.add_task(daily_task)
        
        # Generate 3 instances
        instances = self.scheduler.generate_recurring_instances("daily_feed", num_instances=3)
        
        # Verify correct number of instances
        self.assertEqual(len(instances), 3, "Should generate 3 instances")
        
        # Verify each instance is 1 day apart
        self.assertEqual(instances[0].due_time, datetime(2026, 3, 30, 8, 0), "First instance should be day 1")
        self.assertEqual(instances[1].due_time, datetime(2026, 3, 31, 8, 0), "Second instance should be day 2")
        self.assertEqual(instances[2].due_time, datetime(2026, 4, 1, 8, 0), "Third instance should be day 3")
    
    def test_generate_recurring_instances_weekly_task(self):
        """Verify that weekly recurring task generates instances 7 days apart."""
        weekly_task = Task(
            task_id="weekly_vet",
            description="Vet checkup",
            due_time=datetime(2026, 3, 29, 10, 0),
            frequency="weekly"
        )
        
        self.pet.add_task(weekly_task)
        
        # Generate 2 instances
        instances = self.scheduler.generate_recurring_instances("weekly_vet", num_instances=2)
        
        # Verify spacing
        self.assertEqual(len(instances), 2, "Should generate 2 instances")
        self.assertEqual(instances[0].due_time, datetime(2026, 4, 5, 10, 0), "First instance should be 7 days later")
        self.assertEqual(instances[1].due_time, datetime(2026, 4, 12, 10, 0), "Second instance should be 14 days later")
    
    def test_parent_task_reference_in_instances(self):
        """Verify that generated instances correctly reference the parent task."""
        parent_task = Task(
            task_id="parent_001",
            description="Play session",
            due_time=datetime(2026, 3, 29, 16, 0),
            frequency="daily"
        )
        
        self.pet.add_task(parent_task)
        
        # Generate instances
        instances = self.scheduler.generate_recurring_instances("parent_001", num_instances=2)
        
        # Verify parent task references
        for instance in instances:
            self.assertEqual(instance.parent_task_id, "parent_001", "Instance should reference parent task")
    
    def test_non_recurring_task_returns_empty(self):
        """Verify that generating instances for a non-recurring task returns empty list."""
        once_task = Task(
            task_id="once_groom",
            description="Groom Bella",
            due_time=datetime(2026, 3, 29, 14, 0),
            frequency="once"
        )
        
        self.pet.add_task(once_task)
        
        # Try to generate instances
        instances = self.scheduler.generate_recurring_instances("once_groom", num_instances=3)
        
        self.assertEqual(len(instances), 0, "Non-recurring task should return empty list")
    
    def test_nonexistent_task_returns_empty(self):
        """Verify that generating instances for non-existent task returns empty list."""
        instances = self.scheduler.generate_recurring_instances("nonexistent_task", num_instances=3)
        
        self.assertEqual(len(instances), 0, "Non-existent task should return empty list")


class TestConflictDetection(unittest.TestCase):
    """Test suite for scheduling conflict detection."""
    
    def setUp(self):
        """Create owner, pets, and tasks for conflict detection tests."""
        self.owner = Owner(owner_id="owner_001", owner_name="Charlie")
        self.pet = Pet(
            pet_id="pet_001",
            name="Daisy",
            species="Dog",
            breed="Poodle",
            age=5
        )
        self.owner.add_pet(self.pet)
        self.scheduler = Scheduler(owner=self.owner)
    
    def test_detect_tasks_at_same_time(self):
        """Verify that tasks scheduled at identical times are detected as conflicts."""
        # Use future time to ensure tasks are pending, not overdue
        future_time = datetime.now() + timedelta(hours=2)
        
        task1 = Task(
            task_id="task_001",
            description="Walk",
            due_time=future_time,
            frequency="once"
        )
        
        task2 = Task(
            task_id="task_002",
            description="Feed",
            due_time=future_time,
            frequency="once"
        )
        
        self.pet.add_task(task1)
        self.pet.add_task(task2)
        
        # Detect conflicts with 30-minute window
        conflicts = self.scheduler.detect_conflicts("pet_001", time_window_minutes=30)
        
        self.assertEqual(len(conflicts), 1, "Should detect 1 conflict")
        self.assertEqual(conflicts[0][0].task_id, "task_001", "First task in conflict should be task_001")
        self.assertEqual(conflicts[0][1].task_id, "task_002", "Second task in conflict should be task_002")
    
    def test_detect_conflicts_within_time_window(self):
        """Verify that tasks within the time window are flagged as conflicts."""
        # Use future time to ensure tasks are pending, not overdue
        future_time = datetime.now() + timedelta(hours=2)
        
        task1 = Task(
            task_id="task_001",
            description="Walk",
            due_time=future_time,
            frequency="once"
        )
        
        task2 = Task(
            task_id="task_002",
            description="Play",
            due_time=future_time + timedelta(minutes=20),
            frequency="once"
        )
        
        self.pet.add_task(task1)
        self.pet.add_task(task2)
        
        # 20 minutes apart, should conflict in 30-minute window
        conflicts = self.scheduler.detect_conflicts("pet_001", time_window_minutes=30)
        
        self.assertEqual(len(conflicts), 1, "Should detect conflict within 30-minute window")
    
    def test_no_conflict_outside_time_window(self):
        """Verify that tasks outside the time window are not flagged as conflicts."""
        # Use future time to ensure tasks are pending, not overdue
        future_time = datetime.now() + timedelta(hours=2)
        
        task1 = Task(
            task_id="task_001",
            description="Walk",
            due_time=future_time,
            frequency="once"
        )
        
        task2 = Task(
            task_id="task_002",
            description="Groom",
            due_time=future_time + timedelta(minutes=45),
            frequency="once"
        )
        
        self.pet.add_task(task1)
        self.pet.add_task(task2)
        
        # 45 minutes apart, should NOT conflict in 30-minute window
        conflicts = self.scheduler.detect_conflicts("pet_001", time_window_minutes=30)
        
        self.assertEqual(len(conflicts), 0, "Should not detect conflict outside 30-minute window")
    
    def test_conflicts_exclude_completed_tasks(self):
        """Verify that completed tasks are excluded from conflict detection."""
        # Use future time to ensure tasks are pending, not overdue
        future_time = datetime.now() + timedelta(hours=2)
        
        task1 = Task(
            task_id="task_001",
            description="Walk",
            due_time=future_time,
            frequency="once"
        )
        
        task2 = Task(
            task_id="task_002",
            description="Feed",
            due_time=future_time,
            frequency="once"
        )
        
        self.pet.add_task(task1)
        self.pet.add_task(task2)
        
        # Mark first task as completed
        task1.mark_complete()
        
        # Detect conflicts
        conflicts = self.scheduler.detect_conflicts("pet_001", time_window_minutes=30)
        
        self.assertEqual(len(conflicts), 0, "Completed tasks should not create conflicts")
    
    def test_no_conflicts_for_empty_pet(self):
        """Verify that a pet with no tasks returns no conflicts."""
        conflicts = self.scheduler.detect_conflicts("pet_001", time_window_minutes=30)
        
        self.assertEqual(len(conflicts), 0, "Pet with no tasks should have no conflicts")
    
    def test_no_conflicts_for_single_task(self):
        """Verify that a pet with single task has no conflicts."""
        # Use future time to ensure task is pending, not overdue
        future_time = datetime.now() + timedelta(hours=2)
        
        task1 = Task(
            task_id="task_001",
            description="Walk",
            due_time=future_time,
            frequency="once"
        )
        
        self.pet.add_task(task1)
        
        conflicts = self.scheduler.detect_conflicts("pet_001", time_window_minutes=30)
        
        self.assertEqual(len(conflicts), 0, "Single task should have no conflicts")


if __name__ == "__main__":
    unittest.main()

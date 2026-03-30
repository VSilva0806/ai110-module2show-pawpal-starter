"""
PawPal+ Main Script
Demo script showcasing the pet care scheduling system.
"""

from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an owner
    owner = Owner(owner_id="owner_001", owner_name="Sarah")
    
    # Create pets
    buddy = Pet(pet_id="pet_001", name="Buddy", species="Dog", breed="Golden Retriever", age=3)
    whiskers = Pet(pet_id="pet_002", name="Whiskers", species="Cat", breed="Siamese", age=2)
    
    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    
    # Create tasks with different times
    now = datetime.now()
    
    # Buddy's tasks
    task1 = Task(
        task_id="task_001",
        description="Feed Buddy breakfast",
        due_time=now.replace(hour=8, minute=0),
        frequency="daily"
    )
    
    task2 = Task(
        task_id="task_002",
        description="Walk Buddy in the park",
        due_time=now.replace(hour=10, minute=30),
        frequency="daily"
    )
    
    task3 = Task(
        task_id="task_003",
        description="Give Buddy medication",
        due_time=now.replace(hour=14, minute=0),
        frequency="daily"
    )
    
    # Whiskers' task
    task4 = Task(
        task_id="task_004",
        description="Feed Whiskers dinner",
        due_time=now.replace(hour=18, minute=0),
        frequency="daily"
    )
    
    task5 = Task(
        task_id="task_005",
        description="Clean Whiskers' litter box",
        due_time=now.replace(hour=19, minute=0),
        frequency="daily"
    )
    
    # Add tasks to pets
    buddy.add_task(task1)
    buddy.add_task(task2)
    buddy.add_task(task3)
    whiskers.add_task(task4)
    whiskers.add_task(task5)
    
    # Create scheduler
    scheduler = Scheduler(owner=owner)
    
    # Print today's schedule
    print("\n" + "="*70)
    print(f"🐾 TODAY'S SCHEDULE FOR {owner.owner_name.upper()}")
    print("="*70)
    
    organized_tasks = scheduler.organize_tasks()
    
    if not organized_tasks:
        print("No pending tasks for today!")
    else:
        for i, task in enumerate(organized_tasks, 1):
            # Find which pet this task belongs to
            pet_name = "Unknown"
            for pet in owner.get_all_pets():
                if task in pet.get_tasks():
                    pet_name = pet.name
                    break
            
            time_str = task.due_time.strftime("%H:%M")
            status = "✓" if task.is_completed else "•"
            print(f"{i}. [{status}] {time_str} - {task.description} ({pet_name})")
    
    print("\n" + "-"*70)
    print(f"Total Tasks: {len(organized_tasks)} | Pets: {len(owner.get_all_pets())}")
    print("-"*70 + "\n")
    
    # Mark a task as complete
    task1.mark_complete()
    print(f"✓ Marked '{task1.description}' as complete!\n")
    
    # Show updated schedule
    print("="*70)
    print("UPDATED SCHEDULE (Pending Tasks Only)")
    print("="*70)
    updated_tasks = scheduler.organize_tasks()
    
    for i, task in enumerate(updated_tasks, 1):
        pet_name = "Unknown"
        for pet in owner.get_all_pets():
            if task in pet.get_tasks():
                pet_name = pet.name
                break
        
        time_str = task.due_time.strftime("%H:%M")
        print(f"{i}. {time_str} - {task.description} ({pet_name})")
    
    print("\n")


if __name__ == "__main__":
    main()

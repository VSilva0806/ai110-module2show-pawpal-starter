import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler, TaskPriority, TaskType
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant — manage pets, schedule tasks, and track care.")

st.divider()

# Initialize session state objects (persist across reruns)
if "owner" not in st.session_state:
    # Try to load from data.json first
    loaded_owner = Owner.load_from_json("data.json")
    if loaded_owner:
        st.session_state.owner = loaded_owner
        st.success("📂 Loaded previous data!")
    else:
        st.session_state.owner = Owner(owner_id="owner_001", owner_name="Jordan")

if "pets" not in st.session_state:
    st.session_state.pets = {}

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

# Save data to JSON after any changes
def save_data():
    """Saves current state to data.json"""
    st.session_state.owner.save_to_json("data.json")

st.subheader("Owner & Pet Setup")

# Owner settings
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.owner_name)
    if owner_name != st.session_state.owner.owner_name:
        st.session_state.owner.owner_name = owner_name
        save_data()

with col2:
    st.info(f"Owner ID: {st.session_state.owner.owner_id}")

st.markdown("### Pet Management")

# Add new pet
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit"])
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    pet_id = f"pet_{len(st.session_state.pets) + 1:03d}"
    new_pet = Pet(pet_id=pet_id, name=pet_name, species=species, breed="Unspecified", age=age)
    st.session_state.owner.add_pet(new_pet)
    st.session_state.pets[pet_id] = new_pet
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)  # Refresh scheduler
    save_data()
    st.success(f"✓ Added {pet_name}!")

# Display current pets
if st.session_state.owner.get_all_pets():
    st.write("### Current Pets")
    for pet in st.session_state.owner.get_all_pets():
        st.write(f"🐾 **{pet.name}** — {pet.get_pet_info()}")

st.markdown("### Task Management")

# Select pet for task
pets = st.session_state.owner.get_all_pets()
if pets:
    pet_options = {pet.name: pet for pet in pets}
    selected_pet_name = st.selectbox("Select pet for task", list(pet_options.keys()))
    selected_pet = pet_options[selected_pet_name]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        hour_options = list(range(24))
        task_hour = st.selectbox("Hour", hour_options, index=8, format_func=lambda x: f"{x % 12 or 12}:00 {'AM' if x < 12 else 'PM'}")
    with col3:
        minute_options = list(range(0, 60, 5))  # 0, 5, 10, 15, ..., 55
        task_minute = st.selectbox("Minute", minute_options, index=0, format_func=lambda x: f"{x:02d}")
    
    col1, col2 = st.columns(2)
    with col1:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"])
    with col2:
        priority_options = ["Low", "Medium", "High"]
        priority_index = st.selectbox("Priority", priority_options, index=1)
        priority_map = {"Low": TaskPriority.LOW, "Medium": TaskPriority.MEDIUM, "High": TaskPriority.HIGH}
        selected_priority = priority_map[priority_index]
    
    col1, col2 = st.columns(2)
    with col1:
        task_type_options = [f"{tt.get_emoji()} {tt.get_label()}" for tt in TaskType]
        task_type_index = st.selectbox("Task Type", task_type_options, index=11)  # Default to "Other"
        # Find matching task type by comparing emoji + label
        selected_task_type = TaskType.OTHER
        for tt in TaskType:
            if f"{tt.get_emoji()} {tt.get_label()}" == task_type_index:
                selected_task_type = tt
                break
    
    if st.button("Add Task"):
        task_id = f"task_{len(selected_pet.get_tasks()) + 1:03d}"
        due_time = datetime.now().replace(hour=task_hour, minute=task_minute, second=0, microsecond=0)
        new_task = Task(
            task_id=task_id,
            description=task_title,
            due_time=due_time,
            frequency=frequency,
            priority=selected_priority,
            task_type=selected_task_type
        )
        selected_pet.add_task(new_task)
        st.session_state.scheduler = Scheduler(owner=st.session_state.owner)  # Refresh scheduler
        save_data()
        st.success(f"✓ Added task '{task_title}' for {selected_pet.name}!")
else:
    st.info("Add a pet first to create tasks.")

st.markdown("### Task Dashboard")

# Check for scheduling conflicts across all pets
conflict_report = st.session_state.scheduler.get_conflict_report(time_window_minutes=30)
if conflict_report:
    for pet_id, conflict_info in conflict_report.items():
        st.warning(
            f"⚠️ **Scheduling Conflict Detected for {conflict_info['pet_name']}!** "
            f"({conflict_info['conflict_count']} conflict(s) found)"
        )
        # Display conflict details
        conflict_details = []
        for conflict in conflict_info['conflicts']:
            task1_time = datetime.fromisoformat(conflict['time1']).strftime('%I:%M %p')
            task2_time = datetime.fromisoformat(conflict['time2']).strftime('%I:%M %p')
            conflict_details.append({
                "Task 1": conflict['task1'],
                "Time 1": task1_time,
                "Task 2": conflict['task2'],
                "Time 2": task2_time
            })
        if conflict_details:
            st.dataframe(pd.DataFrame(conflict_details), use_container_width=True)

# Display organized tasks by category
all_tasks = st.session_state.owner.get_all_tasks()

if all_tasks:
    # Task summary metrics  
    col1, col2, col3, col4 = st.columns(4)
    pending_tasks = [t for t in all_tasks if not t.is_completed]
    completed_tasks = [t for t in all_tasks if t.is_completed]
    overdue_tasks = st.session_state.scheduler.get_overdue_tasks()
    
    with col1:
        st.metric("Pending Tasks", len(pending_tasks))
    with col2:
        st.metric("Completed Tasks", len(completed_tasks))
    with col3:
        st.metric("Overdue Tasks", len(overdue_tasks))
    with col4:
        st.metric("Total Tasks", len(all_tasks))
    
    st.divider()
    
    # Today's tasks
    today_tasks = st.session_state.scheduler.get_today_tasks()
    if today_tasks:
        st.subheader("📅 Today's Tasks")
        today_df = pd.DataFrame([
            {
                "Task": task.description,
                "Type": f"{task.task_type.get_emoji()} {task.task_type}",
                "Pet": next((p.name for p in st.session_state.owner.get_all_pets() if p.pet_id == task.pet_id), "—"),
                "Time": task.due_time.strftime('%I:%M %p'),
                "Priority": f"{task.priority.get_emoji()} {task.priority}",
                "Frequency": task.frequency,
                "Status": "✓ Complete" if task.is_completed else "⏳ Pending"
            }
            for task in sorted(today_tasks, key=lambda t: t.due_time)
        ])
        st.table(today_df)
    
    # Upcoming tasks (next 7 days)
    upcoming_tasks = st.session_state.scheduler.get_upcoming_tasks(days=7)
    if upcoming_tasks:
        st.subheader("📆 Upcoming Tasks (Next 7 Days)")
        upcoming_df = pd.DataFrame([
            {
                "Task": task.description,
                "Type": f"{task.task_type.get_emoji()} {task.task_type}",
                "Pet": next((p.name for p in st.session_state.owner.get_all_pets() if p.pet_id == task.pet_id), "—"),
                "Due Date": task.due_time.strftime('%Y-%m-%d'),
                "Time": task.due_time.strftime('%I:%M %p'),
                "Priority": f"{task.priority.get_emoji()} {task.priority}",
                "Frequency": task.frequency
            }
            for task in upcoming_tasks
        ])
        st.table(upcoming_df)
    
    # Overdue tasks with warning
    if overdue_tasks:
        st.subheader("🚨 Overdue Tasks")
        overdue_df = pd.DataFrame([
            {
                "Task": task.description,
                "Type": f"{task.task_type.get_emoji()} {task.task_type}",
                "Pet": next((p.name for p in st.session_state.owner.get_all_pets() if p.pet_id == task.pet_id), "—"),
                "Due Date": task.due_time.strftime('%Y-%m-%d'),
                "Time": task.due_time.strftime('%I:%M %p'),
                "Priority": f"{task.priority.get_emoji()} {task.priority}",
                "Frequency": task.frequency
            }
            for task in overdue_tasks
        ])
        st.warning(f"You have {len(overdue_tasks)} overdue task(s)!")
        st.table(overdue_df)
    
    # All tasks organized by pet
    st.subheader("📋 All Tasks (Organized by Pet)")
    for pet in st.session_state.owner.get_all_pets():
        pet_tasks = st.session_state.scheduler.filter_tasks(pet_id=pet.pet_id)
        if pet_tasks:
            with st.expander(f"🐾 {pet.name} ({len(pet_tasks)} task(s))", expanded=False):
                # Pet status summary
                pet_summary = st.session_state.scheduler.get_pet_status_summary(pet.pet_id)
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric("Pending", pet_summary['pending'])
                with metric_cols[1]:
                    st.metric("Completed", pet_summary['completed'])
                with metric_cols[2]:
                    st.metric("Overdue", pet_summary['overdue'])
                with metric_cols[3]:
                    st.metric("Total", pet_summary['total'])
                
                # Display sorted tasks for this pet (by priority, then time)
                sorted_pet_tasks = sorted(
                    st.session_state.scheduler.filter_tasks(pet_id=pet.pet_id),
                    key=lambda t: (-t.priority.value, t.due_time)
                )
                pet_df = pd.DataFrame([
                    {
                        "Task": task.description,
                        "Type": f"{task.task_type.get_emoji()} {task.task_type}",
                        "Priority": f"{task.priority.get_emoji()} {task.priority}",
                        "Due": task.due_time.strftime('%Y-%m-%d %I:%M %p'),
                        "Frequency": task.frequency,
                        "Status": "✓ Complete" if task.is_completed else "⏳ Pending"
                    }
                    for task in sorted_pet_tasks
                ])
                st.table(pet_df)
else:
    st.info("No tasks yet. Add a pet and create your first task!")

st.divider()

st.subheader("Task Actions")

# Mark a task complete
all_pending = [t for t in st.session_state.owner.get_all_tasks() if not t.is_completed]
if all_pending:
    col1, col2 = st.columns([3, 1])
    with col1:
        task_labels = {f"{t.description} ({next((p.name for p in st.session_state.owner.get_all_pets() if p.pet_id == t.pet_id), '—')})" : t for t in all_pending}
        selected_label = st.selectbox("Select pending task to mark complete", list(task_labels.keys()))
    with col2:
        st.write("")  # Spacer
        if st.button("✓ Mark Complete"):
            task_labels[selected_label].mark_complete()
            save_data()
            st.success(f"✓ Task marked as complete!")
            st.rerun()
else:
    st.success("🎉 All tasks are complete!")

st.divider()

# Delete a task
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    col1, col2 = st.columns([3, 1])
    with col1:
        delete_task_labels = {f"{t.description} ({next((p.name for p in st.session_state.owner.get_all_pets() if p.pet_id == t.pet_id), '—')})" : t for t in all_tasks}
        delete_selected_label = st.selectbox("Select task to delete", list(delete_task_labels.keys()))
    with col2:
        st.write("")  # Spacer
        if st.button("🗑️ Delete Task"):
            task_to_delete = delete_task_labels[delete_selected_label]
            # Find the pet that owns this task and remove it
            for pet in st.session_state.owner.get_all_pets():
                if pet.remove_task(task_to_delete.task_id):
                    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)  # Refresh scheduler
                    save_data()
                    st.success(f"🗑️ Task '{task_to_delete.description}' deleted!")
                    st.rerun()
                    break

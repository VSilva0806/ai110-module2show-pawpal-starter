import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant — manage pets, schedule tasks, and track care.")

st.divider()

# Initialize session state objects (persist across reruns)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="owner_001", owner_name="Jordan")

if "pets" not in st.session_state:
    st.session_state.pets = {}

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

st.subheader("Owner & Pet Setup")

# Owner settings
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.owner_name)
    if owner_name != st.session_state.owner.owner_name:
        st.session_state.owner.owner_name = owner_name

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
        task_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=8)
    with col3:
        task_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)
    
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"])
    
    if st.button("Add Task"):
        task_id = f"task_{len(selected_pet.get_tasks()) + 1:03d}"
        due_time = datetime.now().replace(hour=task_hour, minute=task_minute, second=0, microsecond=0)
        new_task = Task(
            task_id=task_id,
            description=task_title,
            due_time=due_time,
            frequency=frequency
        )
        selected_pet.add_task(new_task)
        st.success(f"✓ Added task '{task_title}' for {selected_pet.name}!")
else:
    st.info("Add a pet first to create tasks.")

# Display all tasks with details
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("### All Tasks")
    for task in all_tasks:
        st.write(f"• {task.get_details()}")
else:
    st.info("No tasks yet.")

st.divider()

st.subheader("Schedule")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Organize Tasks"):
        organized = st.session_state.scheduler.organize_tasks()
        if organized:
            st.write("### Pending (by time)")
            for i, task in enumerate(organized, 1):
                st.write(f"{i}. {task.due_time.strftime('%H:%M')} — {task.description} ({task.frequency})")
        else:
            st.info("No pending tasks.")

with col2:
    if st.button("Show Overdue"):
        overdue = st.session_state.scheduler.get_overdue_tasks()
        if overdue:
            st.write("### Overdue Tasks")
            for task in overdue:
                st.warning(f"⚠ {task.get_details()}")
        else:
            st.success("No overdue tasks.")

with col3:
    if st.button("Show Completed"):
        completed = st.session_state.scheduler.get_completed_tasks()
        if completed:
            st.write("### Completed Tasks")
            for task in completed:
                st.write(f"✓ {task.get_details()}")
        else:
            st.info("No completed tasks yet.")

# Mark a task complete
all_pending = [t for t in st.session_state.owner.get_all_tasks() if not t.is_completed]
if all_pending:
    st.markdown("### Mark Task Complete")
    task_labels = {t.description: t for t in all_pending}
    selected_label = st.selectbox("Select task to mark complete", list(task_labels.keys()))
    if st.button("Mark Complete"):
        task_labels[selected_label].mark_complete()
        st.success(f"✓ '{selected_label}' marked as complete!")

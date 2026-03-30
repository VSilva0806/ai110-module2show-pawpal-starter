import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize session state objects (persist across reruns)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="owner_001", owner_name="Jordan")

if "pets" not in st.session_state:
    st.session_state.pets = {}

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

st.subheader("Quick Demo Inputs")
st.caption("✓ Objects persist across interactions (saved in session_state)")

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
        st.write(f"🐾 **{pet.name}** ({pet.species}, Age {pet.age})")

st.markdown("### Task Management")
st.caption("Add tasks. In your final version, these feed into your scheduler.")

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

# Display tasks
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("### All Tasks")
    for task in all_tasks:
        st.write(f"• {task.description} @ {task.due_time.strftime('%H:%M')} ({task.frequency})")
else:
    st.info("No tasks yet.")

st.divider()

st.subheader("Generate Schedule")
st.caption("Your scheduler organizes tasks by time.")

if st.button("Organize Tasks"):
    organized = st.session_state.scheduler.organize_tasks()
    if organized:
        st.write("### Organized Schedule")
        for i, task in enumerate(organized, 1):
            status = "✓" if task.is_completed else "•"
            st.write(f"{i}. [{status}] {task.due_time.strftime('%H:%M')} - {task.description}")
    else:
        st.info("No pending tasks to organize.")

# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling
The schedular supports advanced task sorting and filtering, allowing users to view tasks by time, pet, and completion. Recurring tasks are supported with the algorithm automatically generating future instances once for daily or weekly tasks once they are finished so that the user does not have to manually input them every time. THe scheduler also supports conflict detection and is able to identify which tasks overlap with which within a certain time window and promptly alerts the user without crashing the app.

## Testing PawPal+
Command to run test: python3 -m pytest

Tests include verification of task completion, task addition and removal, scheduling sorting by chronological ordered. Edge case testing included making sure completed tasks were excluded from scheduling, ensuring identical times and empty task lists were handled, and conflict detection is considered. Recurrence was also tested thouroughly and ensured these recurring tasks were generated with suffice space to allow owner to fulfill parent tasks.

Confidence Level: 4 stars

## PawPal+ Features

Task Sorting by Time — Organize pending tasks by due time
Daily Task View — See all tasks due today
Upcoming Tasks — Preview tasks for the next 7 days
Multi-Pet Management — Handle multiple pets in one account
Task Filtering — Filter by pet and status (pending, completed, overdue)
Recurring Tasks — Support daily, weekly, and monthly recurring tasks with auto-rescheduling
Conflict Detection — Alert when tasks are scheduled within 30 minutes of each other
Available Time Slots — Find open scheduling windows for new tasks
Pet Status Summary — View task counts per pet
Web Interface — User-friendly Streamlit app for managing pets and tasks

##Demo
![alt text](<Screenshot 2026-03-31 at 11.51.31 PM.jpg>)
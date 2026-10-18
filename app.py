import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A simple multi-pet care planner with smart scheduling.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)

with st.sidebar:
    st.header("Household")
    owner.name = st.text_input("Owner name", value=owner.name)
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["dog", "cat", "other"])
        if st.form_submit_button("Add pet"):
            if pet_name.strip() and not any(p.name.lower() == pet_name.strip().lower() for p in owner.pets):
                owner.add_pet(Pet(pet_name.strip(), species))
                st.success(f"Added {pet_name.strip()}.")
            else:
                st.warning("Enter a unique pet name.")

if not owner.pets:
    st.info("Add a pet in the sidebar to begin.")
else:
    st.subheader("Add a care task")
    with st.form("task_form"):
        pet = st.selectbox("Pet", owner.pets, format_func=lambda item: item.name)
        description = st.text_input("Description", value="Morning walk")
        time = st.time_input("Time")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        if st.form_submit_button("Add task"):
            pet.add_task(Task(description, time.strftime("%H:%M"), frequency=frequency, priority=priority))
            st.success("Task added.")

    st.subheader("Today's schedule")
    tasks = scheduler.sort_by_time()
    if tasks:
        st.table([{"Time": t.time, "Pet": t.pet_name, "Task": t.description,
                   "Priority": t.priority, "Status": "Complete" if t.completed else "Open"}
                  for t in tasks])
        for warning in scheduler.find_conflicts(tasks):
            st.warning(warning)
        for task in tasks:
            if not task.completed and st.button(f"Complete: {task.pet_name} — {task.description}", key=id(task)):
                next_task = scheduler.complete_task(task)
                st.success("Completed." if next_task is None else f"Completed. Next occurrence: {next_task.due_date.isoformat()}.")
                st.rerun()
    else:
        st.info("No tasks yet. Add one above.")

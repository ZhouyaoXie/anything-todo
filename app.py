import streamlit as st
import pandas as pd
import numpy as np
from uuid import uuid4  # For generating unique IDs
import time 

# Page configuration
st.set_page_config(
    page_title="Anything To-do",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "Anything To-do"
    }
)

# create sidebar info
st.sidebar.title("about")
st.sidebar.markdown("""
overwhelmed by your to-do list and unable to get started with anything?   
pick one thing at time, anything, and overcome procrastination by committing to do that thing for 5 minutes (yes, just 5 minutes).
that's it.
""")

st.sidebar.title("learn more")
st.sidebar.markdown("""
> [project repo](https://github.com/ZhouyaoXie/anything-todo)  
> [zhouyao's website](https://xiezhouyao.site)  
> [zhouyao's blog](https://zhouyao.substack.com/)  """)

# Function to sort tasks based on priority
def sort_tasks(tasks):
    def sort_key(task):
        important, urgent = task['important'], task['urgent']
        if important and urgent: return 1
        elif important: return 2
        elif urgent: return 3
        else: return 4
    return sorted(tasks, key=sort_key)

# Function to assign equal probabilities to tasks within the same priority group
def assign_probabilities(sorted_tasks):
    groups = pd.DataFrame(sorted_tasks).groupby(['important', 'urgent']).size().to_dict()
    probabilities = []
    for task in sorted_tasks:
        group_size = groups[(task['important'], task['urgent'])]
        # Evenly distribute probability within the group
        probabilities.append(1 / group_size / len(groups))
    # Normalize to ensure the sum of probabilities is 1
    probabilities = np.array(probabilities)
    probabilities /= probabilities.sum()
    return probabilities

def launch_task(sampled_task):
    time.sleep(2)
    msg = st.toast('Let\'s dive right into this: {}'.format(sampled_task))
    time.sleep(2)
    msg.toast('3...')
    time.sleep(1.5)
    msg.toast('2...')
    time.sleep(1.5)
    msg.toast('1...')
    time.sleep(1.5)
    msg.toast('Launch!', icon = "🥂")

# Streamlit UI
st.title('Anything To-do')

st.info("""Overwhelmed by your to-do list and unable to get started with anything? 
Add all your tasks, click "Do Anything", and a task will be picked for you. 
Try to spend the next 5 minutes on that task. When you're done, feel free to continue if you want or come back here again. """, icon = "🍪")

# Use session state to store tasks and form key
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'form_key' not in st.session_state:
    st.session_state.form_key = str(uuid4())

with st.form(key=st.session_state.form_key):
    task_name = st.text_input("What's on your mind right now?", key="task_name")
    important = st.checkbox("Is it important?", key="important")
    urgent = st.checkbox("Is it urgent?", key="urgent")
    submit_button = st.form_submit_button("Add Task")
    
    if submit_button and task_name:
        st.session_state.tasks.append({"id": str(uuid4()), "name": task_name, "important": important, "urgent": urgent})
        # Update form key to reset the form
        st.session_state.form_key = str(uuid4())
        st.experimental_rerun()

if st.session_state.tasks:
    sorted_tasks = sort_tasks(st.session_state.tasks)
    probabilities = assign_probabilities(sorted_tasks)

    st.write("Tasks Added:")
    for task, prob in zip(sorted_tasks, probabilities):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{task['name']} - Important: {task['important']}, Urgent: {task['urgent']}, Probability: {prob:.2f}")
        with col2:
            if st.button("Delete", key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                # Optionally update form key here as well to reset form, if needed
                # st.session_state.form_key = str(uuid4())
                st.experimental_rerun()

    if st.button("Do Anything"):
        sampled_task = np.random.choice([task['name'] for task in sorted_tasks], p=probabilities)
        st.success(f"Anything is: {sampled_task}", icon = "🧋")
        launch_task(sampled_task)
else:
    st.write("No tasks added yet.")

import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
roles = ["Professor", "Associate Professor", "Assistant Professor", "Researcher"]

tasks = ["Research", "Teaching", "Administration", "Community Service"]

# Set Streamlit page configuration
st.set_page_config(page_title="Staff Data Management", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f7fa;
        }
        .title {
            color: #2e3b4e;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 18px;
            padding: 10px;
        }
        .stDataFrame {
            border: 2px solid #4CAF50;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>Staff Data Management</div>", unsafe_allow_html=True)

# Initialize session state for storing staff data
if "staff_data" not in st.session_state:
    st.session_state.staff_data = pd.DataFrame(columns=[
        "Staff ID", "Name", "Role", "Research Papers", "Grants/Funding (Lakh)", "Extra Activities", "Training Hours Attended", "Productive Task", "Non-Productive Task"
    ])

# User Input Form
with st.form("staff_form"):
    st.markdown("### Enter Staff Details")
    staff_id = st.number_input("Staff ID", min_value=10000, max_value=99999, step=1, format="%d")
    name = st.text_input("Name")
    role = st.selectbox("Role", roles)
    research_papers = st.number_input("Research Papers", min_value=0, max_value=50, step=1)
    grants = st.number_input("Grants/Funding (Lakh)", min_value=1, max_value=50, step=1)
    extra_activities = st.text_area("Extra Activities")
    training_hours = st.number_input("Training Hours Attended", min_value=0, max_value=200, step=1)
    productive_task = st.selectbox("Productive Task", tasks)
    non_productive_task = st.text_area("Non-Productive Task")
    submit_button = st.form_submit_button("➕ Add Staff")

# Add data to session state
if submit_button:
    new_entry = pd.DataFrame({
        "Staff ID": [staff_id],
        "Name": [name],
        "Role": [role],
        "Research Papers": [research_papers],
        "Grants/Funding (Lakh)": [grants],
        "Extra Activities": [extra_activities],
        "Training Hours Attended": [training_hours],
        "Productive Task": [productive_task],
        "Non-Productive Task": [non_productive_task]
    })
    st.session_state.staff_data = pd.concat([st.session_state.staff_data, new_entry], ignore_index=True)
    st.success("✅ Staff member added successfully!")

# Search Bar
st.markdown("### 🔍 Search Staff")
search = st.text_input("Search by Name:")
filtered_data = st.session_state.staff_data
if search:
    filtered_data = filtered_data[filtered_data["Name"].str.contains(search, case=False, na=False)]

# Display Data
st.markdown("### 📋 Staff Records")
st.dataframe(filtered_data, height=400)

# CSV Download Button
if not st.session_state.staff_data.empty:
    csv = st.session_state.staff_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="staff_data.csv",
        mime="text/csv"
    )

# Clear Data Button
if st.button("🗑️ Clear All Data"):
    st.session_state.staff_data = pd.DataFrame(columns=st.session_state.staff_data.columns)
    st.warning("⚠️ All staff data has been cleared!")

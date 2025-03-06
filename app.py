import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from faker import Faker

fake = Faker()
roles = ["Professor", "Associate Professor", "Assistant Professor", "Researcher"]
tasks = ["Research", "Teaching", "Administration", "Community Service", "Mentoring", "Curriculum Development"]

st.set_page_config(page_title="Staff Productivity Analysis", page_icon="📊", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #f8f9fa; }
        .title { color: #343a40; font-size: 36px; font-weight: bold; text-align: center; margin-bottom: 20px; }
        .container { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); }
        .banner { background-color: #007BFF; color: white; font-size: 24px; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .final-message { background-color: #28A745; color: white; font-size: 20px; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Staff Productivity Analysis</div>", unsafe_allow_html=True)

if "staff_data" not in st.session_state:
    st.session_state.staff_data = pd.DataFrame(columns=[
        "Staff ID", "Name", "Role", "Research Papers", "Grants/Funding (Lakh)", "Extra Activities", "Training Hours Attended", "Productive Tasks", "Non-Productive Task", "Productive Score"
    ])

col1, col2 = st.columns([1, 2])

with col1:
    with st.form("staff_form"):
        st.markdown("### 📝 Enter Staff Details")
        staff_id = st.number_input("Staff ID", min_value=10000, max_value=99999, step=1, format="%d")
        name = st.text_input("Name", "")
        role = st.selectbox("Role", roles)
        research_papers = st.number_input("Research Papers", min_value=0, max_value=50, step=1)
        grants = st.number_input("Grants/Funding (Lakh)", min_value=1, max_value=50, step=1)
        extra_activities = st.text_area("Extra Activities", "")
        training_hours = st.number_input("Training Hours Attended", min_value=0, max_value=200, step=1)
        productive_tasks = st.multiselect("Productive Tasks", tasks)
        non_productive_task = st.text_area("Non-Productive Task", "")
        productive_score = research_papers * 2 + grants + training_hours * 0.5
        submit_button = st.form_submit_button("➕ Add Staff")

if submit_button:
    new_entry = pd.DataFrame({
        "Staff ID": [staff_id],
        "Name": [name],
        "Role": [role],
        "Research Papers": [research_papers],
        "Grants/Funding (Lakh)": [grants],
        "Extra Activities": [extra_activities],
        "Training Hours Attended": [training_hours],
        "Productive Tasks": [", ".join(productive_tasks)],
        "Non-Productive Task": [non_productive_task],
        "Productive Score": [productive_score]
    })
    st.session_state.staff_data = pd.concat([st.session_state.staff_data, new_entry], ignore_index=True)
    st.success("✅ Staff member added successfully!")
    st.markdown("<div class='final-message'>Thank you for submitting your details! Your contribution plays a crucial role in enhancing productivity and research excellence. Keep up the great work! 🚀</div>", unsafe_allow_html=True)
    st.rerun()

if not st.session_state.staff_data.empty:
    avg_productive_score = st.session_state.staff_data["Productive Score"].mean()
    st.markdown(f"<div class='banner'>Average Productive Score: {avg_productive_score:.2f}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Productivity Analysis")
    if not st.session_state.staff_data.empty:
        task_counts = st.session_state.staff_data["Productive Tasks"].str.split(", ").explode().value_counts()
        fig_bar = px.bar(task_counts, x=task_counts.index, y=task_counts.values, labels={'x': 'Task', 'y': 'Count'}, title="Productive Task Distribution", color=task_counts.index)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        prod_count = st.session_state.staff_data["Productive Tasks"].apply(lambda x: len(x.split(", ")) if isinstance(x, str) else 0).sum()
        non_prod_count = st.session_state.staff_data["Non-Productive Task"].apply(lambda x: 1 if x else 0).sum()
        fig_pie = px.pie(names=["Productive", "Non-Productive"], values=[prod_count, non_prod_count], title="Productivity Ratio")
        st.plotly_chart(fig_pie, use_container_width=True)
        
        fig_score = px.histogram(st.session_state.staff_data, x="Productive Score", title="Distribution of Productive Scores", nbins=10, color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig_score, use_container_width=True)

if not st.session_state.staff_data.empty:
    csv = st.session_state.staff_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="staff_productivity.csv",
        mime="text/csv"
    )

if st.button("🗑️ Clear All Data"):
    st.session_state.staff_data = pd.DataFrame(columns=st.session_state.staff_data.columns)
    st.warning("⚠️ All staff data has been cleared!")

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from code_validator import decode_code2

# Database setup
db_path = Path(__file__).parent / "engineering_dashboard.db"
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


# Define a function to fetch data
def fetch_data():
    with Session() as session:
        query = "SELECT * FROM engineering"
        df = pd.read_sql(query, session.bind)
    return df


# Load data
df = fetch_data()

# Streamlit app setup
st.set_page_config(layout="wide")
st.title("Engineering Dashboard")

# Calculate total person-hours for each project
filtered_df = df[df['project_name'] != "امور جاری"]
project_hours = filtered_df.groupby('project_name')['duration'].sum().reset_index()
project_hours.rename(columns={'duration': 'total_hours'}, inplace=True)

# Plot person-hours per project
fig = px.bar(project_hours, x='project_name', y='total_hours', title="Total Person-Hours per Project")
st.plotly_chart(fig)

# Visualizing Project Distribution
st.divider()
st.subheader("Project Code Distribution")
project_code_distribution = df.groupby(['project_code', 'project_name']).size().reset_index(name='count')

fig1 = px.pie(
    project_code_distribution,
    names='project_code',
    values='count',
    title="Project Code Distribution",
    hover_data={'project_name': True}
)
st.plotly_chart(fig1)

# ********************************* #

# Decode project codes and extract source and type
decoded_results = df['project_code'].apply(decode_code2)
df['decoded'], df['map_source_str'], df['map_tp_str'] = zip(*decoded_results)

# Filter data for map_source_str
source_counts = df['map_source_str'].value_counts().reset_index()
source_counts.columns = ['map_source_str', 'count']
source_counts_filtered = source_counts[source_counts['map_source_str'] != 'امور جاری']

col1, col2 = st.columns(2)
with col1:
    # Create a pie chart for map_source_str
    fig2 = px.pie(
        source_counts_filtered,
        names='map_source_str',
        values='count',
        title="Project Source Distribution",
        hover_data={'map_source_str': True}
    )
    fig2.update_traces(textinfo='percent+label',
                       hovertemplate='<b>Source:</b> %{label}<br><b>Count:</b> %{value}<extra></extra>')
    st.plotly_chart(fig2)

    # Filter data for map_tp_str
    type_counts = df['map_tp_str'].value_counts().reset_index()
    type_counts.columns = ['map_tp_str', 'count']

with col2:
    # Create a pie chart for map_tp_str
    fig3 = px.pie(
        type_counts,
        names='map_tp_str',
        values='count',
        title="Project Type Distribution",
        hover_data={'map_tp_str': True}
    )
    fig3.update_traces(textinfo='percent+label',
                       hovertemplate='<b>Type:</b> %{label}<br><b>Count:</b> %{value}<extra></extra>')
    st.plotly_chart(fig3)




# New Feature: Select project code and show person-hours
st.divider()
st.subheader("Filter By Project Code    ")
df = fetch_data()
unique_project_codes = df['project_code'].unique()
selected_project_code = st.selectbox("Select Project Code", options=unique_project_codes)

# فیلتر کردن داده‌ها بر اساس project_code انتخاب‌شده
project_filtered_df = df[df['project_code'] == selected_project_code]

st.subheader(f"Information for Project Code: {selected_project_code}")
st.dataframe(project_filtered_df, hide_index=True, use_container_width=True)

# ایجاد یک بار چارت بر اساس TASK_NAME و DURATION
fig = px.bar(project_filtered_df, x='task_name', y='duration', title="Task Duration", labels={'DURATION': 'Duration (hours)', 'TASK_NAME': 'Task Name'})

# نمایش بار چارت در Streamlit
st.plotly_chart(fig)



# ********************************* #
st.divider()
# Additional Filtering Options
st.subheader("Filter By Person")
selected_person = st.selectbox("Select Person", options=df['person_name'].unique())
filtered_data = df[df['person_name'] == selected_person]

st.subheader(f"Information for Person: {selected_person}")
st.dataframe(filtered_data)

# Visualization for filtered data
filtered_hours = filtered_data.groupby('project_name')['duration'].sum().reset_index()
filtered_hours.rename(columns={'duration': 'total_hours'}, inplace=True)

fig4 = px.bar(filtered_hours, x='project_name', y='total_hours', title=f"Total Person-Hours for {selected_person}")
st.plotly_chart(fig4)

# ********************************* #




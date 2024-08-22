import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from code_validator import decode_code2


def gradient_divider():
    # Gradient divider using HTML and CSS
    st.markdown(
        """
        <hr style="border: none; height: 3px; background: linear-gradient(to right, #EF5A6F, #F6FB7A);">
        """,
        unsafe_allow_html=True
    )

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
st.set_page_config(layout="wide", page_title="Engineering Visualization")
st.title("Engineering Dashboard")

# Calculate total person-hours for each project
filtered_df = df[df['project_name'] != "امور جاری"]
project_hours = filtered_df.groupby('project_name')['duration'].sum().reset_index()
project_hours.rename(columns={'duration': 'total_hours'}, inplace=True)

# Plot person-hours per project
fig = px.bar(project_hours, x='project_name', y='total_hours', title="Total Person-Hours per Project")
st.plotly_chart(fig)

# Visualizing Project Distribution
gradient_divider()
st.subheader("Project Code Distribution")

# df_filtered = df[df['project_code'] != "000000000"]
# project_code_distribution = df_filtered.groupby(['project_code', 'project_name']).size().reset_index(name='count')

fig1 = px.pie(
    project_hours,
    names='project_name',
    values='total_hours',
    title="Project Code Distribution",
    hover_data={'project_name': True}
)
st.plotly_chart(fig1)

# ********************************* #
# Decode project codes and extract source and type
decoded_results = df['project_code'].apply(decode_code2)
df['decoded'], df['map_source_str'], df['map_tp_str'] = zip(*decoded_results)

# گروه‌بندی داده‌ها بر اساس map_source_str و محاسبه مجموع duration
source_duration = df.groupby('map_source_str')['duration'].sum().reset_index()
source_duration.columns = ['map_source_str', 'total_duration']
source_duration_filtered = source_duration[source_duration['map_source_str'] != 'امور جاری']

col1, col2 = st.columns(2)
with col1:
    # ایجاد نمودار دایره‌ای برای map_source_str با استفاده از مجموع duration
    fig2 = px.pie(
        source_duration_filtered,
        names='map_source_str',
        values='total_duration',
        title="Project Source Duration Distribution",
        hover_data={'map_source_str': True}
    )
    fig2.update_traces(textinfo='percent+label',
                       hovertemplate='<b>Source:</b> %{label}<br><b>Total Duration:</b> %{value} hours<extra></extra>')
    st.plotly_chart(fig2)

    # گروه‌بندی داده‌ها بر اساس map_tp_str و محاسبه مجموع duration
    type_duration = df.groupby('map_tp_str')['duration'].sum().reset_index()
    type_duration.columns = ['map_tp_str', 'total_duration']

with col2:
    # ایجاد نمودار دایره‌ای برای map_tp_str با استفاده از مجموع duration
    fig3 = px.pie(
        type_duration,
        names='map_tp_str',
        values='total_duration',
        title="Project Type Duration Distribution",
        hover_data={'map_tp_str': True}
    )
    fig3.update_traces(textinfo='percent+label',
                       hovertemplate='<b>Type:</b> %{label}<br><b>Total Duration:</b> %{value} hours<extra></extra>')
    st.plotly_chart(fig3)


# ********************************* #
# New Feature: Select project code and show person-hours
gradient_divider()
df = fetch_data()
df = df[df['project_name'] != "امور جاری"]
# Extract unique project codes and corresponding product names
unique_project_codes = df['project_code'].unique()
unique_product_names = list(set(decode_code2(code, True) for code in unique_project_codes))

# Sort the unique product names for better UX
unique_product_names.sort()

# Create a selectbox for product names
st.subheader("Filter By Product Name")
selected_product_name = st.selectbox("Select Product Name", options=unique_product_names)



# Filter data based on the selected product name
filtered_project_codes = [code for code in unique_project_codes if decode_code2(code, True) == selected_product_name]
project_filtered_df = df[df['project_code'].isin(filtered_project_codes)]
project_filtered_df = project_filtered_df.drop(columns=['id'])
# Calculate cumulative duration per project
project_duration = project_filtered_df.groupby('project_code')['duration'].sum().reset_index()

# Display the total sum of durations
total_duration = project_duration['duration'].sum()
st.subheader(f"Total Duration for {selected_product_name} : {total_duration} hours")
# Display the filtered data
st.dataframe(project_filtered_df, hide_index=True, use_container_width=True)



# Create a bar chart to visualize cumulative duration per project
fig = px.bar(project_duration,
             x='project_code',
             y='duration',
             title="Cumulative Duration per Product",
             labels={'duration': 'Cumulative Duration (hours)', 'project_code': 'Project Code'})

# Display the chart in Streamlit
st.plotly_chart(fig)
# ********************************* #
gradient_divider()
st.subheader("Filter By Project Name")
df = fetch_data()
unique_project_codes = df['project_name'].unique()
selected_project_code = st.selectbox("Select Project Code", options=unique_project_codes)

# فیلتر کردن داده‌ها بر اساس project_code انتخاب‌شده
project_filtered_df = df[df['project_name'] == selected_project_code]
project_filtered_df = project_filtered_df.drop(columns=['id'])
# st.subheader(f"Information for Project Code: {selected_project_code}")
st.dataframe(project_filtered_df, hide_index=True, use_container_width=True)

# ایجاد یک بار چارت بر اساس TASK_NAME و DURATION
task_duration = project_filtered_df.groupby('task_name')['duration'].sum().reset_index()

fig4 = px.bar(task_duration,
              x='task_name',
              y='duration',
              title="Task Duration",
              labels={'duration': 'Duration (hours)', 'task_name': 'Task Name'})

st.plotly_chart(fig4)

# ********************************* #

gradient_divider()
df2 = fetch_data()
# Additional Filtering Options
st.subheader("Filter By Person")
selected_person = st.selectbox("Select Person", options=df['person_name'].unique())
filtered_data = df2[df2['person_name'] == selected_person]
filtered_data = filtered_data.drop(columns=['id'])
st.subheader(f"Information for Person: {selected_person}")
st.dataframe(filtered_data, hide_index=True, use_container_width=True)

# Visualization for filtered data
filtered_hours = filtered_data.groupby('project_name')['duration'].sum().reset_index()

fig5 = px.bar(filtered_hours,
              x='project_name',
              y='duration',
              title=f"Total Person-Hours for {selected_person}",
              labels={'duration': 'Duration (hours)', 'task_name': 'Project Name'})
st.plotly_chart(fig5)

# ********************************* #















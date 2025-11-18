import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide",
)
# ------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\lisag\Desktop\hr_cleaned.csv", parse_dates=[
        "DateofHire", "DateofTermination", "DOB", "LastPerformanceReview_Date"
    ])
    return df

df = load_data()

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------

st.title("📊 HR Analytics Dashboard")
st.markdown("A live data dashboard powered by **Streamlit + Python**.")

# ------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------
st.sidebar.header("Filters")

departments = ["All"] + sorted(df["Department"].dropna().unique().tolist())
positions = ["All"] + sorted(df["Position"].dropna().unique().tolist())
managers = ["All"] + sorted(df["ManagerName"].dropna().unique().tolist())
states = ["All"] + sorted(df["State"].dropna().unique().tolist())

selected_dept = st.sidebar.selectbox("Department", departments)
selected_pos = st.sidebar.selectbox("Position", positions)
selected_mgr = st.sidebar.selectbox("Manager", managers)
selected_state = st.sidebar.selectbox("State", states)

# Apply filters
filtered = df.copy()

if selected_dept != "All":
    filtered = filtered[filtered["Department"] == selected_dept]

if selected_pos != "All":
    filtered = filtered[filtered["Position"] == selected_pos]

if selected_mgr != "All":
    filtered = filtered[filtered["ManagerName"] == selected_mgr]

if selected_state != "All":
    filtered = filtered[filtered["State"] == selected_state]

# ------------------------------------------------------
# KPI METRICS
# ------------------------------------------------------
st.subheader("📌 Key HR Metrics")

col1, col2, col3, col4 = st.columns(4)

turnover_rate = filtered["Termd"].mean() * 100
avg_salary = filtered["Salary"].mean()
avg_perf = filtered["PerformanceScore_Num"].mean()
avg_satisfaction = filtered["EmpSatisfaction"].mean()

col1.metric("Turnover Rate", f"{turnover_rate:.1f}%")
col2.metric("Avg Salary", f"${avg_salary:,.0f}")
col3.metric("Avg Performance Score", f"{avg_perf:.2f}")
col4.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}")

# ------------------------------------------------------
# MAIN VISUALS
# ------------------------------------------------------

st.markdown("### 👥 Employee Demographics")

colA, colB = st.columns(2)

with colA:
    fig_race = px.pie(filtered, names="RaceDesc", title="Race Distribution")
    st.plotly_chart(fig_race, use_container_width=True)

with colB:
    fig_gender = px.histogram(filtered, x="Sex", title="Gender Distribution")
    st.plotly_chart(fig_gender, use_container_width=True)

# ------------------------------------------------------

st.markdown("### 💼 Department & Position Insights")

colC, colD = st.columns(2)

with colC:
    fig_dept = px.histogram(filtered, x="Department", color="Termd",
                            title="Terminations by Department")
    st.plotly_chart(fig_dept, use_container_width=True)

with colD:
    fig_pos = px.histogram(filtered, x="Position", title="Employee Count by Position")
    st.plotly_chart(fig_pos, use_container_width=True)

# ------------------------------------------------------

st.markdown("### 💵 Compensation & Tenure")

colE, colF = st.columns(2)

with colE:
    fig_salary = px.box(filtered, y="Salary", title="Salary Distribution")
    st.plotly_chart(fig_salary, use_container_width=True)

with colF:
    fig_tenure = px.scatter(
        filtered, x="Tenure_Years", y="PerformanceScore",
        color="Department", hover_name="Employee_Name",
        title="Tenure vs Performance Score"
    )
    st.plotly_chart(fig_tenure, use_container_width=True)

# ------------------------------------------------------

st.markdown("### 📈 Engagement & Performance")

colG, colH = st.columns(2)

with colG:
    fig_engage = px.scatter(
        filtered, x="EngagementSurvey", y="EmpSatisfaction",
        color="Department", hover_name="Employee_Name",
        title="Engagement vs Satisfaction"
    )
    st.plotly_chart(fig_engage, use_container_width=True)

with colH:
    fig_absences = px.histogram(
        filtered, x="Absences", color="Department",
        title="Absences Distribution"
    )
    st.plotly_chart(fig_absences, use_container_width=True)

# ------------------------------------------------------

st.markdown("### 📆 Termination Trends")

fig_term = px.histogram(
    filtered, x="DateofTermination",
    title="Termination Timeline",
)
st.plotly_chart(fig_term, use_container_width=True)

# ------------------------------------------------------

st.markdown("### 📑 Raw Data Table (Filtered)")
st.dataframe(filtered)
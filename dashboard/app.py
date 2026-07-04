import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px

from src.quality_checks import run_quality_checks
from src.alerts import check_alerts
from src.profiling import profile_columns, get_outlier_rows
from src.history import save_run, load_history
from src.report_generator import generate_pdf_report

# -------------------------------
# Page Configuration (MUST be first Streamlit command)
# -------------------------------
st.set_page_config(
    page_title="Data Quality Monitoring System",
    page_icon="📊",
    layout="wide"
)


# CSS file loading function
def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "reports", "history.csv")

st.title("📊 Data Quality Monitoring System")
st.write("Upload any CSV file to analyze its data quality.")

# -------------------------------
# Upload CSV
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:

    # Load CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Run Quality Checks
    results = run_quality_checks(df)

    missing_values = results["missing_values"]
    duplicates = results["duplicates"]

    invalid_age = results.get("invalid_age", pd.DataFrame())
    invalid_email = results.get("invalid_email", pd.DataFrame())
    invalid_phone = results.get("invalid_phone", pd.DataFrame())
    invalid_join_date = results.get("invalid_join_date", pd.DataFrame())

    # -------------------------------
    # Data Quality Score
    # -------------------------------
    total_issues = (
        missing_values
        + duplicates
        + len(invalid_age)
        + len(invalid_email)
        + len(invalid_phone)
        + len(invalid_join_date)
    )

    score = max(0, 100 - total_issues * 5)

    st.subheader("📋 Dashboard Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Quality Score", f"{score}%")
    col2.metric("Records", len(df))
    col3.metric("Columns", len(df.columns))
    col4.metric("Issues", total_issues)

    # Save this run to history (for trend tracking below)
    save_run(
        HISTORY_PATH,
        file_name=uploaded_file.name,
        records=len(df),
        columns=len(df.columns),
        issues=total_issues,
        score=score,
    )

    # -------------------------------
    # NEW: Column-level Profiling
    # -------------------------------
    st.subheader("🔎 Column Profiling")
    st.caption("Per-column stats: type, missing %, uniqueness, and outliers (numeric columns use the IQR method).")

    profile_df = profile_columns(df)
    st.dataframe(profile_df, use_container_width=True)

    # -------------------------------
    # Alerts
    # -------------------------------
    st.subheader("🚨 Alerts")

    alerts = check_alerts(df)

    if alerts:
        st.warning("Data quality issues were found.")
        st.json(alerts)
    else:
        st.success("No data quality issues found.")

    # -------------------------------
    # NEW: Row-level Drill-down
    # -------------------------------
    st.subheader("🔬 Drill-down: Inspect Issue Rows")

    drilldown_options = {
        "Rows with missing values": df[df.isnull().any(axis=1)],
        "Duplicate rows": df[df.duplicated(keep=False)],
        "Invalid Age": invalid_age,
        "Invalid Email": invalid_email,
        "Invalid Phone": invalid_phone,
        "Invalid Join Date": invalid_join_date,
    }

    # Add one drill-down option per numeric column's outliers
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        drilldown_options[f"Outliers in '{col}'"] = get_outlier_rows(df, col)

    selected_issue = st.selectbox("Choose an issue type to inspect:", list(drilldown_options.keys()))
    selected_rows = drilldown_options[selected_issue]

    if selected_rows is not None and not selected_rows.empty:
        st.write(f"**{len(selected_rows)} row(s)** found for: {selected_issue}")
        st.dataframe(selected_rows, use_container_width=True)
    else:
        st.info(f"No rows found for: {selected_issue}")

    # -------------------------------
    # Chart
    # -------------------------------
    st.subheader("📈 Quality Issues")

    chart_df = pd.DataFrame({
        "Issue": [
            "Missing Values",
            "Duplicates",
            "Invalid Age",
            "Invalid Email",
            "Invalid Phone",
            "Invalid Join Date"
        ],
        "Count": [
            missing_values,
            duplicates,
            len(invalid_age),
            len(invalid_email),
            len(invalid_phone),
            len(invalid_join_date)
        ]
    })

    fig = px.bar(
        chart_df,
        x="Issue",
        y="Count",
        color="Issue",
        title="Data Quality Issues"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # NEW: Trend / History over time
    # -------------------------------
    st.subheader("📉 Quality Score Trend")

    history_df = load_history(HISTORY_PATH)

    if len(history_df) > 1:
        trend_fig = px.line(
            history_df,
            x="timestamp",
            y="score",
            markers=True,
            title="Quality Score Over Time"
        )
        st.plotly_chart(trend_fig, use_container_width=True)
        with st.expander("View raw history"):
            st.dataframe(history_df, use_container_width=True)
    else:
        st.info("Upload more files over time to build up a trend history.")

    # -------------------------------
    # Export
    # -------------------------------
    st.subheader("📥 Export")

    exp_col1, exp_col2 = st.columns(2)

    csv = df.to_csv(index=False).encode("utf-8")
    exp_col1.download_button(
        label="Download CSV",
        data=csv,
        file_name="data_quality_report.csv",
        mime="text/csv"
    )

    # NEW: PDF summary report
    issue_counts = {
        "Missing Values": int(missing_values),
        "Duplicates": int(duplicates),
        "Invalid Age": len(invalid_age),
        "Invalid Email": len(invalid_email),
        "Invalid Phone": len(invalid_phone),
        "Invalid Join Date": len(invalid_join_date),
    }
    pdf_bytes = generate_pdf_report(
        file_name=uploaded_file.name,
        records=len(df),
        columns=len(df.columns),
        score=score,
        issue_counts=issue_counts,
    )
    exp_col2.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name="data_quality_report.pdf",
        mime="application/pdf"
    )

else:
    st.info("Please upload a CSV file.")
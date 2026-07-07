import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px

from src.load_data import load_data
from src.quality_checks import run_quality_checks
from src.alerts import check_alerts
from src.profiling import profile_columns, get_outlier_rows
from src.history import save_run, load_history
from src.report_generator import generate_pdf_report


st.set_page_config(
    page_title="Data Quality Monitoring System",
    page_icon="📊",
    layout="wide"
)


def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "reports", "history.csv")


st.markdown("""
<div class="hero-section">
    <div class="hero-badge">AUDIT</div>
    <div class="hero-title-row">
        <div class="hero-icon">📊</div>
        <div>
            <h1>Data Quality Monitoring System</h1>
            <p>Upload any CSV file to analyze missing values, duplicates, invalid records, outliers, and overall data health.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="upload-heading">📂 Upload your dataset</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"],
    label_visibility="collapsed"
)


with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.markdown("---")
    st.caption("Data Quality Checks")
    st.write("✅ Missing values")
    st.write("✅ Duplicate rows")
    st.write("✅ Invalid emails")
    st.write("✅ Invalid phones")
    st.write("✅ Invalid ages")
    st.write("✅ Invalid dates")
    st.write("✅ Outlier detection")


if uploaded_file is None:
    st.markdown("""
    <div class="welcome-box">
        <h2>Welcome 👋</h2>
        <p>
            Start by uploading a CSV file above.
            The system will automatically scan the dataset and generate a full data health dashboard.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon feature-icon-green">📂</div>
            <h3>Upload CSV</h3>
            <p>Upload any dataset in CSV format.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon feature-icon-blue">🔍</div>
            <h3>Quality Checks</h3>
            <p>Detect missing values, duplicates, invalid records and outliers.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon feature-icon-amber">📊</div>
            <h3>Dashboard</h3>
            <p>View score, charts, alerts, profiling and downloadable reports.</p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


df = load_data(uploaded_file)

results = run_quality_checks(df)

missing_values = int(results.get("missing_values", 0))
duplicates = int(results.get("duplicates", 0))

invalid_age = results.get("invalid_age", pd.DataFrame())
invalid_email = results.get("invalid_email", pd.DataFrame())
invalid_phone = results.get("invalid_phone", pd.DataFrame())
invalid_join_date = results.get("invalid_join_date", pd.DataFrame())

total_issues = (
    missing_values
    + duplicates
    + len(invalid_age)
    + len(invalid_email)
    + len(invalid_phone)
    + len(invalid_join_date)
)

score = max(0, round(100 - ((total_issues / max(len(df), 1)) * 10), 2))

save_run(
    HISTORY_PATH,
    file_name=uploaded_file.name,
    records=len(df),
    columns=len(df.columns),
    issues=total_issues,
    score=score,
)


st.markdown("## 📋 Dashboard Summary")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Quality Score", f"{score}%")
m2.metric("Records", len(df))
m3.metric("Columns", len(df.columns))
m4.metric("Issues", total_issues)

st.progress(score / 100)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Dataset",
    "🔎 Profiling",
    "🚨 Alerts",
    "📈 Charts",
    "📥 Export"
])


with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("🔬 Drill-down: Inspect Issue Rows")

    drilldown_options = {
        "Rows with missing values": df[df.isnull().any(axis=1)],
        "Duplicate rows": df[df.duplicated(keep=False)],
        "Invalid Age": invalid_age,
        "Invalid Email": invalid_email,
        "Invalid Phone": invalid_phone,
        "Invalid Join Date": invalid_join_date,
    }

    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        drilldown_options[f"Outliers in '{col}'"] = get_outlier_rows(df, col)

    selected_issue = st.selectbox(
        "Choose an issue type to inspect:",
        list(drilldown_options.keys())
    )

    selected_rows = drilldown_options[selected_issue]

    if selected_rows is not None and not selected_rows.empty:
        st.write(f"**{len(selected_rows)} row(s)** found for: {selected_issue}")
        st.dataframe(selected_rows, use_container_width=True)
    else:
        st.info(f"No rows found for: {selected_issue}")


with tab2:
    st.subheader("Column Profiling")
    st.caption("Per-column stats: type, missing percentage, uniqueness, and outliers.")

    profile_df = profile_columns(df)
    st.dataframe(profile_df, use_container_width=True)


with tab3:
    st.subheader("Alerts")

    alerts = check_alerts(df)

    if alerts:
        st.warning("Data quality issues were found.")
        with st.expander("View Alert Details"):
            st.json(alerts)
    else:
        st.success("No data quality issues found.")


with tab4:
    st.subheader("📈 Charts")

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

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Quality Issues Bar Chart")

        bar_fig = px.bar(
            chart_df,
            x="Issue",
            y="Count",
            color="Issue",
            title="Data Quality Issues",
            color_discrete_sequence=[
                "#e8b339",
                "#2dd98f",
                "#ef5b5b",
                "#5a9bd4",
                "#c084fc",
                "#f4f2ea"
            ]
        )

        bar_fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="IBM Plex Mono, monospace",
                color="#e8e6df",
                size=12
            ),
            title_font=dict(
                family="Space Grotesk, sans-serif",
                size=16,
                color="#f4f2ea"
            ),
            showlegend=False,
            margin=dict(t=50, l=10, r=10, b=10),
        )

        bar_fig.update_xaxes(showgrid=False, linecolor="#232a38")
        bar_fig.update_yaxes(
            showgrid=True,
            gridcolor="#232a38",
            zerolinecolor="#232a38"
        )
        bar_fig.update_traces(marker_line_width=0)

        st.plotly_chart(bar_fig, use_container_width=True)

    with col2:
        st.markdown("### 🥧 Issue Distribution Pie Chart")

        pie_fig = px.pie(
            chart_df,
            names="Issue",
            values="Count",
            hole=0.45,
            color="Issue",
            color_discrete_sequence=[
                "#e8b339",
                "#2dd98f",
                "#ef5b5b",
                "#5a9bd4",
                "#c084fc",
                "#f4f2ea"
            ]
        )

        pie_fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        pie_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="IBM Plex Mono, monospace",
                size=12,
                color="#e8e6df"
            ),
            showlegend=True,
            legend_title="Issue Type",
            margin=dict(t=50, l=10, r=10, b=10),
        )

        st.plotly_chart(pie_fig, use_container_width=True)

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

        trend_fig.update_traces(
            line=dict(color="#2dd98f", width=3),
            marker=dict(color="#e8b339", size=9),
            fill="tozeroy",
            fillcolor="rgba(45, 217, 143, 0.08)"
        )

        trend_fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="IBM Plex Mono, monospace",
                color="#e8e6df",
                size=12
            ),
            title_font=dict(
                family="Space Grotesk, sans-serif",
                size=16,
                color="#f4f2ea"
            ),
            yaxis_title="Quality Score (%)",
            xaxis_title="",
            margin=dict(t=50, l=10, r=10, b=10),
        )

        trend_fig.update_xaxes(showgrid=False, linecolor="#232a38")
        trend_fig.update_yaxes(
            showgrid=True,
            gridcolor="#232a38",
            range=[0, 105]
        )

        st.plotly_chart(trend_fig, use_container_width=True)

        with st.expander("View Raw History"):
            st.dataframe(history_df, use_container_width=True)

    else:
        st.info("Upload more files over time to build trend history.")

with tab5:
    st.subheader("Export Reports")

    exp_col1, exp_col2 = st.columns(2)

    csv = df.to_csv(index=False).encode("utf-8")

    exp_col1.download_button(
        label="Download CSV",
        data=csv,
        file_name="data_quality_report.csv",
        mime="text/csv"
    )

    issue_counts = {
        "Missing Values": missing_values,
        "Duplicates": duplicates,
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
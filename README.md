# 📊 Data Quality Monitoring System

A Python-based Data Quality Monitoring System built using **Streamlit**, **Pandas**, **Plotly**, and **FPDF** to ensure data integrity and reliability.

This project automatically analyzes uploaded CSV datasets, identifies common data quality issues, generates reports, and provides an interactive dashboard for monitoring data health.

---

# 🚀 Features

- Upload any CSV dataset
- Detect missing values
- Detect duplicate records
- Validate email addresses
- Validate phone numbers
- Detect invalid ages
- Validate join dates
- Outlier detection
- Column profiling
- Interactive dashboard
- Alerts for data quality issues
- Data Quality Score calculation
- Data Quality Trend analysis
- Download CSV report
- Download PDF report

---

# 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- FPDF
- NumPy

---

# 📁 Project Structure

```
DataQualityMonitoringSystem/
│
├── dashboard/
│   ├── app.py
│   └── style.css
│
├── data/
│   ├── raw/
│   └── reports/
│
├── docs/
│   └── governance.md
│
├── src/
│   ├── alerts.py
│   ├── config.py
│   ├── history.py
│   ├── load_data.py
│   ├── metrics.py
│   ├── profiling.py
│   ├── quality_checks.py
│   ├── report_generator.py
│   └── utils.py
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/havindu99/data-quality-monitoring-system.git
```

Go to project folder

```bash
cd data-quality-monitoring-system
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📊 Dashboard Modules

## Dashboard Summary

- Data Quality Score
- Total Records
- Total Columns
- Total Issues

---

## Dataset

- Dataset Preview
- Drill-down Analysis
- Invalid Records

---

## Column Profiling

- Data Type
- Missing Percentage
- Unique Values
- Outlier Detection

---

## Alerts

- Missing Values
- Duplicate Rows
- Invalid Email
- Invalid Phone
- Invalid Age
- Invalid Join Date

---

## Charts

- Bar Chart
- Pie Chart
- Quality Score Trend

---

## Export

- CSV Report
- PDF Report

---

# 📄 Data Quality Checks

The system automatically validates:

- Missing Values
- Duplicate Rows
- Invalid Emails
- Invalid Phone Numbers
- Invalid Age Values
- Invalid Join Dates
- Outlier Records

---

# 📈 Data Quality Score

The quality score is calculated based on the total number of detected issues.

Higher score indicates better data quality.

```
100% = Excellent
90–99% = Good
70–89% = Fair
Below 70% = Poor
```

---

# 📑 Generated Reports

The system generates:

- Data Health Dashboard
- Interactive Charts
- PDF Summary Report
- CSV Export

---

# 🔒 Data Governance Recommendations

- Validate data before storing.
- Remove duplicate records.
- Enforce mandatory fields.
- Validate email and phone formats.
- Monitor data quality regularly.
- Maintain audit logs.
- Apply role-based access control.

---

# 🎯 Project Objectives

- Improve data integrity
- Improve data reliability
- Automate data quality monitoring
- Generate health reports
- Provide real-time quality insights

---

# 👨‍💻 Developed By

**Havindu**
-Data Science Intern

---

# 📜 License

This project is developed for educational and research purposes.

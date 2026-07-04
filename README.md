# 📊 Data Quality Monitoring System

A Streamlit dashboard for uploading any CSV file and instantly checking its data quality — missing values, duplicates, invalid fields, statistical outliers, and trends over time.

---

## Features

- **Dataset Preview** — view the uploaded CSV as a table
- **Quality Score** — an overall 0–100% score based on detected issues
- **Column Profiling** — per-column type, missing %, unique values, and (for numeric columns) min/max/mean/std dev/outlier count using the IQR method
- **Alerts** — automatic detection of:
  - Missing values
  - Duplicate rows
  - Invalid age (negative values)
  - Invalid email (malformed format)
  - Invalid phone (not 10 digits)
  - Invalid join date (unparsable date)
- **Row-level Drill-down** — pick an issue type and inspect the exact rows behind it
- **Quality Score Trend** — tracks every upload's score over time and charts it
- **Export**
  - Download the dataset as CSV
  - Download a one-page PDF summary report

---

## Project Structure

```
DataQualityMonitoringSystem/
├── dashboard/
│   ├── app.py              # Main Streamlit app
│   └── style.css            # Custom dashboard theme
├── data/
│   ├── raw/                 # (optional) raw input files
│   └── reports/
│       └── history.csv      # Auto-generated run history (created on first upload)
├── docs/
│   └── governance.md
├── src/
│   ├── __init__.py
│   ├── alerts.py             # Alert detection logic
│   ├── config.py
│   ├── history.py            # Run history save/load for trend tracking
│   ├── load_data.py
│   ├── metrics.py
│   ├── profiling.py          # Column-level statistics & outlier detection
│   ├── quality_checks.py     # Core quality check logic
│   ├── report_generator.py   # PDF report generation
│   └── utils.py
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

---

## Setup

1. **Clone / open the project folder**

2. **Create and activate a virtual environment** (if not already set up)
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   python -m pip install -r requirements.txt
   ```
   Make sure `streamlit`, `pandas`, `plotly`, and `fpdf2` are included.

4. **Run the dashboard**
   ```powershell
   streamlit run dashboard/app.py
   ```

5. Open the local URL shown in the terminal (usually `http://localhost:8501`).

---

## Usage

1. Upload any `.csv` file using the file uploader.
2. Review the dataset preview, quality score, and column profiling table.
3. Check the **Alerts** section for a JSON summary of detected issues.
4. Use the **Drill-down** dropdown to inspect the exact rows behind any issue (including statistical outliers per numeric column).
5. Upload more files over time to build up the **Quality Score Trend** chart.
6. Export results as CSV or a PDF report from the **Export** section.

---

## Notes

- The `history.csv` file (under `data/reports/`) is created automatically on first upload and grows with every subsequent run — this powers the trend chart.
- Column profiling and outlier detection use the **IQR (Interquartile Range) method**, which flags values falling far outside the typical range for that column.
- The dashboard theme (`style.css`) uses **Space Grotesk** and **IBM Plex Mono**, loaded via Google Fonts with safe local fallbacks.

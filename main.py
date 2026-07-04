from src import load_data
from src import quality_checks
from src import report_generator
from src import alerts


def run_pipeline(file_path):
    # Load the data
    df = load_data.load_data(file_path)

    # Run quality checks
    results = quality_checks.run_quality_checks(df)

    # Generate report
    report_generator.generate_report(df, **results)

    # Send alerts if there are any issues
    alerts.send_alerts(results)
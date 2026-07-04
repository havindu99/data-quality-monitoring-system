from fpdf import FPDF
from datetime import datetime


class _ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Data Quality Monitoring Report", ln=True, align="C")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 6, datetime.now().strftime("Generated on %Y-%m-%d %H:%M:%S"),
                   ln=True, align="C")
        self.ln(4)

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(20, 20, 20)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(200, 200, 200)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(3)


def generate_pdf_report(file_name: str, records: int, columns: int,
                         score: float, issue_counts: dict) -> bytes:
    """
    Builds a one-page summary PDF: file info, quality score, and a
    breakdown table of issue counts. Returns raw PDF bytes for
    st.download_button.
    """
    pdf = _ReportPDF()
    pdf.add_page()

    # --- Summary ---
    pdf.section_title("Summary")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"File: {file_name}", ln=True)
    pdf.cell(0, 7, f"Records: {records}", ln=True)
    pdf.cell(0, 7, f"Columns: {columns}", ln=True)
    pdf.cell(0, 7, f"Quality Score: {score}%", ln=True)
    pdf.ln(4)

    # --- Issue breakdown table ---
    pdf.section_title("Issue Breakdown")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(120, 8, "Issue Type", border=1)
    pdf.cell(60, 8, "Count", border=1, ln=True, align="C")

    pdf.set_font("Helvetica", "", 10)
    for issue, count in issue_counts.items():
        pdf.cell(120, 8, issue, border=1)
        pdf.cell(60, 8, str(count), border=1, ln=True, align="C")

    # fpdf2 returns a bytearray; st.download_button needs bytes
    return bytes(pdf.output())
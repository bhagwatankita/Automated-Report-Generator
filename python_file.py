pip install fpdf pandas
import pandas as pd
from fpdf import FPDF

# Read data from a CSV file
def read_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("File not found.")
        return None

# Analyze data
def analyze_data(data):
    summary = {
        "Total Entries": len(data),
        "Columns": data.columns.tolist(),
        "Mean of Numeric Columns": data.select_dtypes(include='number').mean().to_dict(),
        "Missing Values": data.isnull().sum().to_dict()
    }
    return summary

# Generate PDF Report
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Data Analysis Report', border=0, ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=1)
        self.set_font('Arial', '', 11)
        if isinstance(content, dict):
            for key, value in content.items():
                self.cell(0, 10, f'{key}: {value}', ln=1)
        elif isinstance(content, list):
            for item in content:
                self.cell(0, 10, f'- {item}', ln=1)
        else:
            self.cell(0, 10, content, ln=1)
        self.ln(5)

def generate_pdf_report(summary, output_file):
    pdf = PDFReport()
    pdf.add_page()

    # Add summary sections
    pdf.add_section('Summary', summary)
    pdf.add_section('Mean of Numeric Columns', summary['Mean of Numeric Columns'])
    pdf.add_section('Missing Values', summary['Missing Values'])

    pdf.output(output_file)
    print(f'Report generated: {output_file}')

# Main Function
def main():
    file_path = input("Enter the path to the CSV file: ")
    data = read_data(file_path)

    if data is not None:
        summary = analyze_data(data)
        output_file = "C:/Users/ANKITA BHAGWAT/Documents/Data_Analysis_Report.pdf"
        generate_pdf_report(summary, output_file)

if __name__ == "__main__":
    main()

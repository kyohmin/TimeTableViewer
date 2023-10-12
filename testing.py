import os
from pyexcel_ods import save_data

def save_excel_as_pdf(excel_file_path, pdf_output_path):
    # Ensure the output path has a .pdf extension
    if not pdf_output_path.endswith('.pdf'):
        pdf_output_path += '.pdf'

    # Load your Excel file and save it as a PDF
    data = {os.path.basename(excel_file_path): excel_file_path}
    save_data(pdf_output_path, data)

if __name__ == "__main__":
    excel_file_path = "/Users/khms/CODE/TimeTableViewer/Hello4.xlsx"  # Replace with your Excel file path
    pdf_output_path = "output.pdf"  # Replace with the desired output PDF file path

    save_excel_as_pdf(excel_file_path, pdf_output_path)
from .cenums import ExportFormat
from .get_data import get_data
from .pdf_exporter import export_to_pdf
from .xlsx_exporter import export_to_xlsx

def get_report(url, auth, report_format = ExportFormat.Excel):
    data = get_data(url, auth)
    generate_report(data = data, report_format = report_format)

def generate_report(data, report_format = ExportFormat.Excel):
    print(f'Exporting to : {report_format}', end='\n\n')

    if report_format == ExportFormat.PDF:
        export_to_pdf(data = data)

    elif report_format == ExportFormat.Excel:
        export_to_xlsx(data = data)

    else:
        print('Exporter not supported !!!')
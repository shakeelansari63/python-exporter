from .cenums import ExportFormat, TemplateName
from .get_data import get_data
from .pdf_exporter import export_to_pdf
from .xlsx_exporter import export_to_xlsx
from .template import parse_template

def get_report(url, auth, report_format = ExportFormat.Excel, template = TemplateName.Invoice):
    data = get_data(url, auth)
    generate_report(data = data, report_format = report_format, template = template)

def generate_report(data, report_format = ExportFormat.Excel, template = TemplateName.Invoice):
    data_template = parse_template(template, report_format)
    
    if report_format == ExportFormat.PDF:
        export_to_pdf(data = data, template = data_template, template_name = template.name)

    elif report_format == ExportFormat.Excel:
        export_to_xlsx(data = data, template = data_template, template_name = template.name)

    else:
        print('Exporter not supported !!!')
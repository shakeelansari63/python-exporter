from pyexport import get_report
from pyexport import create_basic_auth
from pyexport import ExportFormat, TemplateName
from pyexport import parse_template

auth = create_basic_auth('CXSvg9Rjz8CVvy7oi5963768qQwWHJ3l','')
url = 'https://api.sandbox.invoiced.com/invoices/10030138'

get_report(url, auth, ExportFormat.Excel, template = TemplateName.Invoice)

#parse_template(TemplateName.Invoice, ExportFormat.Excel)
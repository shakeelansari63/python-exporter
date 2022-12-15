from enum import Enum

class ExportFormat(Enum):
    Excel = 'xlsx'
    PDF = 'pdf'

class TemplateName(Enum):
    Invoice = 'invoice'
    Order = 'order'
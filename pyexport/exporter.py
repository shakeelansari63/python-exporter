import xlsxwriter
import PyPDF2
from .get_data import get_data
import json

def get_report():
    data = get_data()
    print(data)

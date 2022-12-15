#from .yaml_formatter import yaml
import yaml
import os
import re
from .cenums import TemplateName, ExportFormat

def _type_parser(obj):
    if type(obj) == type([]):
        return [ _type_parser(x) for x in obj ]

    elif type(obj) == type(dict()):
        output = dict()
        for item in obj.items():
            output[item[0]] = _type_parser(item[1])
        return output

    elif type(obj) == type(''):
        var_regx = re.compile(r"\$\{\{\s*[a-z0-9\_]{1,}\s*\}\}", re.I)
        var_found = var_regx.findall(obj)

        for yaml_var in var_found:
            std_var = yaml_var.replace(' ', '')
            obj = obj.replace(yaml_var, std_var)
        return obj
    
    else:
        return obj

def parse_template(template_name: TemplateName, output_type: ExportFormat):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    template_file_name = f'{template_name.value}-{output_type.value}.yaml'
    template_file = os.path.join(os.path.join(cur_path, 'templates'), template_file_name)

    with open(template_file, 'r') as tfl:
        template = yaml.load(tfl, Loader = yaml.Loader)
        template = _type_parser(template)
        return template

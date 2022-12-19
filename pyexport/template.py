#from .yaml_formatter import yaml
import yaml
import os
import re
from .cenums import TemplateName, ExportFormat

max_row = 0

def _type_parser(obj):
    if type(obj) == type([]):
        return [ _type_parser(x) for x in obj ]

    elif type(obj) == type(dict()):
        output = dict()
        for item in obj.items():
            output[item[0]] = _type_parser(item[1])
        return output

    elif type(obj) == type(''):
        var_regx = re.compile(r"\$\{\{\s*[a-z0-9\_\.]{1,}\s*\}\}", re.I)
        var_found = var_regx.findall(obj)

        for yaml_var in var_found:
            strd_var = yaml_var.replace(' ', '')
            obj = obj.replace(yaml_var, strd_var)
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

def replace_var(field, data):
    global max_row
    variable_regex = re.compile(r"\$\{\{([a-z0-9\_\.]{1,})\}\}", re.I)

    if type(field) == type(''):
        template_variables = variable_regex.findall(field)

        for template_variable in template_variables:
            variable_value = ''

            if template_variable == 'max_row':
                variable_value = str(max_row)

            elif template_variable in data.keys():
                variable_value = data[template_variable]

            elif '.' in template_variable:
                subfields = template_variable.split('.')
                subdata = data
                notfound = 0
                for subfield in subfields:
                    if subfield in subdata.keys():
                        subdata = subdata[subfield]
                    else:
                        notfound = 1
                        break

                if notfound == 0:
                    variable_value = subdata

            if type(variable_value) != type('') and field.strip() == f'${{{{{template_variable}}}}}':
                field = variable_value

            else:
                field = field.replace(f'${{{{{template_variable}}}}}', variable_value)
                
        return field

    elif type(field) == type(dict()):
        for fl in field.keys():
            field[fl] = replace_var(field[fl], data)
        
        return field

    elif type(field) == type([]):
        return [replace_var(fl, data) for fl in field]
    
    else:
        return field

def update_max_row(row):
    global max_row
    if max_row < row:
        max_row = row

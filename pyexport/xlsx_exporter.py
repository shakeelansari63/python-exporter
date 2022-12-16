import xlsxwriter
import re
max_row = 0
    
def export_to_xlsx(data, template):
    with xlsxwriter.Workbook('Output.xlsx') as wb:
        ws = wb.add_worksheet()

        for section in template.keys():
            if section == "head":
                generate_static_section_export(template[section], wb, ws, data)
            elif section == "table":
                generate_table_section_export(template[section], wb, ws, data)
            elif section == "foot":
                generate_static_section_export(template[section], wb, ws, data)
            else:
                print(f"Invalid Section: {section}")
            

def generate_static_section_export(section, workbook, worksheet, inp_data):
    global max_row
    for field in section:
        field_data = replace_var( field['data'] if 'data' in field.keys() else '', inp_data)
        position = replace_var( field['start'] if 'start' in field.keys() else [0, 0], inp_data)
        colspan = replace_var( field['colspan'] if 'colspan' in field.keys() else 1, inp_data)
        rowspan = replace_var(field['rowspan'] if 'rowspan' in field.keys() else 1, inp_data)
        align = replace_var( field['align'] if 'align' in field.keys() else 'left', inp_data)
        valign = replace_var( field['valign'] if 'valign' in field.keys() else 'vcenter', inp_data)

        cell_format = workbook.add_format({'align': align, 'valign':valign})

        if type(position[0]) == type(''):
            position[0] = eval(position[0])

        if type(position[1]) == type(''):
            position[1] = eval(position[1])

        if position[0] > max_row:
            max_row = position[0]

        if colspan > 1 or rowspan > 1:
            worksheet.merge_range(position[0], position[1], position[0] + rowspan - 1, position[1] + colspan - 1, field_data, cell_format )

        else:
            worksheet.write(position[0], position[1], field_data, cell_format)

def generate_table_section_export(section, workbook, worksheet, inp_data):
    global max_row
    table_data = replace_var(section['data'] if 'data' in section.keys() else [], inp_data)
    position = replace_var( section['start'] if 'start' in section.keys() else [0, 0], inp_data)
    header = replace_var( section['header'] if 'header' in section.keys() else True, inp_data)
    border = replace_var( section['border'] if 'border' in section.keys() else True, inp_data)
    columns = section['columns'] if 'columns' in section.keys() else []

    if header:
        for idx, col in enumerate(columns):
            worksheet.write(position[0], position[1] + idx, col['name'])

    for row_idx, row in enumerate(table_data, start = 1 if header else 0):
        for col_idx, col in enumerate(columns):
            col_val = replace_var(col['data'], row)
            worksheet.write(position[0] + row_idx, position[1] + col_idx, col_val)

    if max_row < position[0] + row_idx:
        max_row = position[0] + row_idx

def replace_var(field, data):
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
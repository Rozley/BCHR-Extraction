# extraction demo program

import csv
import io
import re
import pandas as pd
from local_templates.basic_information_template import local_basic_information_template
from local_templates.matrix_information_template import local_matrix_information_template, local_matrix_template
import extraction.calculate_matrix

filename = '../../data/17EDR_ACM.CSV'


def result_generator(file_data, basic_information_template, matrix_template, brand):
    result = {'brand': brand}
    if 'brand' in basic_information_template.keys():
        if 'brand' in basic_information_template['brand'].keys():
            item = basic_information_template['brand']['brand']
            result.setdefault(item[0], {})[item[1]] = brand

    # basic info extraction
    file_buffer = io.StringIO(file_data, newline='')
    csv_reader = csv.reader(file_buffer, delimiter=',', quotechar='"', dialect=csv.excel_tab)
    sub_title = ""
    for row in csv_reader:
        # record sub title
        if sub_title == "" and len(row) == 1 and row[0] in basic_information_template.keys():
            sub_title = row[0]
            continue
        # when find an empty row clear the sub title
        if len(row) == 0 or sub_title == "":
            sub_title = ""
            continue
        if row[0] in basic_information_template[sub_title].keys():
            item = basic_information_template[sub_title][row[0]]
            result.setdefault(item[0], {})[item[1]] = row[1].strip()

    # matrix info extraction
    file_buffer = io.StringIO(file_data, newline='')
    csv_reader = csv.reader(file_buffer, delimiter=',', quotechar='"', dialect=csv.excel_tab)
    sub_title = ""
    event = {}
    for row in csv_reader:
        # record sub title
        if sub_title == "" and len(row) == 1 and \
                re.sub("\(.*?\)$", "", row[0]).strip() in local_matrix_information_template.keys():
            sub_title = re.sub("\(.*?\)$", "", row[0]).strip()
            continue
        # when find an empty row clear the sub title
        if len(row) == 0 or sub_title == "":
            sub_title = ""
            continue
        if row[0] in local_matrix_information_template[sub_title].keys():
            item = local_matrix_information_template[sub_title][row[0]]
            if item[1] in event.keys():
                if item[0] not in result.keys():
                    result[item[0]] = []
                result[item[0]].append(event)
                event = {}
            event[item[1]] = row[1].strip()
    if event:
        if item[0] not in result.keys():
            result[item[0]] = []
        result[item[0]].append(event)
        event = {}


    # matrix calculation
    file_buffer = io.StringIO(file_data, newline='')
    csv_reader = csv.reader(file_buffer, delimiter=',', quotechar='"', dialect=csv.excel_tab)
    sub_title = ""
    mat_count = 0
    mat_header = []
    mat = []
    abstract = []
    is_recording_matrix = False
    is_recording_abstract = False
    for row in csv_reader:
        # if len(row) > 0:
        #     print(re.sub("\(.*?\)$", "", row[0]).strip())
        # record sub title
        if sub_title == "" and len(row) == 1 and \
                re.sub("\(.*?\)$", "", row[0]).strip() in matrix_template.keys():
            sub_title = re.sub("\(.*?\)$", "", row[0]).strip()
            continue

        # when find an empty row clear the sub title
        if sub_title == "":
            continue
        if len(row) == 0:
            if is_recording_matrix is True:
                is_recording_matrix = False
                mat_type = matrix_template[sub_title]
                mat_data = pd.DataFrame(mat, columns=mat_header)
                delta_v, angle, impact_level, event_type = extraction.calculate_matrix.matrix_classifier(mat_data, mat_type)
                result['bchr_summary'][mat_count]['pdof'] = angle
                result['bchr_summary'][mat_count]['max_delta_v'] = delta_v
                result['bchr_summary'][mat_count]['impact_level'] = impact_level
                result['bchr_summary'][mat_count]['event'] = event_type
                mat_count = mat_count + 1
            if is_recording_abstract is True:
                is_recording_abstract = False
                mat_type = matrix_template[sub_title]
                mat_data = pd.DataFrame(abstract, columns=["keywords", "item"])
                print(mat_data)
                delta_v, angle, impact_level, event_type = extraction.calculate_matrix.matrix_classifier(mat_data, mat_type)
                result['bchr_summary'][mat_count]['pdof'] = angle
                result['bchr_summary'][mat_count]['max_delta_v'] = delta_v
                result['bchr_summary'][mat_count]['impact_level'] = impact_level
                result['bchr_summary'][mat_count]['event'] = event_type
                mat_count = mat_count + 1
            sub_title = ""
            mat = []
            abstract = []
            mat_header = []
            continue

        # calculate matrix
        mat_type = matrix_template[sub_title]
        if mat_type == "Abstract":
            is_recording_abstract = True
            abstract.append(row)
        if is_recording_matrix is False and re.search('^Time \(msec\)', row[0]):
            is_recording_matrix = True
            mat_header = row
        elif is_recording_matrix is True:
            mat.append(row)
    print(result)
    return result

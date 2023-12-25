# calculate_matrix
# input matrix

import pandas as pd
import re
import sys
import math

filename = '../../data/test_data_hybrid.csv'
longitudinal_regex = 'LONGITUDINAL'
lateral_regex = 'LATERAL'
num_regex = r'-?[0-9]+\.[0-9]*|-?[0-9]+'
mps2_regex = r'(\(m\/s\^2\))|(\(\%?ms\))'
kmph2_regex = r'\(km\/h\)'


def read_data(filepath):
    df = pd.read_csv(filepath, header=1, index_col=False)
    hd = df.columns
    # print(df)
    # print(hd)

    # check the type of the matrix
    mat_type = None
    lat_flag = False
    lon_flag = False

    for item in hd:
        if re.search(lateral_regex, item.upper()) is not None:
            lat_flag = True

        if re.search(longitudinal_regex, item.upper()) is not None:
            lon_flag = True

    if lat_flag and lon_flag:
        mat_type = "Hybrid"
    elif lat_flag:
        mat_type = "Lateral"
    elif lon_flag:
        mat_type = "Longitudinal"
    else:
        pass
    return df, mat_type


def unit_finder(text):
    if re.search(mps2_regex, text):
        return "m/s^2"
    elif re.search(kmph2_regex, text):
        return "km/h^2"
    else:
        return ""


def calculate_hybrid_matrix(df):

    # find the max lateral delta_v and the max longitudinal delta_v
    lat_dv = 0
    lon_dv = 0
    lat_r = sys.maxsize
    lon_r = sys.maxsize
    t_col = df.columns[0]
    lat_unit = ""
    lon_unit = ""
    unit = ""
    for col in df.columns:
        if re.search(longitudinal_regex, col) is not None:
            for i in range(len(df[col])):
                item = df[col][i]
                if re.match(num_regex, str(item)):
                    if abs(lon_dv) < abs(float(item)):
                        lon_dv = float(item)
                        lat_r = i
                        lon_unit = unit_finder(col)

        if re.search(lateral_regex, col.upper()) is not None:
            for i in range(len(df[col])):
                item = df[col][i]
                if re.match(num_regex, str(item)):
                    if abs(lat_dv) < abs(float(item)):
                        lat_dv = float(item)
                        lon_r = i
                        lat_unit = unit_finder(col)

    tr = min(lat_r, lon_r)

    # select the latest max delta_v
    lat_dv = 0
    lon_dv = 0
    for col in df.columns:
        if re.search(longitudinal_regex, col.upper()) is not None:
            if abs(lon_dv) < abs(float(df[col][tr])):
                lon_dv = float(df[col][tr])
                unit = lat_unit

        if re.search(lateral_regex, col.upper()) is not None:
            if abs(lat_dv) < abs(float(df[col][tr])):
                lat_dv = float(df[col][tr])
                unit = lon_unit

    # calculate sum delta_v and sum angle
    sum_dv = pow(pow(lon_dv, 2) + pow(lat_dv, 2), 0.5)
    sum_ang = math.degrees(math.atan(lat_dv/lon_dv))
    if sum_ang < 0:
        sum_ang += 360
    if lon_dv > 0:
        sum_ang += 180

    return str(round(abs(sum_dv), 2)) + unit, str(round(sum_ang, 2))


def calculate_lateral_matrix(df):
    lat_dv = 0
    lat_r = sys.maxsize
    t_col = df.columns[0]
    lat_unit = ""
    for col in df.columns:
        if re.search(lateral_regex, col.upper()) is not None:
            for i in range(len(df[col])):
                item = df[col][i]
                if re.match(num_regex, str(item)):
                    if abs(lat_dv) < abs(float(item)):
                        lat_dv = float(item)
                        lat_r = i
                        lat_unit = unit_finder(col)

    sum_dv = lat_dv
    sum_ang = 90
    if lat_dv > 0:
        sum_ang += 180
    return str(round(abs(sum_dv), 2)) + lat_unit, str(round(sum_ang, 2))


def calculate_longitudinal_matrix(df):
    lon_dv = 0
    lon_r = sys.maxsize
    t_col = df.columns[0]
    lon_unit = ""
    for col in df.columns:
        if re.search(longitudinal_regex, col.upper()) is not None:
            for i in range(len(df[col])):
                item = df[col][i]
                if re.match(num_regex, str(item)):
                    if abs(lon_dv) < abs(float(item)):
                        lon_dv = float(item)
                        lon_r = i
                        lon_unit = unit_finder(col)
    sum_dv = lon_dv
    sum_ang = 0
    if lon_dv < 0:
        sum_ang += 180
    return str(round(abs(sum_dv), 2)) + lon_unit, str(round(sum_ang, 2))


def calculate_rollover_matrix(df):
    return "", ""


def calculate_abstract(df):
    lon_flag = False
    lat_flag = False
    lon_dv = 0
    lat_dv = 0
    sum_dv = 0
    max_dv = 0
    lon_unit = ""
    lat_unit = ""
    max_unit = ""
    unit = ""
    sum_dv = ""
    sum_ang = ""
    evt_type = ""
    for i in range(len(df['keywords'])):
        key = df['keywords'][i]
        item = re.sub(",", "", df['item'][i])
        if not re.match(num_regex, item):
            continue
        if re.search(longitudinal_regex, key.upper()) is not None:
            if not lon_flag:
                lon_unit = unit_finder(key)
                lon_dv = float(item)
                lon_flag = True
            elif unit_finder(key) is "km/h^2":
                lon_unit = unit_finder(key)
                lon_dv = float(item)
        elif re.search(lateral_regex, key.upper()) is not None:
            if not lat_flag:
                lat_unit = unit_finder(key)
                lat_dv = float(item)
                lat_flag = True
            elif unit_finder(key) is "km/h^2":
                lat_unit = unit_finder(key)
                lat_dv = float(item)
        if re.search("Max", key) and max_dv < abs(float(item)):
            max_unit = unit_finder(key)
            max_dv = float(item)
    if lon_dv == 0 and lat_dv == 0:
        if max_dv == 0:
            evt_type = "Invalid"
        else:
            evt_type = "Pedestrian"
        sum_dv = str(round(abs(max_dv), 2)) + max_unit
        sum_ang = ""
    elif abs(lon_dv) > abs(lat_dv):
        evt_type = "Longitudinal"
        sum_dv = str(round(abs(lon_dv), 2)) + lon_unit
        if lon_dv >= 0:
            sum_ang = "0"
        else:
            sum_ang = "180"
    elif abs(lon_dv) < abs(lat_dv):
        evt_type = "Lateral"
        sum_dv = str(round(abs(lat_dv), 2)) + lat_unit
        if lat_dv >= 0:
            sum_ang = "270"
        else:
            sum_ang = "90"
    return sum_dv, sum_ang, evt_type


def matrix_classifier(df, mt):
    delta_v = ""
    angle = ""
    impact_level = ""
    event_type = mt
    if mt == 'Hybrid':
        delta_v, angle =  calculate_hybrid_matrix(df)
    elif mt == 'Lateral':
        delta_v, angle =  calculate_lateral_matrix(df)
    elif mt == 'Longitudinal':
        delta_v, angle = calculate_longitudinal_matrix(df)
    elif mt == 'Rollover':
        delta_v, angle = calculate_rollover_matrix(df)
    elif mt == 'Abstract':
        delta_v, angle, event_type = calculate_abstract(df)
    if delta_v:
        impact_level = cal_level(delta_v)
    return delta_v, angle, impact_level, event_type + " Crash"


def cal_level(dv):
    imp_l = "0"
    res = re.search(num_regex, dv)
    if float(res[0]) > 100.0:
        imp_l = "2"
    elif float(res[0]) > 10.0:
        imp_l = "1"
    return imp_l


if __name__ == "__main__":
    dataframe, matrix_type = read_data(filename)
    delta_v, angle, impact_level = matrix_classifier(dataframe, matrix_type)
    print(f'delta_v = {delta_v}, angle = {angle}, impact_level = {impact_level}')
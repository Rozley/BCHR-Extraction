def template_parser(data_param):
    basic_information_template = {}
    matrix_template = {}

    cdr_list = data_param["cdrFileInformation"]
    veh_list = data_param["vehicleInformation"]
    mat_list = data_param["dataMatrix"]
    brand = data_param["brand"]

    for item in cdr_list:
        if item["module"] not in basic_information_template.keys():
            basic_information_template[item["module"]] = {}
        basic_information_template[item["module"]][item["keywords"]] = ["cdr_info", item["attribute"]]

    for item in veh_list:
        if item["module"] not in basic_information_template.keys():
            basic_information_template[item["module"]] = {}
        basic_information_template[item["module"]][item["keywords"]] = ["vehicle_info", item["attribute"]]

    for item in mat_list:
        matrix_template[item["keywords"]] = item["correspondingAlgorithm"]

    return basic_information_template, matrix_template, brand

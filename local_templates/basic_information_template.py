# local basic info template
# input : csv file
# output: report data

local_basic_information_template = {
    "CDR FILE INFORMATION": {
        "User Entered VIN/Frame Number": ["vehicle_info", "vin"],
        "User": ["cdr_info", "user"],
        "Case Number": ["cdr_info", "case_number"],
        "Filename": ["cdr_info", "filename"],
        "Saved on": ["cdr_info", "cdr_retrieval_date_and_time"],
        "Imaged with CDR version": ["cdr_info", "imaged_with_cdr_version"],
        "Reported with CDR version": ["cdr_info", "reported_with_cdr_version"],
        "Event(s) recovered": ["cdr_info", "events_recovered"],
        "Crash Date": ["vehicle_info", "first_registration"],
    },
    "SYSTEM STATUS AT RETRIEVAL": {
        "ECU Part Number": ["cdr_info", "ecu_part_number"],
        "EDR Generation": ["cdr_info", "edr_generation"],
        "Complete File Recorded": ["cdr_info", "complete_file_recorded"],
        "Ignition Cycle, Download (times)": ["cdr_info", "ignition_cycle_at_download"],
    },
}
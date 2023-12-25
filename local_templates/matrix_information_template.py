# local matrix info template
# input : csv file
# output: report data

local_matrix_information_template = {
    "SYSTEM STATUS AT EVENT": {
        "TRG Count (times)": ["bchr_summary", "event_count"],
        "Multi-event, Number of Events": ["bchr_summary", "event_count"],
        "Recording order information": ["bchr_summary", "event_count"],
        "Event Type": ["bchr_summary", "event_type"],
        "Ignition Cycle, Crash": ["bchr_summary", "ig_cycle_count"],
        "Ignition Cycle, Download (cycles)": ["bchr_summary", "ig_cycle_count"],
        "Ignition Cycle, Frontal Crash (times)": ["bchr_summary", "ig_cycle_count"],
        "Ignition Cycle, RH Side Crash (times)": ["bchr_summary", "ig_cycle_count"],
        "Ignition Cycle, LH Side Crash (times)": ["bchr_summary", "ig_cycle_count"]
    },
    "DTCS PRESENT AT TIME OF EVENT": {
        "Ignition Cycle Since DTC was Set (times)": ["bchr_summary", "ig_cycle_count"],
    },
}

local_matrix_template = {
    "LATERAL CRASH PULSE": "Lateral",
    "LONGITUDINAL CRASH PULSE": "Longitudinal",
    "LONGITUDINAL/LATERAL CRASH PULSE": "Hybrid",
    "ROLLOVER CRASH PULSE": "Rollover",
    # Abstract Mode can not work with other algorithms together, try avoid using them together within a single brand.
    "SYSTEM STATUS AT EVENT": "Abstract",
}


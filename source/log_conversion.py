import pandas as pd
import pm4py

def from_csv_to_xes(csv_path, xes_converted):
    dataframe = pd.read_csv(csv_path, sep=';')
    dataframe = pm4py.format_dataframe(dataframe, case_id="base_case_id", activity_key="concept:name", timestamp_key="time:timestamp")
    event_log = pm4py.convert_to_event_log(dataframe)
    pm4py.write_xes(event_log, xes_converted)
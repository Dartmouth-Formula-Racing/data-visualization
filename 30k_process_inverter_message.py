import pandas as pd
from candecoder import decode_message_by_id
from datetime import timedelta, datetime
from ast import literal_eval

data = pd.read_csv('./records.csv') 
data_cut = data.iloc[:30000] # Subset main data to 30k rows

header = ['Timestamp', 'Variable', 'Value', 'Units'] # Create column titles
processed_data = pd.DataFrame(columns=header) # Create new dataframe 
required_cols = ["rawtime"] + ["id"] + [f"data{n}" for n in range(0, 8)] # Create list of desired columns


def extractDateInfo(rawtime): # Process time from records data
    days = timedelta(days=rawtime)
    date = datetime(year=1899, month=12, day=30) + days
    return pd.to_datetime(date)

def map_row(rawtime, id, *hex_bytes): # Process main data 
    try:
        data_bytes = [int(hex_byte, 16) for hex_byte in hex_bytes]
        values = decode_message_by_id(id, data_bytes)
        ret_values = pd.DataFrame(columns=header)
        for variable, value in values.items():
            if type(value) == tuple:
                ret_values.loc[len(ret_values)] = {
                    "Timestamp": extractDateInfo(rawtime),
                    "Variable": variable,
                    "Value": value[0],
                    "Units": value[1]
                }
            else:
                ret_values.loc[len(ret_values)] = {
                    "Timestamp": extractDateInfo(rawtime),
                    "Variable": variable,
                    "Value": value,
                    "Units": None
                }
        return ret_values
    except:
        return None
    
dfs = [map_row(*row) for row in zip(*[data_cut[col] for col in required_cols]) ] # Call functions, process and create list of dfs
dfs = pd.concat(dfs) # Concat list of dfs to one df

dfs.to_csv("./30k_processed_records.csv") # Save df to csv

import pandas as pd
import csv
import math

# variables
test_file = 'module_configurations.csv'
batch_file = 'batch_file.csv'

# functions

def read_config(test_file):
    try:
        config = pd.read_csv(test_file, header=0)
    except FileNotFoundError:
        logging.error("File not found")
        print("File not found. Please check the file path.")
    except pd.errors.ParserError:
        logging.error("Parsing failed")
        print("Error occurred while parsing the CSV file.")
    return config

def get_config(index, config):
    configRow = config.iloc[index-1]
    configRowAsKwargs = configRow.to_dict()
    return configRowAsKwargs

def write_batch(batch_size, file_path, config_df, batch_df):
    rows =0
    transmit_time = 0
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)    
        writer.writerow(['bat'])
        print(len(config_df))

        while rows < len(config_df):
            print(batch_size)
            selected_rows = config_df.iloc[batch_size-17:batch_size]
            print(selected_rows) 
            for index, row in selected_rows.iterrows():
                config = get_config(index, config_df)
                mode = config['mod']
                frequency = config['freq']
                spreadingFactor = config["sf"]
                bandWidth = config["bw"]
                codingRate = config["cr"]
                power = config["pwr"]
                maxPayload = 23
                rows += 1
                transmit_time += timeOnAir(spreadingFactor, bandWidth, codingRate, "off", "off", maxPayload, 8)
           
            time = [transmit_time]    
            writer.writerow(time)
            
            transmit_time = 0
            batch_size += 17

      

def timeOnAir( spreadfactor, bandwidth, codingrate, header="off", optimization="on", payload_size=23, preamble_length=8):
        # Convert input parameters to appropriate values
        sf = int(spreadfactor[2:])
        bw = bandwidth * 1000
        cr_num, cr_denom = map(int, codingrate.split('/'))
        h = 1 if header.lower() == "on" else 0
        opt = 1 if optimization.lower() == "on" else 0
        # Calculate symbol duration
        tsym = (2 ** sf) / bw
        # Calculate number of preamble symbols
        preamble_symbols = preamble_length + 4.25
        # Calculate preamble duration
        preamble_duration = tsym * preamble_symbols
        # Calculate number of payload symbols
        payload_symbols = 8 + math.ceil(
            (
                (8 * payload_size - 4 * sf + 28 + 16 - 20 * h + 8 * opt)
                / (4 * (sf - 2 * opt))
            )
        ) * (cr_num + 4)
        # Calculate payload duration
        payload_duration = tsym * payload_symbols
        # Calculate total airtime (LoRa packet duration)
        airtime = preamble_duration + payload_duration
        return airtime


config_df = read_config(test_file)
batch_df = pd.DataFrame() 
print("files are read")

write_batch(batch_size=17, file_path=batch_file, config_df=config_df, batch_df=batch_df)
print("done")


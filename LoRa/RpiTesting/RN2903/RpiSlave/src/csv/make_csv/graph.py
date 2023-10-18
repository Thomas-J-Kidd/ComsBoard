import matplotlib.pyplot as plt
import pandas as pd

def read_config(file):
    try:
        df = pd.read_csv(file, header=0)
    except FileNotFoundError:
        print("Config file not found. Please check the file path.")
    except pd.errors.ParserError:
        print("Error occurred while parsing the CSV file.")
    return df



send_time = "time_to_send.csv"
df = read_config(send_time)
df.reset_index(inplace=True)


plt.plot(df['index'], df['avg time to send'])
plt.xlabel('Config Number')
plt.ylabel('Average Time to Send a data and change configurations')
plt.title('Time to send data using RN2903')
plt.show()

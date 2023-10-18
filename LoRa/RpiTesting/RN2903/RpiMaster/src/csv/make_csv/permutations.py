
possRadioConfigs = {
    "sf":["sf7", "sf8", "sf9", "sf10", "sf11", "sf12"],
    #"sf":["sf7", "sf8" ],
    "bw": [125, 250, 500],
    "cr":["4/5", "4/6", "4/7", "4/8"],
    "freq":"915000000",
    "pwr":[20, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
    "mod":"lora",
    "wdt":0

}


import csv

def generate_module_configurations_to_csv(file_path, **kwargs):
    # Retrieve the values for each configuration option
    sf_options = kwargs.get("sf", [])
    bw_options = kwargs.get("bw", [])
    cr_options = kwargs.get("cr", [])
    freq = kwargs.get("freq", "")
    pwr_options = kwargs.get("pwr", [])
    mod = kwargs.get("mod", "")
    wdt = kwargs.get("wdt", 0)

    # Open the CSV file for writing
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["sf", "bw", "cr", "freq", "pwr", "mod", "wdt"])

        # Generate and write all possible configurations
        for sf in sf_options:
            for bw in bw_options:
                for cr in cr_options:
                    for pwr in pwr_options:
                        configuration = [sf, bw, cr, freq, pwr, mod, wdt]
                        writer.writerow(configuration)



file_path = "csv_test.csv"
generate_module_configurations_to_csv(file_path, **possRadioConfigs)



import csv

# Function to add a new column to the CSV file
def add_column_to_csv(input_file, output_file, new_column_header, new_column_data):
    # Read the input CSV file
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)  # Convert the CSV data into a list

    # Add the new column header to the first row
    data[0].append(new_column_header)

    # Add the new column data to each row
    for batch in range(72):
        for row in data[(batch*17)+1:(batch*17)+18]:
            row.append(batch)

    # Write the modified data to the output CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Example usage
input_file = 'csv_test.csv'
output_file = 'csv_test_with_batch_label.csv'
new_column_header = 'batch_num'
new_column_data = 'Value'

add_column_to_csv(input_file, output_file, new_column_header, new_column_data)


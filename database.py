import csv


# We are using .csv for data storage for the sake for simplicity and universal.

# Establishing handle with our csv file
def get_csv_rw_handle(fileName):
    with open(fileName + ".csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
    return csv_reader

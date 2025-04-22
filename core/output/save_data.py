import datetime
import os
from zoneinfo import ZoneInfo
import csv


def write_data_to_csv(SENSORS, row_data, file_prefix="Sens_Box", directory="data", max_rows=10000):
    """Prints the measurement values to a CSV, adds header if necessary

    :param row_data: (Dictionary of {Sensor_name, value})
    :param file_prefix: (_type_, optional): identifier added to CSV file name. Defaults to device_name.
    :param directory: (str, optional): Directory the files are saved in. Defaults to /data.
    :param max_rows: (int, optional): max length of file. Defaults to 10000.
    """
    
    timestamp = datetime.datetime.now(tz=ZoneInfo("Europe/Berlin"))
    # Track how many rows have been written
    # If no row or file numbering exist create them
    if not hasattr(write_data_to_csv, "row_count"):
        write_data_to_csv.row_count = 0
        write_data_to_csv.file_index = 0

    # Create folder if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Rotate file if limit reached
    if write_data_to_csv.row_count % max_rows == 0:
        filename = f"{file_prefix}_{write_data_to_csv.file_index:03d}_{timestamp.isoformat()}.csv" 
        write_data_to_csv.current_file = os.path.join(directory, filename)
        write_data_to_csv.file_index += 1
        write_data_to_csv.need_header = True
    else:
        write_data_to_csv.need_header = False

    # Write data to the current file 
    with open(write_data_to_csv.current_file, "a", newline="") as csv_file:
        
        fieldnames = ["timestamp"] + [label for label, _ in SENSORS] # Create the correct order of the column labels
        row_data["timestamp"] = timestamp.strftime("%d/%m/%Y %H:%M:%S") #TODO Maybe change to .isoformat(): 2025-04-11T15:24:02
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if write_data_to_csv.need_header:
            writer.writeheader()

        writer.writerow(row_data)
        write_data_to_csv.row_count += 1  
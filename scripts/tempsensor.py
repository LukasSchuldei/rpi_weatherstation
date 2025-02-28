#!/usr/bin/env python
import os
import glob
import time
import datetime
import csv

def read_temp(decimals=1):
    """Reads the temperature from a 1-wire device and returns it."""
    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"
    try:
        with open(device, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            with open(device, "r") as f:
                lines = f.readlines() 
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = round(float(temp_string) / 1000.0, decimals)
            return temp
    except IndexError:
        print("Sensor not found or not connected properly.")
        return None

def write_to_csv():
    """Writes the timestamp and temperature to a CSV file."""
    while True:
        timestamp = datetime.datetime.now()
        temperature = read_temp()
        
        if temperature is not None:
            date_str = timestamp.strftime("%Y%m%d")
            filename = os.path.join(os.getcwd(), 'data', f"tempdata_{date_str}.csv")

            # Ensure the data directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            file_exists = os.path.isfile(filename)
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['Timestamp', 'Temperature']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header only if the file doesn't exist
                if not file_exists:
                    writer.writeheader()

                writer.writerow({'Timestamp': timestamp.strftime("%d/%m/%Y %H:%M:%S"), 'Temperature': temperature})

        time.sleep(900)  # Set the interval for data logging, 15min

if __name__ == "__main__":
    # To run log data, uncomment below:
    write_to_csv()

    # To only read temperature data, uncomment below:
    # print(read_temp())

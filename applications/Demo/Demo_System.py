#!/usr/bin/env python
import os
import time
import datetime
import csv
from zoneinfo import ZoneInfo

# Import Output functions
from core.output.display_to_lcd import print_to_LCD
from core.output.plot_to_commandline import plot_sensor_data


# Import sensor read functions
from core.sensors.temp_DS18B20 import read_temperature
from core.sensors.humid_demo import read_humidity
from core.sensors.pres_demo import read_pressure

# Import utilities 
from core.output.save_data import write_data_to_csv

device_name= "Peter" #TODO Create .env import
measurement_interval=1 # Set the interval between measurements, in seconds: 900 = 15 min
test_mode= True # To only print into command line, change to True

    
    
# Edit list to add/change sensor-readouts
# First: label of sensor, second: function that reads sensor
# Example: ("temperature", read_temperature)
SENSORS = [
    ("temperature", read_temperature),
    ("pressure", read_pressure),
    ("humidity", read_humidity)
    
]


def get_sensor_data(): # Calls sensor read functions from list SENSORS, creates dictionary with label of sensor and returned value
    #TODO add timestamp here, but as first key in the dictionary
    return {label: func() for label, func in SENSORS}    


     
# Log data to csv indefinetly         
def measurement_loop(test_mode):
    
    if test_mode: # Save data, print to console and to LCD-Display
        
        while True:        
            sensor_data=get_sensor_data()
            write_data_to_csv(SENSORS, sensor_data, file_prefix=device_name)
            print(sensor_data)
            time.sleep(measurement_interval)
            plot_sensor_data(write_data_to_csv.current_file)
            
    else:
        while True:        
            print_to_LCD(measurement_values=sensor_data)
            write_data_to_csv(get_sensor_data()) # Save data to csv
            time.sleep(measurement_interval)
        
if __name__ == "__main__":
        
    measurement_loop(test_mode)

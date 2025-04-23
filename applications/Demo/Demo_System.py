#!/usr/bin/env python
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import Output functions
from core.output.display_to_lcd import print_to_LCD
from core.output.plot_to_commandline import plot_sensor_data


# Import sensor read functions
from core.sensors.temp_DS18B20 import temp_ds18b20
from core.sensors.BME680 import temp_bme680, pressure_bme680, rel_hum_bme680

# Import utilities 
from core.output.save_data import write_data_to_csv

device_name= "Peter" #TODO Create .env import
measurement_interval=1 # Set the interval between measurements, in seconds: 900 = 15 min
test_mode= True # To only print into command line, change to True

    
    
# Edit list to add/change sensor-readouts
# First: label of sensor, second: function that reads sensor
# Example: ("temperature", read_temperature)
SENSORS = [
    ("temp_ds18", temp_ds18b20),
    ("temp_bme680", temp_bme680),
    ("pressure", pressure_bme680),
    ("humidity", rel_hum_bme680)
    
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
            plot_sensor_data(write_data_to_csv.current_file)
            print_to_LCD(measurement_values=sensor_data)
            time.sleep(measurement_interval)
            
    else:
        while True:    
            sensor_data=get_sensor_data()
            print(sensor_data)
            write_data_to_csv(SENSORS, sensor_data, file_prefix=device_name) # Save data to csv       
            time.sleep(measurement_interval)
    
if __name__ == "__main__":
        
    measurement_loop(test_mode)

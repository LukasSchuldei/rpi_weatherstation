import board #pip install adafruit-blinka
from lcd.lcd import LCD #pip3 install adafruit-circuitpython-lis3dh 
from lcd.lcd import CursorMode
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import time 

def print_to_LCD(measurement_values):
    
        # Initialize LCD with 2 rows and 16 columns, if not present
    if not hasattr(print_to_LCD, "lcd"):
        print_to_LCD.lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows=2, num_cols=16)

    """
    Displays sensor data on a 2x16 LCD, 2 sensors at a time.
    Rotates through all sensors every 2 seconds if more than 2.
    
    :param measurement_values: Dictionary of {sensor_name: value}
    """
    sensor_items = list(measurement_values.items())
    total_sensors = len(sensor_items)

    # Display two sensors at a time
    for i in range(0, total_sensors, 2):
        print_to_LCD.lcd.clear()
        # First line
        if i < total_sensors:
            key1, val1 = sensor_items[i]
            line1 = f"{key1[:4]}: {val1}"[:16]
            print_to_LCD.lcd.set_cursor_pos(0, 0)
            print_to_LCD.lcd.print(line1)
        # Second line
        if i + 1 < total_sensors:
            key2, val2 = sensor_items[i + 1]
            line2 = f"{key2[:4]}: {val2}"[:16]
            print_to_LCD.lcd.set_cursor_pos(1, 0)
            print_to_LCD.lcd.print(line2)

        time.sleep(2)  # Pause to rotate display
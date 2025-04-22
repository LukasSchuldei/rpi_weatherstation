import board #pip install adafruit-blinka
from core.output.lcd.lcd import LCD #pip3 install adafruit-circuitpython-lis3dh 
from core.output.lcd.lcd import CursorMode
from core.output.lcd.i2c_pcf8574_interface import I2CPCF8574Interface

def print_to_LCD(measurement_values):
    """
    Displays sensor data on a 2x16 LCD, 2 sensors 
    
    :param measurement_values: Dictionary of {sensor_name: value}
    """
    
    # Initialize LCD with 2 rows and 16 columns, if not present
    if not hasattr(print_to_LCD, "lcd"):
        print_to_LCD.lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows=2, num_cols=16)

    sensor_items = list(measurement_values.items())
    total_sensors = len(sensor_items)

    # Print the first two measurement values onto the display
    print_to_LCD.lcd.clear()
    
    for i in range(0,2):
        try:
            key, val = sensor_items[i]
            line = f"{key[:4]}: {val}"[:16]
            print_to_LCD.lcd.set_cursor_pos(i, 0)
            print_to_LCD.lcd.print(line)
            
        except ValueError:
            print(f"No {i}. element in measurement_values")

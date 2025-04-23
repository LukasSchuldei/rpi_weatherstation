import glob
import time



def temp_ds18b20(decimals=1):
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
        #TODO add error logging
        return None
    
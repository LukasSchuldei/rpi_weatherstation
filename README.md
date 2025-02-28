# rpi_weatherstation


## Table of Contents

- DS18B20 Temperature Sensor
- Wiring the Sensor
- Load the Sensor on Your Raspberry Pi
- Read the Temperature in Python
- Change the Default Pin

## DS18B20 Temperature Sensor

The DS18B20 is a digital temperature sensor that can measure temperatures between -55°C and +125°C with the Raspberry Pi, with the input and output linked on the same wire.

## Wiring the Sensor

When you order the DS18B20, it should come with a 4.7K resistor cable. The DS18B20 has three wires: a ground wire (white), the power at 3.3V (red), and the data wire (yellow). Pin assignment depending on the version:

    Red (VCC), Yellow (DATA), Black (GND)
    Red (VCC), White (DATA), Black (GND)
    Red (VCC), Yellow (DATA), White (GND)

## Load the Sensor on Your Raspberry Pi

Now that the sensor is connected, turn on your Raspberry Pi. The first thing to do is to enable the 1-wire interface, which is required to read out the data of the DS18B20. To do this using the Desktop interface, go to Preferences > Raspberry Pi Configuration > Interfaces > and click Enabled for 1-wire. Alternatively, use the `raspi-config` tool using the terminal. Now reboot your Raspberry Pi (`sudo reboot`).

We will now need to identify the serial number of the sensor, which we enable by adding the 1-Wire and thermometer drivers to the Raspberry Pi:

```bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
```

To check if the DS18B20 has connected, go to the directory of the 1-Wire devices and list those available:

```bash
cd /sys/bus/w1/devices/
ls
```

You should now see a folder that starts with `28-xxxxxx`. This is the serial number of the sensor. You can read out the raw temperature directly in the terminal by going to the folder `cd 28-xxxxxx` and typing in `cat w1_slave`. The temperature is provided after the `t=` in thousands of a degree.

## Change the Default Pin

If you want to change the default pin from GPIO4 to another pin, you need to modify the `/boot/config.txt` file. Add the following line to the file:

```bash
dtoverlay=w1-gpio,gpiopin=X
```

Replace `X` with the GPIO pin number you want to use. For example, to use GPIO2, you would add:

```bash
dtoverlay=w1-gpio,gpiopin=2
```

After making this change, reboot your Raspberry Pi (`sudo reboot`).

## Setting Up a systemd Service for the tempsensor.py Script 

A systemd service has been configured to automatically start the tempsensor.py script upon system boot. This script is responsible for reading temperature data from a sensor and logging it. 
Service Configuration Details 

Here is the configuration of the service file:

```
[Unit]
Description=tempsensor.py service
After=network.target

[Service]
ExecStart=python /your/path/to/rpi_weatherstation/scripts/tempsensor.py
WorkingDirectory=/your/path/to/rpi_weatherstation/
Restart=always
User=****
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
``` 
 

    Description:  Provides a brief description of the service and its purpose.
    After:  Ensures that the network service is up and running before executing the script.
    ExecStart:  Specifies the command to start the Python script.
    WorkingDirectory:  Sets the working directory from which the script is executed.
    Restart:  Configures the service to automatically restart if it stops unexpectedly.
    User:  The user under which the service runs. Replace `****` with the appropriate user name.
    Environment:  Sets environment variables, in this case ensuring Python does not buffer output.


This should cover the basics of connecting and reading from the DS18B20 temperature sensor with your Raspberry Pi. Happy monitoring!

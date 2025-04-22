#!/bin/bash

### HAVENT TESTED THIS YET
# This script performs various configuration and installation steps on a Raspberry Pi.
# It configures the 1-Wire interface, installs Docker, and sets up Home Assistant with Docker Compose.

# Enable the 1-Wire interface using raspi-config in non-interactive mode
echo "Enabling 1-Wire interface..."
sudo raspi-config nonint do_onewire 0

# Load the 1-Wire kernel modules
echo "Loading 1-Wire kernel modules..."
sudo modprobe w1-gpio
sudo modprobe w1-therm

# Verify that the 1-Wire sensor is detected
echo "Verifying 1-Wire sensor..."
cd /sys/bus/w1/devices/
if [ -d "28-*" ]; then
    echo "1-Wire sensor detected."
    SENSOR_DIR=$(ls -d 28-*)
    echo "Sensor directory: $SENSOR_DIR"
    cat $SENSOR_DIR/w1_slave
else
    echo "1-Wire sensor not detected. Please check your wiring and sensor."
fi

echo "1-Wire configuration completed."

# Install Docker
echo "Installing Docker..."
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker ${USER}
groups ${USER}
sudo systemctl enable docker

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version
sudo docker run hello-world
docker images

# Create and configure the Docker Compose directory for Home Assistant
echo "Creating and configuring Docker Compose for Home Assistant..."
mkdir -p docker/homeAssistant
cd docker/homeAssistant/

# Create the docker-compose.yml file for Home Assistant
echo "Creating docker-compose.yml for Home Assistant..."
cat <<EOF > docker-compose.yml
---
version: '3'
services:
    homeassistant:
        image: lscr.io/linuxserver/homeassistant
        container_name: homeassistant
        network_mode: host
        environment:
            - PUID=1000
            - PGID=1000
            - TZ=Europe/Berlin
        volumes:
            - /home/pi/docker/homeAssistant/data:/config
EOF

# Display the docker-compose.yml file
echo "Displaying docker-compose.yml file..."
cat docker-compose.yml

# Start Home Assistant with Docker Compose
echo "Starting Home Assistant with Docker Compose..."
sudo docker compose up -d

# Edit the Home Assistant configuration file
echo "Editing the Home Assistant configuration file..."
vim configuration.yaml

# Edit the Raspberry Pi configuration file
echo "Editing the Raspberry Pi configuration file..."
sudo nano /boot/firmware/config.txt

echo "Script completed."

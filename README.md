# Home Assistant Integration for Studer Devices

This project implements the Studer-Innotec Xcom protocol for communication with Studer devices via Xcom-232i. It enables seamless integration with home automation systems, particularly Home Assistant, through MQTT.

This project uses the xcom_proto protocol implementation from [zocker-160](https://github.com/zocker-160). Many thanks for this great work that made this integration possible.

## Features

- Complete communication with Studer devices through Xcom protocol
- Extensive data collection:
  - AC Power metrics (in/out, energy, frequency, voltage, current)
  - Battery metrics (voltage, current, power, state of charge, temperature, cycles)
  - Solar panel metrics (VarioTrack & VarioString)
  - System states and statistics
- Real-time MQTT publishing
- Full Home Assistant integration with pre-configured sensors
- Lightweight implementation (runs perfectly on a Raspberry Pi 1!)

## Prerequisites

- A Raspberry Pi (even a Pi 1 is sufficient!) or equivalent running Linux
- A Studer device Xcom-232i interface (available from [Fangpusun](https://www.fangpusun.com/communication-module-xcom-232i) for around $80 - works perfectly with Studer equipment as it's the exact same hardware)
- USB to Serial adapter cable ([recommended model on Amazon](https://www.amazon.fr/dp/B00QUZY4UG))
- Python 3.x
- MQTT broker (like Mosquitto)
- Home Assistant
- Network connection for the Raspberry Pi

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jackylaviss/homeassistant-studer-integration.git
cd homeassistant-studer-integration
```

2. Run the installation script as root:
```bash
sudo ./install.sh
```

The installation script will:
- Install required system dependencies (python3, pip, etc.)
- Prompt for all configuration information:
  - Serial port for Xcom-232i
  - MQTT broker IP address
  - MQTT port
  - MQTT username
  - MQTT password
- Install the project in `/opt/xcom-protocol`
- Configure and start systemd service for automatic startup

## Service Management

Once installed, you can manage the service with these commands:
```bash
# Check service status
sudo systemctl status xcom-protocol

# Start the service
sudo systemctl start xcom-protocol

# Stop the service
sudo systemctl stop xcom-protocol

# Restart the service
sudo systemctl restart xcom-protocol

# View logs
sudo journalctl -u xcom-protocol -f
```

## Home Assistant Integration

1. Copy `homeassistant/xcom-sensors.yaml` from this repository to your Home Assistant configuration directory. The location of this directory depends on your Home Assistant installation method.

2. Add the following to your Home Assistant `configuration.yaml`:
```yaml
mqtt: !include xcom-sensors.yaml
```

Alternatively, if you already have MQTT configured, you can include just the sensors:
```yaml
mqtt:
  sensor: !include xcom-sensors.yaml
```

All sensors will be automatically configured with:
- Appropriate units of measurement
- Device classes
- Logical grouping
- Ready for dashboard creation

After modifying your configuration, restart Home Assistant to apply the changes.

## Manual Configuration (if needed)

If you need to modify the configuration after installation:

1. Edit the configuration file:
```bash
sudo nano /opt/xcom-protocol/config.py
```

2. Restart the service to apply changes:
```bash
sudo systemctl restart xcom-protocol
```


## Usage

The service starts automatically after installation and on system boot. It will:
1. Connect to your Studer device via Xcom
2. Collect all available data
3. Publish it to MQTT
4. Update values continuously

You can monitor the service status and logs using the commands in the Service Management section above.

## Available Data

### AC Power
- Input/Output power
- Daily and total energy
- Frequency, voltage, current

### Battery
- Voltage, current, power
- State of charge, temperature
- Cycle phase, health status
- Charge/discharge statistics
- Historical data

### Solar (VarioTrack)
- Voltage, current, power
- Daily and total energy production
- Sun hours tracking
- Temperature monitoring

### VarioString
- Power, voltage, current
- Energy production
- Operating status
- Temperature monitoring


## Maintenance

The script is configured as a system service for automatic startup. Logs provide monitoring of operation and any potential errors are reported to Home Assistant.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

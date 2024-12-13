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
- A Studer device with Xcom-232i interface and USB port
- Python 3.x
- MQTT broker (like Mosquitto)
- Home Assistant
- Network connection for the Raspberry Pi

## Installation

1. Clone the repository:
```bash
git clone https://github.com/[your-repo]/xcom-protocol
cd xcom-protocol
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

## Configuration

1. Copy `homeassistant.yaml` to your Home Assistant configuration directory and add its contents to your configuration.

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

## Home Assistant Integration

All sensors are automatically configured with:
- Appropriate units of measurement
- Device classes
- Logical grouping
- Ready for dashboard creation

## Maintenance

The script can be configured as a system service for automatic startup. Logs provide monitoring of operation and any potential errors are reported to Home Assistant.

## Support

- Full documentation in this README
- Easy parameter addition through `parameters.py`
- Issues can be reported via GitHub

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Studer-Innotec for the Xcom protocol documentation
- Home Assistant community

## License

[Your License]

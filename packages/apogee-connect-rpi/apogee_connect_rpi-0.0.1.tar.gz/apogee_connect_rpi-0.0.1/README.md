# Apogee Connect for Raspberry Pi 

Apogee Connect for Raspberry Pi is a lightweight script intended for automating the data collection process with Apogee's bluetooth sensors. This CLI application will automatically connect to and collect data from an Apogee Bluetooth sensor and store the data in a csv file with various configurable options.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
   - [Prerequisite](#prerequisite)
   - [Installation](#installation-1)
   - [Update](#update)
   - [Uninstall](#uninstall)
- [Commands](#commands)
   - [collect](#collect)
   - [config](#config)
   - [list](#list)
   - [scan](#scan)
   - [stop](#stop)
   - [version](#version)
   - [help](#help)
- [Contact](#contact)

## Installation

### *Prerequisite*

In order to install Apogee Connect for Raspberry Pi, you will need pip (package installer for Python). If you installed Python from source or with an installer from python.org, pip should already be included. You can confirm pip is installed by running the command

	`pip --version`

If pip isn't already installed visit the following for instructions on pip installation:

[https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)

### *Installation*

Install the Apogee Connect for Raspberry Pi from the Python Package Index by running the following command in terminal:

	`pip install apogee-connect-rpi`

### *Update*

Whenever updates are available, the app can be updated simply by running the following command in terminal:

	`pip install apogee-connect-rpi --upgrade`

#### *Uninstall*

To uninstall, run the following command in terminal:

	`pip uninstall apogee-connect-rpi`


## Commands

Key:
`apogee command <required_arguments> [--optional_arguments (default: value)]`


### collect

*Usage*

Automatically collect data from an Apogee sensor and write the data to a csv file (For peace of mind, all this data is also logged in the sensors internal memory and the application will attempt to retrieve missed data if there is a temporary interruption in connection)

*Example*

`apogee collect E8:63:32:06:6D:7D  --interval 10 --start 1720647720 --end 1721250915 --file /usr/documents/greenhouse-data.csv`

*Documentation*

`apogee collect <MAC address> [--interval (default: 5)] [--duration (default: infinite)] [--file (default: ./data/MAC_address.csv)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| Mac Address| N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF |
| -i, --interval | 5 minutes | Collect data every set number of minutes (must be a positive integer) |
| -s, --start | Now | Start time for data collection using epoch time (Unix timestamp in seconds) |
| -e, --end | Never | End time for data collection using epoch time (Unix timestamp in seconds) |
| -f, --file | ./data/MAC_address.csv | File path to write data to csv file. Will create folders and files is they don’t exist. | 


### config

*Usage*

Change or view the default configuration of application.

*Example*

`apogee config --filepath /usr/documents/live-data --precision 4 --temp F --par-filtering True`

*Documentation*

`apogee config [--filepath (default: ./data/)] [--precision (default: 2)] [--temp (default: C)] [--par-filtering (default: False)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| (N/A)| (N/A) | If no optional arguments are provided, the current configuration will be displayed. |
| -f, --filepath | ./data/ | The default path to save collected data. Adjust to avoid needing to specify full filepath every time data collection is initiated. |
| --p, --precision | 2 | Maximum number of decimal places for live data. |
| -t, --temp | C | Change preferred temperature units. Enter “C” for Celsius and “F” for Fahrenheit (without quotations). |
| -pf, --par-filtering | False | Filter negative PAR (PPFD) values to compensate for sensor "noise" in low-light conditions. Enter "True" or "False" (without quotations). |

### list

*Usage*

List all the sensors currently collecting data.

*Example*

`apogee list`

*Documentation*

`apogee list`


### scan

*Usage*

Scan for nearby Apogee sensors

*Example*

`apogee scan --time 15`

*Documentation*

`apogee scan [--time (default: 10)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
|-t, --time | 5-20 | Number of seconds to scan for Apogee Bluetooth sensors. If not set, scanning will continue until no new sensors are being discovered or a maximum of 20 seconds. |


### stop

*Usage*

Stop data collection from an Apogee sensor

*Example*

`apogee stop E8:63:32:06:6D:7D  --interval 10 --number 6 --file /usr/documents/greenhouse-data.csv`

*Documentation*

`apogee stop <MAC address> [--after (default: now)]`

| Argument | Default Value | Usage |
| -------- | ------------- | ----- |
| MAC address | N/A (required) | MAC address of sensor in the format of AA:BB:CC:DD:EE:FF |
| -e, --end | Now | End time for data collection using epoch time (Unix timestamp in seconds) |


### version

*Usage*

Show current application version

*Example*

`apogee --version`

*Documentation*

`apogee --version`

`apogee -v`


### help

*Usage*

Show help menu for entire application or for specific command, depending on usage

*Example*

`apogee collect --help`

*Documentation*

Entering just `--help` (or `-h`) will show a high-level overview of available commands.
Entering a command followed by `--help` will show a menu with required and optional arguments.
Any unrecognized command will also print the high-level overview help menu.

## Contact

For more information or additional help, contact Apogee Instruments at: [techsupport@apogeeinstruments.com](mailto:techsupport@apogeeinstruments.com) or [+1(435)245-8012](tel:+14352458012)
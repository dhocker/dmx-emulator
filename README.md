# DMX Emulator for AtHomeDMX
Copyright © 2019 by Dave Hocker

## Overview
This app was designed to be a test tool for the AtHomeDMX DMX controller.
It basically provides a DMX interface that recognizes up to 512 channels.
It can be driven through AtHomeDMX scripts. The number of DMX channels defaults
to 512, but can be changed through a configuration file.

The **test_client.py** file serves as both a test of the emulator and a programming
example of how to use the emulator.

## Setup
The app requires Python 3 (>=3.6). The simplest setup is to create a
VENV using the requirements.txt file.

## Configuration
Both the server and the test client use the dmx_emulator.conf file for
configuration. This file is JSON formatted and looks like this:

    {
        "num_channels": 512,
        "host": "localhost",
        "port": 5555,
        "polling_interval": 30,
        "log_console": "true",
        "log_level": "debug",
        "log_file": "dmx-emulator.log"
    }

| Key | Value | Description |
|-----|-------|-------------|
| num_channels | int | 1-512. The maximum number of DMX channels in a frame. |
| host | string | Test client only. DMX emulator host name. |
| port | int | TCP port number used by DMX emulator. |
| polling_interval | int | DMX emulator polling time in milliseconds. |
| log_console | bool | DMX emulator only. Routes logging to console. |
| log_level | string | DMX emulator only. debug, warn, error or info. |
| log_file | string | DMX emulator only. Full path to log file. |

## Quick Test
Open a terminal window and activate the VENV. Start the emulator.

    python dmx-emulator.py

You should see the emulator UI window.

Open a second terminal window and run the test client.

    python3 test_client.py

The emulator window should show changing DMX chanenel values as the emulator is
driven by the test client.

## API
The app acts as a server. A client connects to the server (default port 5555)
and sends it DMX data frames. Each DMX data frame contains up to 512 channels.

### DMX Data Frame
A DMX data frame contains the following.

    Number of channels (4 bytes)
    Channel data bytes (1-512 bytes)

Where:

Number of channels = 4 bytes as a packed integer.

Channel data bytes = up to 512 bytes for channels 1-512.

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

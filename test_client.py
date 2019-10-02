#
# test client - for testing LED Emulator
# Copyright © 2019  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

import socket
import time
from configuration import Configuration
from dmx_emulator_client import DMXEmulatorClient

def main():
    """
    Main program for test client. This client connects to the LED Emulator
    and sends it a number of LED data frames.
    :return: Nothing
    """
    num_channels = Configuration.num_channels()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Opening DMXClientEmulator", Configuration.host(), Configuration.port())
        sock = DMXEmulatorClient(Configuration.num_channels(), host=Configuration.host(), port=Configuration.port())
        sock.open()

        print("Sending frames...")
        for i in range(64):
            frame = bytes([(n + i) % 256 for n in range(num_channels)])
            sock.send(frame)
            print("Frame {0} sent".format(i + 1))
            time.sleep(0.500)
    except Exception as ex:
        print(str(ex))
    finally:
        sock.close()

#
# Run as an application
#
if __name__ == "__main__":
    Configuration.load_configuration()
    main()

#
# Server socket connection handler
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

import app_logger
from configuration import Configuration
from threading import Lock

logger = app_logger.getAppLogger()

class DMXConnectionHandler:
    """
    The socket server creates one instance of this class for each
    incoming connection. That instance handles DMX data sent by a network client.

    The protocol is simple. The client sends a stream of data as if the
    server is a DMX system.

    Each transmission is (4h + 4d + 512b + 4t) bytes in length where h is a 4-byte
    header of zeroes, d is a 4-byte data length and t is a 4-byte trailer of 0xFF.
    The data length indicates how many bytes of the 512 byte body are valid. It's
    range is 1 to 512. Note that the body is ALWAYS 512 bytes.
    """

    frame_list = []
    frame_lock = Lock()

    def __init__(self):
        """
        Constructor for an instance. A DMX data frame looks like this.
        Header = 4 bytes of 0x00
        Effective Data Length = 4 bytes
        Body = 512 bytes (always this size)
        Trailer = 4 bytes of 0xFF
        """

    def execute_command(self, port, dmx_data):
        """
        Execute a client command/request.
        :param port: The port number receiving the request. It can be used
        to qualify or discriminate the request. The idea is to be able to
        map a port number to a device.
        :param dmx_data: The DMX data sent by the client as a list of bytes
        :return: None
        """
        # print("Frame received:", len(dmx_data))
        # Let's reformat the frame into something that the DMX window can readily use
        DMXConnectionHandler.frame_lock.acquire()

        DMXConnectionHandler.frame_list.append(dmx_data)

        DMXConnectionHandler.frame_lock.release()

        return None

    @classmethod
    def get_frame(cls):
        """
        Gets the next available DMX data frame. The frame is a list of bytes.
        :return: Returns the frame or None
        """
        frame = None

        DMXConnectionHandler.frame_lock.acquire()

        if len(cls.frame_list):
            frame = cls.frame_list.pop()

        DMXConnectionHandler.frame_lock.release()

        return frame

# coding: utf-8
#
# AtHomeSocketServer
# Copyright © 2016, 2019  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#


import sys
try:
    import socketserver as socketserver
except ImportError:
    import SocketServer as socketserver
from struct import unpack


class TCPRequestHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    call_sequence = 1

    # The command_handler_class is injected by the user of this class
    # See dmx_client.py for an example implementation.
    command_handler_class = None

    # Default size of a complete LED data frame for 50 pixels
    max_frame_size = 512

    @classmethod
    def set_max_frame_size(cls, frame_size):
        """
        Complete LED data frame size injection
        :param frame_size:
        :return:
        """
        cls.max_frame_size = frame_size

    @classmethod
    def set_command_handler_class(cls, command_handler_to_use, connection_time_out=-1):
        """
        Command handler injection
        :param command_handler_to_use: A class that implements a
        Response class and an execute_command method.
        :param connection_time_out:
        :return:
        """
        cls.command_handler_class = command_handler_to_use
        cls.connection_time_out = connection_time_out

    """
    This handler uses raw data from the SocketServer.TCPServer class.
    """

    def handle(self):
        print("Connection from {0}".format(self.client_address[0]))

        # Do until close is received
        connection_open = True
        while connection_open:
            # self.request is the TCP socket connected to the client
            dmx_data = self.read_dmx_data()

            if dmx_data and len(dmx_data) > 0:
                try:
                    # The command handler generates the response
                    if TCPRequestHandler.command_handler_class:
                        # Create an instance of the command handler
                        handler = TCPRequestHandler.command_handler_class()
                        # Pass the command string to the command handler
                        response = handler.execute_command(self.request.getsockname()[1], dmx_data)
                except Exception as ex:
                    print("Exception occurred while handling LED data")
                    print(str(ex))
                    print(dmx_data)
                finally:
                    pass

                TCPRequestHandler.call_sequence += 1
            else:
                # We consider this an error, so we force close the socket
                connection_open = False
        print("Connection closed")

    def read_dmx_data(self):
        """
        Read a stream of LED data from a socket
        :return: Returns a list of bytes or None
        """
        # This is essentially APA102 format.
        # client_frame_size followed by
        # 4 bytes all zeroes header + 4 bytes per pixel * pixels + 4 bytes all ones trailer
        client_frame_size = self.receive(4)
        if not client_frame_size:
            return None
        # Note that the result of unpack is a tuple with one value
        client_frame_size = unpack('!i', client_frame_size)[0]
        if client_frame_size > TCPRequestHandler.max_frame_size:
            print("Client frame size is too large")
            return None

        dmx_data = self.receive(client_frame_size)
        if not dmx_data:
            print("Failed to receive complete frame")
            return None

        return dmx_data

    def receive(self, block_size):
        """
        Read a given number of bytes from stream
        :param block_size:
        :return: Received block as a list of bytes
        """
        count = block_size
        dmx_data = b''
        # Read exactly "count" bytes
        while count:
            seg = self.request.recv(count)
            if seg:
                dmx_data += seg
                count -= len(seg)
            else:
                # Broken socket
                return None
        # It is likely that some sort of data conversion will be required.
        # For now we'll coerce the frame into a list of bytes (which
        # should be the format it is already in)
        dmx_data = bytes(dmx_data)
        return dmx_data

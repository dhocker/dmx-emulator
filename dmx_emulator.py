#
# DMX Emulator - for testing AtHomeDMX
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

import logging
import signal
import os
import sys
from dmxsocketserver import SocketServerThread
# import configuration
import app_logger
# import app_trace # in athomeutils package
import disclaimer.disclaimer
from configuration import Configuration
from dmx_connection_handler import DMXConnectionHandler
from dmx_window import run_dmx_window

terminate_service = False

#
# main
#
def main():
    global terminate_service

    logger = logging.getLogger("dmx")

    # Clean up when killed
    def term_handler(signum, frame):
        global terminate_service
        logger.info("DMXEmulator received kill signal...shutting down")
        # This will break the forever loop at the foot of main()
        terminate_service = True
        sys.exit(0)

    # Orderly clean up of the LED emulator
    def CleanUp():
        logger.info("DMXEmulator shutdown complete")
        logger.info("################################################################################")
        app_logger.Shutdown()

    # Change the current directory so we can find the configuration file.
    # For Linux we should probably put the configuration file in the /etc directory.
    just_the_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(just_the_path)

    # Load the configuration file
    Configuration.load_configuration()

    # Activate logging to console or file
    # Logging.EnableLogging()
    app_logger.EnableEngineLogging()

    # Per GPL, show the disclaimer
    disclaimer.disclaimer.DisplayDisclaimer()
    print("Use ctrl-c to shutdown emulator\n")

    logger.info("################################################################################")

    # For additional coverage, log the disclaimer
    disclaimer.disclaimer.LogDisclaimer()

    logger.info("Python version: %s", str(sys.version))
    print("Python version:", str(sys.version))

    logger.info("Starting up...")

    # logger.info("Using configuration file: %s", configuration.Configuration.GetConfigurationFilePath())
    Configuration.dump_configuration()

    # Set up handler for the kill signal
    signal.signal(signal.SIGTERM, term_handler)  # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C or kill the daemon.

    # This accepts connections from any network interface. It was the only
    # way to get it to work in the RPi from remote machines.
    HOST, PORT = "0.0.0.0", Configuration.cfg_port

    # Create the TCP socket server on its own thread.
    # This is done so that we can handle the kill signal which
    # arrives on the main thread. If we didn't put the TCP server
    # on its own thread we would not be able to shut it down in
    # an orderly fashion.
    server = SocketServerThread.SocketServerThread(HOST, PORT,
                                                   DMXConnectionHandler,
                                                   connection_time_out=-1,
                                                   frame_size=512)

    # Launch the socket server
    try:
        # This runs "forever", until ctrl-c or killed
        server.Start()

        terminate_service = False
        run_dmx_window(Configuration.num_channels(), Configuration.polling_interval())
    except KeyboardInterrupt:
        logger.info("DMXEmulator shutting down...")
    except Exception as e:
        logger.error("Unhandled exception occurred")
        logger.error(e)
        logger.error(sys.exc_info()[0])
        # app_trace.log_trace(logger, ex=e)
    finally:
        # We actually get here through ctrl-c or process kill (SIGTERM)
        server.Stop()
        CleanUp()
    print("Exiting main()")


#
# Run as an application
#
if __name__ == "__main__":
    main()

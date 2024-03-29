#
# Configuration
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Server configuration
#
# The at_home_dmx.conf file holds the configuration data in JSON format.
# Currently, it looks like this:
#
# {
# }
#
# The JSON parser is quite finicky about strings being quoted as shown above.
#
# This class behaves like a singleton class. There is only one instance of the configuration.
# There is no need to create an instance of this class, as everything about it is static.
#

import os
import json
import logging

logger = logging.getLogger("dmx")


########################################################################
class Configuration():
    cfg_host = "localhost"
    cfg_port = 5555
    cfg_num_channels = 512
    cfg_polling_interval = 30
    cfg_log_console = True
    cfg_log_file = ""
    cfg_log_level = "debug"

    ######################################################################
    def __init__(self):
        Configuration.load_configuration()

    ######################################################################
    # Load the configuration file
    @classmethod
    def load_configuration(cls):
        # Try to open the conf file. If there isn't one, we give up.
        try:
            cfg_path = Configuration.get_configuration_file_path()
            print("Opening configuration file {0}".format(cfg_path))
            cfg = open(cfg_path, 'r')
        except Exception as ex:
            print("Unable to open {0}".format(cfg_path))
            print(str(ex))
            return

        # Read the entire contents of the conf file
        cfg_json = cfg.read()
        cfg.close()
        # print cfg_json

        # Try to parse the conf file into a Python structure
        try:
            config = json.loads(cfg_json)
        except Exception as ex:
            print("Unable load configuration file as JSON")
            print(str(ex))
            return

        try:
            # Parse out config values
            if "host" in config:
                cls.cfg_host = config["host"]
            if "port" in config:
                cls.cfg_port = int(config["port"])
            if "num_channels" in config:
                cls.cfg_num_channels = int(config["num_channels"])
            if "polling_interval" in config:
                cls.cfg_polling_interval = int(config["polling_interval"])
            if "log_level" in config:
                cls.cfg_log_level = config["log_level"].lower()
            if "log_console" in config:
                cls.cfg_log_console = config["log_console"].lower() == "true"
            if "log_file" in config:
                cls.cfg_log_file = config["log_file"]
        except Exception as ex:
            print("Unable to parse configuration file as JSON")
            print(str(ex))
            return

        return

    @classmethod
    def dump_configuration(cls):
        logger.info("Active configuration")
        logger.info("host: %s", cls.cfg_host)
        logger.info("port: %d", cls.cfg_port)
        logger.info("num_channels: %d", cls.cfg_num_channels)
        logger.info("polling_interval: %d", cls.cfg_polling_interval)
        logger.info("log_console: %s", str(cls.cfg_log_console))
        logger.info("log_file: %s", cls.cfg_log_file)
        logger.info("log_level: %s", cls.cfg_log_level)

    ######################################################################
    @classmethod
    def is_linux(cls):
        """
        Returns True if the OS is of Linux type (Debian, Ubuntu, etc.)
        """
        return os.name == "posix"

    ######################################################################
    @classmethod
    def is_windows(cls):
        """
        Returns True if the OS is a Windows type (Windows 7, etc.)
        """
        return os.name == "nt"

    ######################################################################
    @classmethod
    def host(cls):
        return cls.cfg_host

    ######################################################################
    @classmethod
    def port(cls):
        return cls.cfg_port

    ######################################################################
    @classmethod
    def num_channels(cls):
        return cls.cfg_num_channels

    ######################################################################
    @classmethod
    def polling_interval(cls):
        return cls.cfg_polling_interval

    ######################################################################
    @classmethod
    def log_console(cls):
        return cls.cfg_log_console

    ######################################################################
    @classmethod
    def log_file(cls):
        return cls.cfg_log_file

    ######################################################################
    @classmethod
    def log_level(cls):
        return cls.cfg_log_level

    ######################################################################
    @classmethod
    def get_configuration_file_path(cls):
        """
        Returns the full path to the configuration file
        """
        file_name = 'dmx_emulator.conf'
        return file_name

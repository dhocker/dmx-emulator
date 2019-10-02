#
# LEDEmulator app logger
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import logging
import logging.handlers
from configuration import Configuration


########################################################################
# Enable logging for the AtHomeDMX application
def EnableEngineLogging():
    # Default overrides
    logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
    logdateformat = '%Y-%m-%d %H:%M:%S'

    # Logging level override
    log_level_override = Configuration.cfg_log_level
    if log_level_override == "debug":
        loglevel = logging.DEBUG
    elif log_level_override == "info":
        loglevel = logging.INFO
    elif log_level_override == "warn":
        loglevel = logging.WARNING
    elif log_level_override == "error":
        loglevel = logging.ERROR
    else:
        loglevel = logging.DEBUG

    logger = logging.getLogger("dmx")
    logger.setLevel(loglevel)

    formatter = logging.Formatter(logformat, datefmt=logdateformat)

    # Do we log to console?
    if Configuration.log_console():
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Do we log to a file?
    logfile = Configuration.log_file()
    if logfile != "":
        # To file
        fh = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', backupCount=3)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # After defining logs, record what was defined
    if Configuration.log_console():
        logger.debug("Logging to console")
    if logfile:
        logger.debug("Logging to file: %s", logfile)

def getAppLogger():
    """
    Return an instance of the default logger for this app.
    :return: logger instance
    """
    return logging.getLogger("dmx")

# Controlled logging shutdown
def Shutdown():
    logging.shutdown()
    print("Logging shutdown")

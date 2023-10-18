###################################################################
# #   IMPORTS
###################################################################
import inspect
import os
import datetime
import logging

###################################################################
#   GLOBAL VARIABLES
###################################################################

# Indicates whether global debugging is enabled or not.
GLOBAL_DEBUG = False

# Indicates whether global logging is enabled or not.
GLOBAL_LOG = False

# The name of the global log file.
GLOBAL_LOG_FILE = "log.txt"

###################################################################
#   CLASS
###################################################################
class prettyDebug:
    """
    A debugging utility class that provides methods for printing debug messages, logging to a file and raising exceptions with debug info.
    """
    def __init__(self,name="None"):
        """
        Initializes a new instance of the prettyDebug class.
        
        :param name: The name to associate with this instance.
        """
        self.LOCAL_DEBUG = False
        self.LOCAL_LOG = False
        self.NAME = name
    
    def getDebugInfo(self):
        """
        Returns a string containing information about the current function call, including the filename, line number,
        calling class, and instance name (if specified).
        
        :return: A string containing debug information.
        """
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        filename = inspect.getframeinfo(inspect.currentframe().f_back.f_back).filename
        line_no = inspect.getframeinfo(inspect.currentframe().f_back.f_back).lineno
        calling_class = inspect.stack()[2][0].f_locals.get('self', None).__class__.__name__
        return f"{now} | {os.path.basename(filename):<30} | Line:{line_no:<5} | Class:{calling_class:<15} | Name:{self.NAME:<30} -> "
    
    def print(self, message, raiseError=None):
        """
        Prints a debug message and logs it to a file if global or local logging is enabled. If an exception class
        is provided, raises an exception with the debug information and message.
        
        :param message: The message to print.
        :param raiseError: Optional. The exception class to raise, if any.
        """
        if GLOBAL_DEBUG or self.LOCAL_DEBUG:
            print(f"{self.getDebugInfo()}{message}")
        if GLOBAL_LOG  or self.LOCAL_LOG:
            logging.basicConfig(filename=GLOBAL_LOG_FILE, level=logging.DEBUG)
            logging.debug(f"{self.getDebugInfo()}{message}")
        if raiseError:
            raise raiseError(f"{self.getDebugInfo()}{message}")

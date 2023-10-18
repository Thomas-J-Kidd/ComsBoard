###################################################################
# #   IMPORTS
###################################################################
import time
from . import Debug

###################################################################
#   CLASS
###################################################################
class CircularBuffer:
    """
    A circular buffer implementation that allows for reading and writing of data.
    """
    def __init__(self, bufferSize, overflowTimeout=1, overflowSleep=0.1, name="None"):
        """
        Initializes the CircularBuffer instance.

        Args:
            bufferSize (int): The size of the buffer.
            overflowTimeout (float, optional): The timeout for writing to the buffer if it is full. Default is 1 secods.
            overflowSleep (float, optional): The sleep time between checking if the buffer is full. Default is 0.1 secods.
            name (str, optional): The name of the buffer. Default is "none".
        """
        # Setup debug
        self.name = name
        self.pd = Debug.prettyDebug(name=self.name)
        self.pd.LOCAL_DEBUG = False
        self.pd.LOCAL_LOG = False
        self.pd.print("INIT")
        
        # Init Class
        self.size = bufferSize
        self.overflowTimeout = overflowTimeout
        self.overflowSleep = overflowSleep
        self.clear()
        
    def clear(self):
        """
        Clears the buffer and sets the head, tail, and full flags.
        """
        self.pd.print("Clearing Buffer")
        self.buffer = [None] * self.size
        self.head = 0
        self.tail = 0
        self.full = False

    def is_empty(self):
        """
        Checks if the buffer is empty.

        Returns:
            bool: True if the buffer is empty, False otherwise.
        """
        return not self.full and self.head == self.tail

    def is_full(self):
        """
        Checks if the buffer is full.

        Returns:
            bool: True if the buffer is full, False otherwise.
        """
        return self.full

    def write(self, data):
        """
        Writes data to the buffer.

        Args:
            data: The data to write to the buffer.

        Returns:
            bool: True if the write was successful, False otherwise.
        """
        if self.is_full():
            start_time = time.time()
            while time.time() - start_time < self.overflowTimeout:
                if not self.is_full():
                    break
                time.sleep(self.overflowSleep)
            else:
                self.pd.print(f"Write overflow - Size:{self.size:<5} Full:{self.full:<5} Tail:{self.tail+1:<5} Head:{self.head+1:<5} Data:{data}")
                return False
        self.buffer[self.head] = data
        self.head = (self.head + 1) % self.size
        if self.head == self.tail:
            self.full = True
        return True

    def read(self):
        """
        Reads data from the buffer.

        Returns:
            The data read from the buffer or False if the buffer is empty.
        """
        if self.is_empty():
            self.pd.print(f"Read empty     - Size:{self.size:<5} Full:{self.full:<5} Tail:{self.tail+1:<5} Head:{self.head+1:<5}")
            return False
        data = self.buffer[self.tail]
        self.full = False
        self.tail = (self.tail + 1) % self.size
        return data

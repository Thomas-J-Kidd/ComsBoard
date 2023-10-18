###################################################################
# #   IMPORTS
###################################################################
import threading
import serial
import time
from queue import Queue
import re
from myLibs import Debug

###################################################################
#   CLASS
###################################################################
class SerialDevice:
    """
    A class representing a serial device that handles communication over a serial port.

    Attributes:
        port (str): The serial port to which the device is connected.
        receive_callback (callable): The callback function to be executed upon receiving data.
        baudrate (int): The baud rate of the serial communication.
        timeout (float): The timeout for reading data from the serial port.
        loopSleep (float): The sleep time between loop iterations in the send and receive threads.
        name (str): The name of the serial device.
    """
    def __init__(self, callback, port, baudrate=115200, timeout=0.1, loopSleep=0.1, name="None"):
        """
        Initializes the SerialDevice object with the given parameters.

        Args:
            callback (callable): The callback function to be executed upon receiving data.
            port (str): The serial port to which the device is connected.
            baudrate (int, optional): The baud rate of the serial communication. Defaults to 115200.
            timeout (float, optional): The timeout for reading data from the serial port. Defaults to 0.1.
            loopSleep (float, optional): The sleep time between loop iterations in the send and receive threads. Defaults to 0.1.
            name (str, optional): The name of the serial device. Defaults to "None".
        """
        # Setup debug
        self.name = name
        self.pd = Debug.prettyDebug(name=self.name)
        self.pd.LOCAL_DEBUG = True 
        self.pd.LOCAL_LOG = False
        self.pd.print("INIT")
        
        self.port = port
        self.receive_callback = callback
        self.baudrate = baudrate
        self.timeout = timeout
        self.loopSleep = loopSleep
        self.serial = None
        self.receiveThread = None
        self.sendQueue = Queue()
        self.sendThread = None
        self.serialLock = threading.RLock()
        self.runThreads = False
        self.pauseThreads = False
        
        if not bool(re.search(r'/dev/[a-zA-Z]+', port) or (re.search(r'COM\d+', port))):
            self.pd.print("Serial init: Invalid COM")
            #self._class_print(f"Serial init: Invalid COM")
        
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            if self.serial.is_open:
                self.pd.print(f"Serial init: Serial port opened")
            else:
                self.pd.print("Serial init: Serial port fail to open")
                return None
        except Exception as e:
            self.pd.print(f"Serial init: Exception {e}",e)
            return None

    def _class_print(self, message):
        self.pd.print(message)

    def open(self):
        """
        Opens the serial port and starts the send and receive threads.
        """
        self.runThreads = True
        self.receiveThread = threading.Thread(target=self.receiveLoopThread, daemon=True)
        self.receiveThread.start()
        time.sleep(self.timeout)
        self.sendThread = threading.Thread(target=self.sendLoopThread, daemon=True)
        self.sendThread.start()
        time.sleep(self.timeout)
        
    def close(self):
        """
        Closes the serial port and stops the send and receive threads.
        """
        self.runThreads = False
        self.receiveThread.join()
        self.sendThread.join()        
        try:
            self.serial.close()
        except Exception as e: 
            self.pd.print(f"Serial close: Exception {e}")
        self.pd.print(f"Serial close: Serial port closed")
        
    def send(self, data):
        """
        Sends data to the serial device.

        Args:
            data (bytes): The data to be sent.

        Returns:
            int: The number of bytes written.
        """
        with self.serialLock:
            try:
                result = self.serial.write(data)
                if result:
                    self.pd.print(f"Serial send: {data}")
                else:
                    self.pd.print(f"Serial send: ERROR {data}")
            except Exception as e:
                self.pd.print(f"Serial send: Exexption - {e}")
        return result
        
    def receive(self):
        """
        Receives data from the serial device.

        Returns:
            bytes: The received data.
        """
        with self.serialLock:
            try:
                result = self.serial.readline()
                if result:
                    self.pd.print(f"Serial receive: {result}")
            except Exception as e:
                self.pd.print(f"Serial receive: Exexption - {e}")
        return result
        
    def sendAndReceive(self, data, timeout=0.1):
        """
        Sends data to the serial device and waits for a response.

        Args:
            data (bytes): The data to be sent.
            timeout (float, optional): The timeout for waiting for a response. Defaults to 0.1.

        Returns:
            bytes: The received response.
        """
        try:
            with self.serialLock: 
                if self.send(data):
                    time.sleep(timeout)
                    result = self.receive()
                    if not result:
                        self.pd.print(f"Serial sendAndReceive: TIMED OUT {result}")
        except Exception as e:
            self.pd.print(f"Serial sendAndReceive: Exexption - {e}")
        return result
            
    def sendAndValidate(self, data, validation, timeout=0.1):
        """
        Sends data to the serial device and validates the received response.

        Args:
            data (bytes): The data to be sent.
            validation (bytes): The expected response.
            timeout (float, optional): The timeout for waiting for a response. Defaults to 0.1.

        Returns:
            bool: True if the received response matches the expected response, False otherwise.
        """
        try:
            with self.serialLock: 
                if self.send(data):
                    time.sleep(timeout)
                    result = self.receive()
                    if result == validation:
                        return True
                    else:
                        self.pd.print(f"Serial sendAndValidate: ERROR {result}")
        except Exception as e:
            self.pd.print(f"Serial sendAndValidate: Exexption - {e}")
        return False

    def sendToSendLoop(self, data):
        """
        Adds data to the send queue to be sent by the send thread.

        Args:
            data (bytes): The data to be sent.
        """
        self.sendQueue.put(data)
            
    def stopThreads(self):
        """
        Pauses the send and receive threads.
        """
        self.pauseThreads = True
        
    def resumeThreads(self):
        """
        Resumes the send and receive threads.
        """
        self.pauseThreads = False

    def receiveLoopThread(self):
        """
        The receive loop thread function. Continuously receives data from the serial device and executes the callback function.
        """
        self.pd.print("Serial receiveLoopThread: Start")
        while self.runThreads:
            if not self.pauseThreads:
                try:
                    with self.serialLock:
                        data = self.receive()
                    if data and self.receive_callback:
                        self.receive_callback(data)
                except Exception as e:
                        self.pd.print(f"Serial receiveLoopThread: Exexption - {e}")
                        break
            time.sleep(self.loopSleep)
        self.pd.print(f"Serial receiveLoopThread: Exit")

    def sendLoopThread(self):
        """
        The send loop thread function. Continuously sends data from the send queue to the serial device.
        """
        self.pd.print("Serial sendLoopThread: Start")
        while self.runThreads:
            if not self.pauseThreads:
                if not self.sendQueue.empty():
                    try:
                        with self.serialLock:
                            data = self.sendQueue.get()
                            self.send(data)
                    except Exception as e:
                        self.pd.print(f"Serial sendLoopThread: Exexption - {e}")
                        break
            time.sleep(self.loopSleep)
        self.pd.print(f"Serial sendLoopThread: Exit")

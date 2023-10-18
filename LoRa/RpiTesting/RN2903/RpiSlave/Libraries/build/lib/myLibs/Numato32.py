"""
NumatoGPIO - A Python library for controlling Numato Lab GPIO and Analog Input/Output devices over serial.
Author: Carlos Finocchiaro
Date: 4/30/2023
License: MIT
Description: This library provides functions for controlling Numato Lab GPIO and Analog Input/Output devices over serial. 
It supports setting the direction and reading/writing values to individual GPIO pins, as well as reading values from analog input channels.
Usage:
    1. Instantiate the NumatoGPIO class with the serial port and optional baudrate and timeout:
    gpio = NumatoGPIO('COM18', baudrate=115200, timeout=1, debug=True)
    
    2. Set the direction of a GPIO pin to input ("in") or output ("out"):
    gpio.setGpioDirection(1, 'out')
    
    3. Write a value of 0 or 1 to a GPIO pin:
    gpio.writeGpio(1, 1)
    
    4. Read the value of a GPIO pin:
    gpio.readGpio(1)
    
    5. Read the value of an analog input channel:
    gpio.readAnalog(1)
    
Note: This library requires the PySerial package to be installed. You can install it with pip: `pip install pyserial`.
"""

import serial
import time
import re

###################################################################
#   CLASS NUMATOGPIO
###################################################################
class NumatoGPIO:
    """
    A class for controlling Numato Lab GPIO and Analog Input/Output devices over serial.
        Args:
            port (str): The name or number of the serial port to use.
            baudrate (int, optional): The baudrate of the serial connection. Defaults to 115200.
            timeout (float, optional): The timeout of the serial connection in seconds. Defaults to 1.
            debug (bool, optional): Whether to print debug messages. Defaults to False.
        Attributes:
            ser (serial.Serial): The serial connection object.
            debug (bool): Whether to print debug messages.
        Methods:
            __init__(self, port, baudrate=115200, timeout=1, debug=False): Initializes the NumatoGPIO object and opens the serial port.
            __del__(self): Closes the serial port.
            _class_print(self, message, raiseError=False): Prints a debug message or raises a ValueError if raiseError is True.
            _sendCommand(self, command): Sends a command to the Numato device and returns the response.
            _validateGpio(self, gpio): Validates a GPIO number and returns True if it is valid, False otherwise.
            _convertGPIO(self, gpio): Converts a GPIO number to a string or character.
            _calculateMask(self, gpio): Calculates the binary mask for a GPIO number.
            _calculateDirectionMaks(self, gpio, direction): Calculates the binary mask for a GPIO direction.
            setGpioDirection(self, gpio, direction): Sets the direction of a GPIO pin to input ("in") or output ("out").
            writeGpio(self, gpio, value): Writes a value of 0 or 1 to a GPIO pin.
            readGpio(self, gpio): Reads the value of a GPIO pin.
            _validateAnalog(self, channel): Validates an analog input channel and returns True if it is valid, False otherwise.
            readAnalog(self, channel): Reads the value of an analog input channel.
    """
    #------------------------------------------------------------------
    #   CLASS VARIABLES
    #------------------------------------------------------------------
    _GPIO_MAX_NUMERIC = 10
    _GPIO_MIN = 0
    _GPIO_MAX = 31
    _ADC_MIN = 1
    _ADC_MAX = 7
    
    #------------------------------------------------------------------
    #   INIT FUNCTIONS
    #------------------------------------------------------------------
    def __init__(self, port, baudrate=115200, timeout=1, debug=False):
        """
        Initializes a NumatoGPIO object and opens the serial port.
            Args:
                port (str): The name or number of the serial port to use.
                
                baudrate (int, optional): The baudrate of the serial connection, Defaults to 115200.
                
                timeout (float, optional): The timeout of the serial connection in seconds, Defaults to 1.
                
                debug (bool, optional): Whether to print debug messages, Defaults to False.
            Raises:
                ValueError: If the port number is invalid or the serial connection fails to open.
            Returns:
                None
        """
        self.debug = debug
        self._class_print("Class Init")
        
        if not bool(re.search(r'COM\d+', port)):
            self._class_print(f"Serial: Invalid COM",raiseError=True)
            
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            if self.ser.is_open:
                self._class_print("Serial: Opened")
            else:
                self._class_print("Serial: Fail to open",raiseError=True)
        except Exception as e:
            self._class_print(f"Serial: {e}",raiseError=True)    
        self._class_print(f"Serial: Port {port}, Baudrate {baudrate}, Timeout: {timeout}")
        
    def __del__(self):
        """
        Destructs the object and performs any necessary cleanup before the object is deleted.
        This method is called by Python's garbage collector when there are no more references to the object.
        The purpose of this method is to release any resources held by the object, such as file handles or network connections.
        Note that it is not guaranteed that this method will be called, so it should not be relied upon to release
        critical resources. Instead, it's generally a good idea to use context managers or other techniques to manage
        resource cleanup explicitly.
            Returns:
                None
        """
        try:
            self.ser.close()
            self._class_print("Serial: Closed")
        except Exception as e:
            self._class_print(f"Serial: {e}",raiseError=True)
    
    #------------------------------------------------------------------
    #   DEBUG FUNCTIONS
    #------------------------------------------------------------------
    def _class_print(self, message, raiseError=False):
        """
        Prints a message with the name of the class as a prefix, if debug mode is enabled.
            Args:
                message (str): The message to print.
                raiseError (bool): If True, raises a ValueError instead of printing the message.
            Raises:
                ValueError: If raiseError is True.
        """
        if self.debug and not raiseError:
            print(f"{self.__class__.__name__}-> {message}")
        elif raiseError:
            raise ValueError(f"{self.__class__.__name__}-> {message}")

    #------------------------------------------------------------------
    #   SERIAL FUNCTIONS
    #------------------------------------------------------------------
    def _sendCommand(self, command):
        """
        Sends a command to the device and waits for a response.
            Args:
                command (str): The command to send to the device.
            Returns:
                bool or str: If the response from the device contains a ">", returns True, indicating the command was successful.
                            Otherwise, returns the response string.
        """
        self._class_print(f"TX-> {command}")  
        self.ser.write((command + '\r').encode())
        time.sleep(0.1)
        response = self.ser.read(self.ser.inWaiting()).decode().split("\r")[1].strip("\n")
        if response.find(">") != -1:
            return True
        else:
            self._class_print(f"RX<- {response}")
            return response
    
    #------------------------------------------------------------------
    #   GPIO FUNCTIONS
    #------------------------------------------------------------------
    def _validateGpio(self, gpio):
        """
        Validates the GPIO pin number provided by the user. Returns True if the GPIO pin number is valid, False otherwise.
            Args:
                gpio (int or str): The GPIO pin number to be validated.
            Returns:
                bool: True if the GPIO pin number is valid, False otherwise.
        """
        gpio = str(gpio)
        if not re.match(r'^\d+$', gpio):
            self._class_print(f"GPIO: Invalid gpio {gpio}")
            return False
        gpio = int(gpio)
        if gpio < self._GPIO_MIN or gpio > self._GPIO_MAX:
            self._class_print(f"GPIO: gpio out of range ({self._GPIO_MIN}-{self._GPIO_MAX}): {gpio}")
            return False
        return True
    
    def _convertGPIO(self, gpio):
        """
        Converts the specified GPIO to its corresponding string representation.
        the Numato board accepts GPIO number from 0-9, and A-V (10-31), total 32 values.
            Args:
                gpio (int): The GPIO to convert.
            Returns:
                str: The string representation of the GPIO.
        """
        return str(gpio) if gpio < self._GPIO_MAX_NUMERIC else chr(55 + gpio)
    
    def _calculateMask(self, gpio):
        """
        Calculate a hex mask for a given GPIO pin
            Args:
                gpio (int): The GPIO pin for which to calculate the mask. padded with zeroes to a length of 8 characters.
            Returns:
                str: The hexadecimal mask for the given GPIO pin.
        """
        binaryMask = '0' * (31 - gpio) + '1' + '0' * gpio
        return hex(int(binaryMask, 2))[2:].zfill(8)
    
    def _calculateDirectionMaks(self, gpio, direction):
        """
        Calculate the direction mask for a specific GPIO pin.
            Args:
                gpio (int): The GPIO pin number.
                direction (int): The direction to set. 1 for output and 0 for input.
            Returns:
                str: A string representing the direction mask in hexadecimal format, padded with zeroes to a length of 8 characters.
        """
        binaryMask = '0' * (31 - gpio) + str(direction) + '0' * gpio
        return hex(int(binaryMask, 2))[2:].zfill(8)
        
    def setGpioDirection(self, gpio, direction):
        """
        Sets the direction of the specified GPIO pin.
            Args:
                gpio (int): The GPIO pin number.
                
                direction (str): The direction to set the GPIO pin to. Must be "in" or "out".
            Returns:
                bool: Returns True if the GPIO direction was set successfully. Returns False if the GPIO pin number is invalid.
            Example:
                To set GPIO 0 to output, call setGpioDirection(0, "out")
                To set GPIO 0 to input, call setGpioDirection(0, "in")
        """
        if self._validateGpio(gpio):
            mask = self._calculateMask(gpio)
            if direction == "in":
                directionMask = self._calculateDirectionMaks(gpio,1)
            elif direction == "out":
                directionMask = self._calculateDirectionMaks(gpio,0)
            else:
                self._class_print(f"GPIO Direction: Invalid direction. Must be 'in' or 'out'.")
            self._sendCommand(f'gpio iomask {mask}')
            self._sendCommand(f'gpio iodir {directionMask}')
            return True
        else:
            return False
    
    def writeGpio(self, gpio, value):
        """
        Sets the output value of a specified GPIO pin.
            Args:
                gpio (int): The GPIO pin number to write to.
                
                value (int): The value to write to the specified GPIO pin. Must be 0 or 1.
            Returns:
                bool: True if the write was successful, False otherwise.
            Example:
                To write a high to GPIO 0, call writeGpio(0,1)
                To write a low to GPIO 0, call writeGpio(0,0)
        """
        if self._validateGpio(gpio):
            if value == 1:
                return self._sendCommand(f'gpio set {self._convertGPIO(gpio)}')
            elif value == 0:
                return self._sendCommand(f'gpio clear {self._convertGPIO(gpio)}')
            else:
                self._class_print(f"GPIO: gpio value of range ({value})")
        else:
            return False

    def readGpio(self, gpio):
        """
        Reads the value of a GPIO pin.
            Args:
                gpio (int): The GPIO pin number to read.
            Returns:
                int: The value of the GPIO pin (1 or 0).
                Bool: False if an invalid GPIO pin is provided.
            Example:
                To read the value of GPIO 0, call readGpio(0)
        """
        if self._validateGpio(gpio):
            return int(self._sendCommand(f'gpio read {self._convertGPIO(gpio)}'))
        else:
            return False

    #------------------------------------------------------------------
    #   ANALOG FUNCTIONS
    #------------------------------------------------------------------
    def _validateAnalog(self, channel):
        """
        Validates an analog channel input and returns the channel number if valid.
            Args:
                channel (int or str): The channel number to validate.
            Returns:
                int: The channel number if it is a valid input.
                Bool: Returns False if the channel is invalid.
        """
        channel = str(channel)
        if not re.match(r'^\d+$', channel):
            self._class_print(f"Analog: Invalid channel {channel}")
            return False
        channel = int(channel)
        if channel < self._ADC_MIN or channel > self._ADC_MAX:
            self._class_print(f"Analog: channel out of range ({self._ADC_MIN}-{self._ADC_MAX}): {channel}")
            return False
        return channel

    def readAnalog(self, channel):
        """
        Reads the analog value of the given channel.
            Args:
                channel (int): The analog channel to read. Must be an integer between 1 and 7.
            Returns:
                int: The analog value read from the channel. 
                Bool: Returns False if the channel is invalid.
            Example:
                To read the value of AN1 (GPIO1), call readAnalog(1)
        """
        channel = self._validateAnalog(channel)
        if channel is not False:
            return int(self._sendCommand(f'adc read {channel}'))
        else:
            return False
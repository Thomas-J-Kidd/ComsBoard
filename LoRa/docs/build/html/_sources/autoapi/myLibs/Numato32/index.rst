:py:mod:`myLibs.Numato32`
=========================

.. py:module:: myLibs.Numato32

.. autoapi-nested-parse::

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



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.Numato32.NumatoGPIO




.. py:class:: NumatoGPIO(port, baudrate=115200, timeout=1, debug=False)


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

   .. py:attribute:: _GPIO_MAX_NUMERIC
      :value: 10

      

   .. py:attribute:: _GPIO_MIN
      :value: 0

      

   .. py:attribute:: _GPIO_MAX
      :value: 31

      

   .. py:attribute:: _ADC_MIN
      :value: 1

      

   .. py:attribute:: _ADC_MAX
      :value: 7

      

   .. py:method:: __del__()

      Destructs the object and performs any necessary cleanup before the object is deleted.
      This method is called by Python's garbage collector when there are no more references to the object.
      The purpose of this method is to release any resources held by the object, such as file handles or network connections.
      Note that it is not guaranteed that this method will be called, so it should not be relied upon to release
      critical resources. Instead, it's generally a good idea to use context managers or other techniques to manage
      resource cleanup explicitly.
          Returns:
              None


   .. py:method:: _class_print(message, raiseError=False)

      Prints a message with the name of the class as a prefix, if debug mode is enabled.
          Args:
              message (str): The message to print.
              raiseError (bool): If True, raises a ValueError instead of printing the message.
          Raises:
              ValueError: If raiseError is True.


   .. py:method:: _sendCommand(command)

      Sends a command to the device and waits for a response.
          Args:
              command (str): The command to send to the device.
          Returns:
              bool or str: If the response from the device contains a ">", returns True, indicating the command was successful.
                          Otherwise, returns the response string.


   .. py:method:: _validateGpio(gpio)

      Validates the GPIO pin number provided by the user. Returns True if the GPIO pin number is valid, False otherwise.
          Args:
              gpio (int or str): The GPIO pin number to be validated.
          Returns:
              bool: True if the GPIO pin number is valid, False otherwise.


   .. py:method:: _convertGPIO(gpio)

      Converts the specified GPIO to its corresponding string representation.
      the Numato board accepts GPIO number from 0-9, and A-V (10-31), total 32 values.
          Args:
              gpio (int): The GPIO to convert.
          Returns:
              str: The string representation of the GPIO.


   .. py:method:: _calculateMask(gpio)

      Calculate a hex mask for a given GPIO pin
          Args:
              gpio (int): The GPIO pin for which to calculate the mask. padded with zeroes to a length of 8 characters.
          Returns:
              str: The hexadecimal mask for the given GPIO pin.


   .. py:method:: _calculateDirectionMaks(gpio, direction)

      Calculate the direction mask for a specific GPIO pin.
          Args:
              gpio (int): The GPIO pin number.
              direction (int): The direction to set. 1 for output and 0 for input.
          Returns:
              str: A string representing the direction mask in hexadecimal format, padded with zeroes to a length of 8 characters.


   .. py:method:: setGpioDirection(gpio, direction)

      Sets the direction of the specified GPIO pin.
          Args:
              gpio (int): The GPIO pin number.
              
              direction (str): The direction to set the GPIO pin to. Must be "in" or "out".
          Returns:
              bool: Returns True if the GPIO direction was set successfully. Returns False if the GPIO pin number is invalid.
          Example:
              To set GPIO 0 to output, call setGpioDirection(0, "out")
              To set GPIO 0 to input, call setGpioDirection(0, "in")


   .. py:method:: writeGpio(gpio, value)

      Sets the output value of a specified GPIO pin.
          Args:
              gpio (int): The GPIO pin number to write to.
              
              value (int): The value to write to the specified GPIO pin. Must be 0 or 1.
          Returns:
              bool: True if the write was successful, False otherwise.
          Example:
              To write a high to GPIO 0, call writeGpio(0,1)
              To write a low to GPIO 0, call writeGpio(0,0)


   .. py:method:: readGpio(gpio)

      Reads the value of a GPIO pin.
          Args:
              gpio (int): The GPIO pin number to read.
          Returns:
              int: The value of the GPIO pin (1 or 0).
              Bool: False if an invalid GPIO pin is provided.
          Example:
              To read the value of GPIO 0, call readGpio(0)


   .. py:method:: _validateAnalog(channel)

      Validates an analog channel input and returns the channel number if valid.
          Args:
              channel (int or str): The channel number to validate.
          Returns:
              int: The channel number if it is a valid input.
              Bool: Returns False if the channel is invalid.


   .. py:method:: readAnalog(channel)

      Reads the analog value of the given channel.
          Args:
              channel (int): The analog channel to read. Must be an integer between 1 and 7.
          Returns:
              int: The analog value read from the channel. 
              Bool: Returns False if the channel is invalid.
          Example:
              To read the value of AN1 (GPIO1), call readAnalog(1)




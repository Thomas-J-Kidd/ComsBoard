:py:mod:`myLibs.Communications`
===============================

.. py:module:: myLibs.Communications


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.Communications.SerialDevice




.. py:class:: SerialDevice(callback, port, baudrate=115200, timeout=0.1, loopSleep=0.1, name='None')


   A class representing a serial device that handles communication over a serial port.

   Attributes:
       port (str): The serial port to which the device is connected.
       receive_callback (callable): The callback function to be executed upon receiving data.
       baudrate (int): The baud rate of the serial communication.
       timeout (float): The timeout for reading data from the serial port.
       loopSleep (float): The sleep time between loop iterations in the send and receive threads.
       name (str): The name of the serial device.

   .. py:method:: _class_print(message)


   .. py:method:: open()

      Opens the serial port and starts the send and receive threads.


   .. py:method:: close()

      Closes the serial port and stops the send and receive threads.


   .. py:method:: send(data)

      Sends data to the serial device.

      Args:
          data (bytes): The data to be sent.

      Returns:
          int: The number of bytes written.


   .. py:method:: receive()

      Receives data from the serial device.

      Returns:
          bytes: The received data.


   .. py:method:: sendAndReceive(data, timeout=0.1)

      Sends data to the serial device and waits for a response.

      Args:
          data (bytes): The data to be sent.
          timeout (float, optional): The timeout for waiting for a response. Defaults to 0.1.

      Returns:
          bytes: The received response.


   .. py:method:: sendAndValidate(data, validation, timeout=0.75)

      Sends data to the serial device and validates the received response.

      Args:
          data (bytes): The data to be sent.
          validation (bytes): The expected response.
          timeout (float, optional): The timeout for waiting for a response. Defaults to 0.1.

      Returns:
          bool: True if the received response matches the expected response, False otherwise.


   .. py:method:: sendToSendLoop(data)

      Adds data to the send queue to be sent by the send thread.

      Args:
          data (bytes): The data to be sent.


   .. py:method:: stopThreads()

      Pauses the send and receive threads.


   .. py:method:: resumeThreads()

      Resumes the send and receive threads.


   .. py:method:: receiveLoopThread()

      The receive loop thread function. Continuously receives data from the serial device and executes the callback function.


   .. py:method:: sendLoopThread()

      The send loop thread function. Continuously sends data from the send queue to the serial device.




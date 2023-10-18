:py:mod:`myLibs.Buffers`
========================

.. py:module:: myLibs.Buffers


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.Buffers.CircularBuffer




.. py:class:: CircularBuffer(bufferSize, overflowTimeout=1, overflowSleep=0.1, name='None')


   A circular buffer implementation that allows for reading and writing of data.

   .. py:method:: clear()

      Clears the buffer and sets the head, tail, and full flags.


   .. py:method:: is_empty()

      Checks if the buffer is empty.

      Returns:
          bool: True if the buffer is empty, False otherwise.


   .. py:method:: is_full()

      Checks if the buffer is full.

      Returns:
          bool: True if the buffer is full, False otherwise.


   .. py:method:: write(data)

      Writes data to the buffer.

      Args:
          data: The data to write to the buffer.

      Returns:
          bool: True if the write was successful, False otherwise.


   .. py:method:: read()

      Reads data from the buffer.

      Returns:
          The data read from the buffer or False if the buffer is empty.




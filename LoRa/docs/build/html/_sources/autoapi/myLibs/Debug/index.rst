:py:mod:`myLibs.Debug`
======================

.. py:module:: myLibs.Debug


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.Debug.prettyDebug




Attributes
~~~~~~~~~~

.. autoapisummary::

   myLibs.Debug.GLOBAL_DEBUG
   myLibs.Debug.GLOBAL_LOG
   myLibs.Debug.GLOBAL_LOG_FILE


.. py:data:: GLOBAL_DEBUG
   :value: False

   

.. py:data:: GLOBAL_LOG
   :value: False

   

.. py:data:: GLOBAL_LOG_FILE
   :value: 'log.txt'

   

.. py:class:: prettyDebug(name='None')


   A debugging utility class that provides methods for printing debug messages, logging to a file and raising exceptions with debug info.

   .. py:method:: getDebugInfo()

      Returns a string containing information about the current function call, including the filename, line number,
      calling class, and instance name (if specified).

      :return: A string containing debug information.


   .. py:method:: print(message, raiseError=None)

      Prints a debug message and logs it to a file if global or local logging is enabled. If an exception class
      is provided, raises an exception with the debug information and message.

      :param message: The message to print.
      :param raiseError: Optional. The exception class to raise, if any.




:py:mod:`myLibs.RN2903`
=======================

.. py:module:: myLibs.RN2903


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.RN2903.RN2903
   myLibs.RN2903.RN2903_Radio
   myLibs.RN2903.RN2903_Lora




.. py:class:: RN2903(comDriver, buffer, name='None')


   .. py:attribute:: _MODULE
      :value: ''

      

   .. py:attribute:: _VERSION
      :value: ''

      

   .. py:attribute:: _EUI
      :value: ''

      

   .. py:attribute:: _MACPAUSE
      :value: ''

      

   .. py:method:: open(callback, RadioConfig, Buffer)


   .. py:method:: close()


   .. py:method:: receive(**kwargs)


   .. py:method:: commandSendAndReceive(data, **kwargs)


   .. py:method:: commandSendAndValidate(data, validation, **kwargs)


   .. py:method:: dataSend(data)


   .. py:method:: dataSendAndValidate(data, validation, loopTime)


   .. py:method:: sendToBuffer(data, **kwargs)


   .. py:method:: getDeviceInfo()


   .. py:method:: factoryReset()


   .. py:method:: encodeData(data)


   .. py:method:: decodeData(data)


   .. py:method:: timeOnAir(spreadfactor, bandwidth, codingrate, header='off', optimization='on', payload_size=30, preamble_length=8)


   .. py:method:: configure()
      :abstractmethod:


   .. py:method:: receiveCallback(data)
      :abstractmethod:



.. py:class:: RN2903_Radio(comDriver, buffer, name='None')


   Bases: :py:obj:`RN2903`

   .. py:method:: configure(config)


   .. py:method:: receiveCallback(data)


   .. py:method:: startReceive()


   .. py:method:: stopReceive()


   .. py:method:: Testing(callback, testMessage, currentConfig, RadioConfig, Buffer)

      Args
          - configuration: specific to the RN2903 
          - message: line number 
      Return 
          - True of false based on Radio Tx OK 
      Function
          - update testing configurations of the device 
          - send the message 
          - validate the message was sent 
          - return the validation and the time from ok to TX_Ok 



.. py:class:: RN2903_Lora(config, comDriver, buffer, name='None')


   Bases: :py:obj:`RN2903`

   .. py:method:: configure()


   .. py:method:: receiveCallback(data)




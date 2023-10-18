:py:mod:`myLibs.RN2483`
=======================

.. py:module:: myLibs.RN2483


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.RN2483.RN2483
   myLibs.RN2483.RN2483_Radio
   myLibs.RN2483.RN2483_Lora




.. py:class:: RN2483(comDriver, buffer, name='None')


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


   .. py:method:: timeOnAir(spreadfactor, bandwidth, codingrate, header, optimization, payload_size, preamble_length)


   .. py:method:: configure()
      :abstractmethod:


   .. py:method:: receiveCallback(data)
      :abstractmethod:



.. py:class:: RN2483_Radio(comDriver, buffer, name='None')


   Bases: :py:obj:`RN2483`

   .. py:method:: configure(config)


   .. py:method:: receiveCallback(data)


   .. py:method:: startReceive()


   .. py:method:: stopReceive()



.. py:class:: RN2483_Lora(config, comDriver, buffer, name='None')


   Bases: :py:obj:`RN2483`

   .. py:method:: configure()


   .. py:method:: receiveCallback(data)




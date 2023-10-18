:py:mod:`src.receiver`
======================

.. py:module:: src.receiver


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   src.receiver.create_obj
   src.receiver.read_config
   src.receiver.read_batch
   src.receiver.get_config
   src.receiver.save_to_csv
   src.receiver.find_os
   src.receiver.save_new_data_to_csv
   src.receiver.radio_setup
   src.receiver.send_config
   src.receiver.callback
   src.receiver.sync_to_start
   src.receiver.sync_to_next_batch



Attributes
~~~~~~~~~~

.. autoapisummary::

   src.receiver.batch_config_file
   src.receiver.batch_time_file
   src.receiver.all_configs_file
   src.receiver.RED
   src.receiver.GREEN
   src.receiver.YELLOW
   src.receiver.RESET
   src.receiver.settings
   src.receiver.radio_rn2903
   src.receiver.current_time
   src.receiver.received_messages_array
   src.receiver.start_time
   src.receiver.configurations


.. py:function:: create_obj()


.. py:function:: read_config(file)


.. py:function:: read_batch(file)


.. py:function:: get_config(index, config)


.. py:function:: save_to_csv(df, file)


.. py:function:: find_os()


.. py:function:: save_new_data_to_csv(file)


.. py:function:: radio_setup(obj, callback, settings)


.. py:function:: send_config(obj, config_line)


.. py:function:: callback(message)


.. py:function:: sync_to_start()


.. py:function:: sync_to_next_batch(next_batch_number, batch_time)


.. py:data:: batch_config_file
   :value: 'csv/module_configurations_slave.csv'

   

.. py:data:: batch_time_file
   :value: 'csv/batch_file.csv'

   

.. py:data:: all_configs_file
   :value: 'csv/module_configurations.csv'

   

.. py:data:: RED
   :value: '\x1b[91m'

   

.. py:data:: GREEN
   :value: '\x1b[92m'

   

.. py:data:: YELLOW
   :value: '\x1b[93m'

   

.. py:data:: RESET
   :value: '\x1b[0m'

   

.. py:data:: settings

   

.. py:data:: radio_rn2903

   

.. py:data:: current_time

   

.. py:data:: received_messages_array
   :value: []

   

.. py:data:: start_time

   

.. py:data:: configurations

   


:py:mod:`calc_batch`
====================

.. py:module:: calc_batch


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   calc_batch.read_config
   calc_batch.get_config
   calc_batch.write_batch
   calc_batch.timeOnAir



Attributes
~~~~~~~~~~

.. autoapisummary::

   calc_batch.test_file
   calc_batch.batch_file
   calc_batch.config_df
   calc_batch.batch_df


.. py:data:: test_file
   :value: 'module_configurations.csv'

   

.. py:data:: batch_file
   :value: 'batch_file.csv'

   

.. py:function:: read_config(test_file)


.. py:function:: get_config(index, config)


.. py:function:: write_batch(batch_size, file_path, config_df, batch_df)


.. py:function:: timeOnAir(spreadfactor, bandwidth, codingrate, header='off', optimization='on', payload_size=23, preamble_length=8)


.. py:data:: config_df

   

.. py:data:: batch_df

   


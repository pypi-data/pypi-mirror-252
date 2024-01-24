hexrec.formats.motorola.Record
==============================

.. currentmodule:: hexrec.formats.motorola

.. autoclass:: Record
   :members:
   :inherited-members:
   :private-members:
   :special-members:

   
   
   .. rubric:: Methods

   .. autosummary::
      :nosignatures:
   
      ~Record.__init__
      ~Record.build_count
      ~Record.build_data
      ~Record.build_header
      ~Record.build_standalone
      ~Record.build_terminator
      ~Record.check
      ~Record.check_sequence
      ~Record.compute_checksum
      ~Record.compute_count
      ~Record.fit_count_tag
      ~Record.fit_data_tag
      ~Record.fix_tags
      ~Record.get_header
      ~Record.get_metadata
      ~Record.is_data
      ~Record.load_blocks
      ~Record.load_memory
      ~Record.load_records
      ~Record.marshal
      ~Record.overlaps
      ~Record.parse_record
      ~Record.read_blocks
      ~Record.read_memory
      ~Record.read_records
      ~Record.readdress
      ~Record.save_blocks
      ~Record.save_memory
      ~Record.save_records
      ~Record.set_header
      ~Record.split
      ~Record.unmarshal
      ~Record.update_checksum
      ~Record.update_count
      ~Record.write_blocks
      ~Record.write_memory
      ~Record.write_records
   
   

   
   
   .. rubric:: Attributes

   .. autosummary::
   
      ~Record.tag
      ~Record.count
      ~Record.address
      ~Record.data
      ~Record.checksum
      ~Record.EXTENSIONS
      ~Record.LINE_SEP
      ~Record.MATCHING_TAG
      ~Record.REGEX
      ~Record.TAG_TO_ADDRESS_LENGTH
      ~Record.TAG_TO_COLUMN_SIZE
   
   
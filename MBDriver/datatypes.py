from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder



builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)

builder.add_8bit_uint(12)
payload = builder.to_registers()
print payload
payload = builder.build()
print payload

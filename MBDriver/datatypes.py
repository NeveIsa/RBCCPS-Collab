import sys
import logging
import loggingcolormod


from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder




"""

NOTE:

    The byte-endianness and word-endianness are determined by the order in which the BYTES and WORDS arrive on the serial bus. It has nothing to do with the endianness of the client and the Master devices as long as using REGISTER wise access from a SANE client and master library as the library handles the byte-endianness at both the machines.
    
    The byte-endianness has nothing to do how WORDS/BYTES/THINGS are stored in the REGISTERS(MEMORY) i.e endianness of the client machine or the master machine.
    
    This is because no matter the endianness of the machine, the modbus specifies that the registers be sent in BIG ENDIAN format. So a SANE modbus client implementation will always send the MSB of the register word first and then the LSB of the register word and the client library will take care of the actual endianness of the client device.

    Similarly a Master library should always treat the 1st byte as MSB and the 2nd byte as the LSB and then store in the host machine taking care of the endianness such that a 16bit(WORD) type struture/variable on the master machine reads the same as that on the client device.

    Now that byte endianness is all sorted and made unambiguous by the modbus specificationand that any Modbus master library will give us REGISTER/WORD access rather than to byte acess,  we can forget all about the byte-endianness as it is ABSTRACTED by the library. 



    So we should never change the byte-endianness unless some device is CRAZY and MURDERS the modbus specs to send bytes in opposite order i.e. LSB first and then MSB.

    NOW lets get to the word-endianness.
    
    
    
    Because we address Modbus as ABSTRACT REGISTERS/WORDS addresses, we must think of the memory as WORDS/REGISTERS and independent of the endianness of the client device or the master device.
    
    Word-endianness has to do how things are stored in the CLIENT MODBUS DEVICE'S ABSTRACTED MEMORY - which are caled Registers. If the MSW is stored in the LOWER register and LSW in the higer register, it is big endian. 
    
    As we read multiple registers in SERIES, it also follows that the MSW (lower registeri, sya 40001) will be put on the serial bus first and then the LSW(higher register, say 40002). So in a general sense, we can consider HOW BYTES AND WORDS/REGISTERS ARRIVE ON THE SERIAL BUS DETERMINE THE BYTE AND WORD ENDIANNESS.


    Now when we read registers from an address, say 2 registers together are read, the first register is sent and then the second register. Now if we use Big endian for WORD-Endianness in using this master library, the first register, say 40001 should contain the MSW and 40002 should contain the LSW. Now from the perspective of ABSTRACTDR MODBUS memory locations, when we consider the modbus registers as memory locations, we see that the lower address(40001) contains the MSW and the higher address(40002) contains the LSW. Now that is infact a BIG-Endian configuration which states that the MSU (U=unit, could be BYTE or WORD or whatever the unit be) is stored in lower memory locations/addresses and LSU be stored in Higher memory locations/addresses  



NOW there is a responsibility for the people who fill the Registers in the client devices, lets say using an Arduino and a modbus client library.
As long as word size varaiables are used, the modbus client library should take care to send the bytes of the variable in Big-Endian format. But whn we want to implement variables of 4 bytes or more, the designer has to take care for the endianness of the device and figure out how to put the MSW of the 4 byte, for examaple, to the register address 40001 and the LSW to the register address 40002 if the master library here is configure to Word-Endianness = big.

Because we know that the WORD/REGISTER level values will be communicated properly due to the abstaractions  mentioned at REGISTER level by the client and the master library, we donot have to worry about the byte level endianness and most of the time can be left configured to big-endian as thats the specs of Modbus.


"""




def data2registers(data, datatype, byteEndianness="big", wordEndianness="big"):
    ndata = len(data)

    if byteEndianness=='big': bOrder = Endian.Big
    else: bOrder = Endian.Little

    if wordEndianness=='big': wOrder = Endian.Big
    else: wOrder = Endian.Little

    #builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
    builder = BinaryPayloadBuilder(byteorder=bOrder,wordorder=wOrder)
    
    #builder.add_string('abcdefgh')
    #builder.add_bits([0, 1, 0, 1, 1, 0, 1, 0])
    #builder.add_8bit_int(-0x12)
    #builder.add_8bit_uint(0x12)
    #builder.add_16bit_int(-0x5678)
    #builder.add_16bit_uint(0x1234)
    #builder.add_32bit_int(-0x1234)
    #builder.add_32bit_uint(0x12345678)
    #builder.add_32bit_float(22.34)
    #builder.add_32bit_float(-22.34)
    #builder.add_64bit_int(-0xDEADBEEF)
    #builder.add_64bit_uint(0x12345678DEADBEEF)
    #builder.add_64bit_uint(0x12345678DEADBEEF)
    #builder.add_64bit_float(123.45)
    #builder.add_64bit_float(-123.45)
        

    if datatype=="int8":
        add_data = builder.add_8bit_int
    elif datatype=="int16":
        add_data = builder.add_16bit_int
    elif datatype=="int32":
        add_data = builder.add_32bit_int
    elif datatype=="int64":
        add_data = builder.add_64bit_int
    
    elif datatype=="uint8":
        add_data = builder.add_8bit_uint    
    elif datatype=="uint16":
        add_data = builder.add_16bit_uint
    elif datatype=="uint32":
        add_data = builder.add_32bit_uint
    elif datatype=="uint64":
        add_data = builder.add_64bit_uint

    elif datatype=="float32":
        add_data = builder.add_32bit_float
    elif datatype=="float64":
        add_data = builder.add_64bit_float

    elif datatype=="string":
        logging.error("----------> strings are not supported yet in datatypes.py")
        sys.exit(1)
        add_data = builder.add_string
    
    else:
        logging.error("---> Invalid datatype: %s to encode..." % datatype)


    for datum in data:
        add_data(datum)


    #payload = builder.build()
    #print (payload)
    
    
    payload = builder.to_registers()
    #print (payload)
    
    return payload


def registers2data(registers, datatype, no_of_data_points=0, byteEndianness="big", wordEndianness="big"):
    '''
    
    Number of data points is the number of data units to decode, like how many int32 are present in the parameter registers

    no_of_data_points=0,None,False means the number of registers will be automatically calculated from the no of items in the params 'registers' and 'datatype'
    
    '''


    if not no_of_data_points:
        """ Autodetect length"""

        # modbus registers are 2 bytes long - 16 bits
        no_bytes_reg = len(registers)*2 

        if "8" in datatype: datatype_size = 1
        elif "16" in datatype: datatype_size = 2
        elif "32" in datatype: datatype_size = 4
        elif "64" in datatype: datatype_size = 8

        no_of_data_points = int(no_bytes_reg / datatype_size)
        logging.info("--> Autodetected register decode size - nbytes_in_regs: %s, datatype_size: %s, no_of_data_points: %s" % (no_bytes_reg, datatype_size, no_of_data_points) )


    if byteEndianness=='big': bOrder = Endian.Big
    else: bOrder = Endian.Little

    if wordEndianness=='big': wOrder = Endian.Big
    else: wOrder = Endian.Little
    
    #decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Little, wordorder=Endian.Little)
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=bOrder, wordorder=wOrder)

    # decoded = OrderedDict([
    # ('string', decoder.decode_string(8)),
    # ('bits', decoder.decode_bits()),
    # ('8int', decoder.decode_8bit_int()),
    # ('8uint', decoder.decode_8bit_uint()),
    # ('16int', decoder.decode_16bit_int()),
    # ('16uint', decoder.decode_16bit_uint()),
    # ('32int', decoder.decode_32bit_int()),
    # ('32uint', decoder.decode_32bit_uint()),
    # ('32float', decoder.decode_32bit_float()),
    # ('32float2', decoder.decode_32bit_float()),
    # ('64int', decoder.decode_64bit_int()),
    # ('64uint', decoder.decode_64bit_uint()),
    # ('ignore', decoder.skip_bytes(8)),
    # ('64float', decoder.decode_64bit_float()),
    # ('64float2', decoder.decode_64bit_float()),
    # ])

    if datatype=="int8":
        get_data = decoder.decode_8bit_int
    elif datatype=="int16":
        get_data = decoder.decode_16bit_int
    elif datatype=="int32":
        get_data = decoder.decode_32bit_int
    elif datatype=="int64":
        get_data = decoder.decode_64bit_int

    elif datatype=="uint8":
        get_data = decoder.decode_8bit_uint
    elif datatype=="uint16":
        get_data = decoder.decode_16bit_uint
    elif datatype=="uint32":
        get_data = decoder.decode_32bit_uint
    elif datatype=="uint64":
        get_data = decoder.decode_64bit_uint

    elif datatype=="float32":
        get_data = decoder.decode_32bit_float
    elif datatype=="float64":
        get_data = decoder.decode_32bit_float

    elif datatype=="string":
        logging.error("----------> strings are not supported yet in datatypes.py")
        sys.exit(1)
        get_data = decoder.decode_string
    
    else:
        logging.error("---> Invalid datatype: %s to decode..." % datatype)


    _data=[]


    for _ in range(no_of_data_points):
        _data.append(get_data())

    return _data




if __name__ == "__main__":
    import time,yaml
    from pymodbus.client.sync import ModbusSerialClient as ModbusClient
    
    ### CONNECT TO SERIAL ###

    with open("drvConf.yml") as f:
        logging.debug("Loading drvConf.yml")
        drvConf=yaml.load(f.read())

    """
    MQTT_HOST=drvConf["MQTT_HOST"]
    MQTT_PORT=drvConf["MQTT_PORT"]
    MB_DISCOVERY_INTERVAL=drvConf["MB_DISCOVERY_INTERVAL"]
    MB_DISCOVERY_DEVICE_ID=drvConf["MB_DISCOVERY_DEVICE_ID"]
    MB_DISCOVERY_DEVICE_META_REGISTER_ADDR=drvConf["MB_DISCOVERY_DEVICE_META_REGISTER_ADDR"]
    DEVICE_CONF_UPDATE_CHECK_INTERVAL=drvConf["DEVICE_CONF_UPDATE_CHECK_INTERVAL"]
    """
    logging.debug("loaded...")


    #drvConf["serialConf"]["baudrate"]=9600
    drvConf["serialConf"]["timeout"]=0.1

    logging.info("Attempting : {}:{}".format(drvConf["serialConf"]["port"],drvConf["serialConf"]["baudrate"]))
    client=ModbusClient(**drvConf["serialConf"])
    if not client.connect():
        logging.error("Could not connect to serial port... Exiting")
        exit()
    time.sleep(3)
    logging.info("Connected...")


    for i in range(1000):
        import time
        #time.sleep(0.001)
        result = client.read_holding_registers(0,2,unit=1)

        if result.isError(): 
            print("Failed modbus read")
            continue
        #sys.exit()
        
        data = registers2data(result.registers,"float32",0,"big","big")
        print (result.registers,data)


        result = client.read_holding_registers(2,2,unit=1)

        if result.isError(): 
            print("Failed modbus read")
            continue
        
        data = registers2data(result.registers,"float32",0,"big","big")
        print (result.registers,data)
        
        exit()


       



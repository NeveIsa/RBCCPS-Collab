import time,yaml
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import logging
import loggingcolormod

import time

with open("drvConf.yml") as f:
    logging.debug("Loading drvConf.yml")
    drvConf=yaml.load(f.read())
    MQTT_HOST=drvConf["MQTT_HOST"]
    MQTT_PORT=drvConf["MQTT_PORT"]
    MB_DISCOVERY_INTERVAL=drvConf["MB_DISCOVERY_INTERVAL"]
    MB_DISCOVERY_DEVICE_ID=drvConf["MB_DISCOVERY_DEVICE_ID"]
    MB_DISCOVERY_DEVICE_META_REGISTER_ADDR=drvConf["MB_DISCOVERY_DEVICE_META_REGISTER_ADDR"]
    DEVICE_CONF_UPDATE_CHECK_INTERVAL=drvConf["DEVICE_CONF_UPDATE_CHECK_INTERVAL"]
    logging.debug("loaded...")


from gwtools import services as gwservices
device=gwservices.Device(drvConf["DRIVER_NAME"])
device.setup()


### CONNECT TO SERIAL ###

logging.info("Attempting : {}:{}".format(drvConf["serialConf"]["port"],drvConf["serialConf"]["baudrate"]))
client=ModbusClient(**drvConf["serialConf"])
if not client.connect():
    logging.error("Could not connect to serial port... Exiting")
    exit()
time.sleep(3)
logging.info("Connected...")



### CONNECT TO SERIAL ###


def discoverNewDev():
    """
    Reads a holding register to figure out if the deviceID=MB_DISCOVERY_DEVICE_ID is on bus
    """
    # Read 1 register at address MB_DISCOVERY_REGISTER_ADDR
    # and deviceID=unit=MB_DISCOVERY_DEVICE_ID
    logging.info("Running discovery for devID:{} by reading holding register {} | timeout:{} second(s)".format(MB_DISCOVERY_DEVICE_ID,MB_DISCOVERY_DEVICE_META_REGISTER_ADDR,client.socket.timeout))
    result = client.read_holding_registers(MB_DISCOVERY_DEVICE_META_REGISTER_ADDR,1,unit=MB_DISCOVERY_DEVICE_ID)
    if result.isError():
        logging.info("No new device discovered...")
    else:
        new_device_meta_id = result.registers[0]
        logging.warning("New device discovered at ID:{} with device_meta_id:{}".format(MB_DISCOVERY_DEVICE_ID,new_device_meta_id))
        newDevInfo={"devID":MB_DISCOVERY_DEVICE_ID,"metaID":new_device_meta_id}
        device.reportDiscovery(newDevInfo)
        return newDevInfo
    

def readReg(entry):
    """To read the register, given its deviceID, register address, number of registers and register type."""
    
    devID,addr,nRegs,regType,devName,scaling,mqttSubTopic,unpackFormat,devModbusEndianness = entry["devID"],entry["addr"],entry["nRegs"],entry["regType"],entry["devName"],entry["scaling"],entry["mqttSubTopic"],entry["unpackFormat"],entry["devModbusEndianness"]

    if regType=="holding":
        result=client.read_holding_registers(addr,nRegs,unit=devID)                                    
    elif regType=="input":
        result=client.read_input_registers(addr,nRegs,unit=devID)
    else:
        logging.error("In readReg -> Invalid regType:%s" % regType)
        return None
    
    if result.isError():
        logging.error ("Couldn't read register in function 'readReg' \n\t--> devID:%s  addr:%s  nRegs:%s  regType:%s" % (devID, addr, nRegs,regType))
        return None

    if unpackFormat=="integer":
        dataValue = result.registers[0]
    elif unpackFormat=="float":
        logging.error("In readReg --> unpackFormat - float : Not supported yet")
        return 

    logging.info("In readReg -> %.3f | devID:%s addr:%s  nRegs:%s devName:%s regValues: %s mqttSubTopic:%s" % (time.time(),devID,addr,nRegs,devName,result.registers,mqttSubTopic))
    subTopic="{}/{}".format(devName,mqttSubTopic)
    device.reportSensorVal(subTopic,str(dataValue))
    return result.registers

def writeReg(entry,data2write):
    devID,addr,devModbusEndianness,packFormat = entry["devID"],entry["addr"],entry["devModbusEndianness"],entry["packFormat"]
    
    if packFormat=="integer":
        pass
    elif packFormat=="float":
        logging.error("In writeReg --> packFormat - float: Not supported yet...")
        return

    if type(data2write)==list:
        print(client.write_registers(addr,data2write,unit=devID))
    elif type(data2write)==int:
        print(client.write_register(addr,data2write,unit=devID))
    else:
        logging.error("In writeReg -> data2write must be of type list or int, found %s " % type(data2write))
        return

    logging.warning("In writeReg -> Writing to devID:%s addr:%s value(s):%s" % (devID,addr,data2write))


def subscribeIncomingSubTopic(subtopic):
    device.subscribeIncomingSubtopics(subtopic)

def startListening():
    device.startListening()

def stopListening():
    device.stopListening()

def messageAvailable():
    return device.messageInwaiting()

def messageRead():
    return device.messageGet()

if __name__=="__main__":
    import MBscheduler
    
    #first run a discovery
    discoverNewDev()



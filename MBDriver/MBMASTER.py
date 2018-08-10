import signal,sys,time
import json

def signal_handler(signal, frame):
        print('Exiting gracefully...')
        time.sleep(0.5)
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

import logging,loggingcolormod

import loadConf
import MBdrv
import MBscheduler

import datatypes

# Use the actual driver function not the dummy one provided above
MBscheduler.modbusPoll = MBdrv.readReg

lastConfUpdateTS = 0
lastDevDiscoveryTS = 0
now = last = time.time()

WriteRegMqttSubTopics=[]


def getConfigFromDevID(devID,allConfigs):
    for conffilename in allConfigs:
        conf = allConfigs[conffilename]
        if conf["modbusDevID"]==devID:
            return conf

    #if not found, return None
    return None

        


while True:
    if now - lastDevDiscoveryTS > MBdrv.MB_DISCOVERY_INTERVAL:
        MBdrv.discoverNewDev()
        lastDevDiscoveryTS = now

    if now - lastConfUpdateTS > MBdrv.DEVICE_CONF_UPDATE_CHECK_INTERVAL:
        # print("\n"+ "-----"*8)
        logging.warning("|| Rechecking Config files for changes ||".upper())
        # print("-----"*8)


        # LOAD DEVICE CONFIGS
        mbconfig, priorities = loadConf.mainLoadConfig()
        read_entries,write_entries = MBscheduler.generate_scheduler_entries(mbconfig, priorities)
        
        lastConfUpdateTS = now
        # time.sleep(3)

    # REGISTER WRITE ENTRIES MQTT SUBTOPIC IF NOT ALREADY DONE
    newSubtopicFound=False

    for entry in write_entries:
        # subscribe only if not already subscribed
        mqttsubtopic = entry["mqttSubTopic"]
        if not mqttsubtopic in WriteRegMqttSubTopics:
            logging.warning("New writeReg mqttSubTopic detected: %s" % mqttsubtopic)
            MBdrv.subscribeIncomingSubTopic(mqttsubtopic)
            WriteRegMqttSubTopics.append(mqttsubtopic)
            newSubtopicFound=True
            #print (entry)
    
    if newSubtopicFound:
        logging.warning("-> New SubTopic (for writeRegs) detected.... Restarting MQTT Loop...")
        MBdrv.stopListening() # stop mqtt loop - done for safety, not really necessary
        MBdrv.startListening() # start mqtt loop to start handling callbacks
    

    # SCHEDULE ONE SHOT 
    maxTP = MBscheduler.oneshot_schedule(read_entries)

    ###################  READ MODBUS AND SEND VIA MQTT  ###################
    
    # Run only if entries is not empty
    if len(read_entries):
        
        past = time.time()
        logging.info("scheduler run started: %s" % str(past))
        MBscheduler.MBSCHED.run()

        now = time.time()
        logging.info("scheduler stopped: %s" % str(now))
        scheduler_running_time = now-past

        # Check if it took scheduler more time than maxTP as we should
        # complete one round of scheduling within maxTP

        if scheduler_running_time > maxTP:
            logging.error("Scheduler run took (blocking): %s seconds | this is more than allowed maxTP=%s seconds" % (scheduler_running_time, maxTP))
        else:
            logging.warning("Scheduler run took (blocking): %s second(s)" % scheduler_running_time)
    else:
        logging.warning("-> No read_entries found in conf files.... sleeping for a moment.")
        time.sleep(1)

    


    ###################  READ MODBUS AND SEND VIA MQTT  ###################
    
    
    ###################  WRITE MODBUS AFTER READING MQTT VIA QUEUE  ###################
    
    while MBdrv.messageAvailable():
        msg=MBdrv.messageRead()
        #logging.warning (msg)

        # Filter from write entries all the devices/registers whose "mqttSubTopic" match the msg's "subtopic"
        entriesThatNeedWrite = list(filter(lambda x:x["mqttSubTopic"]==msg["subtopic"], write_entries))


        
        for entry in entriesThatNeedWrite:
            #logging.warning(entry)
            #msg = int(msg['message'])

            # MESSAGES ON MQTT ARE ALWAYS RECEIVED IN JSON ARRAY FORMAT 
            # (Upgrades can be made later as we are using JSON, for now only JSON arrays are supported 
            # as they map directly to registers )

            # load msg and check validity as array
            try:
                message = json.loads(msg["message"].decode("utf8"))
                assert(type(message)==list)
            except Exception as e:
                logging.error("In MBMASTER --> Exception on loading json from msg OR asserting type(msg) as list: %s" % e)
                logging.error("In MBMASTER --> Exception on msg: %s" % str(msg))
                

            # convert/encode data to registers - 
            # find out in advance how many registers will be needed for given datatype/packFormat
            # this is needed so that we can decide whether to use WriteMultipleRegisters function code or not.
            _registers=datatypes.data2registers(message,entry["packFormat"],entry["devModbusEndianness"]["byte"],entry["devModbusEndianness"]["word"])

            # check if device has WriteMultipleRegistersFunctionSupport
            conf=getConfigFromDevID(entry["devID"],mbconfig)
            
            # if device supports WriteMultipleRegistersFunctionSupport
            if conf["WriteMultipleRegistersFunctionSupport"]==True and len(_registers)>1:
                # do not encode anymore as we have already encoded, so encode2registers is False
                MBdrv.writeReg(entry,data2write=_registers,encode2registers=False)
                logging.warning("In MBMASTER --> Wrote %s registers, entry:%s" % (len(_registers),entry) )

            else: 
                # If valid, write to modbus one register at a time
                import copy
                temp_entry = copy.deepcopy(entry)
                
                for __reg in _registers:
                    #print (temp_entry)
                    
                    # do not encode anymore as we have already encoded, so encode2registers is False
                    MBdrv.writeReg(temp_entry,data2write=__reg,encode2registers=False)

                    # Manually increment register address
                    temp_entry["addr"]+=1

                    logging.warning("In MBMASTER --> Wrote 1 register, entry:%s" % entry )




    ###################  WRITE MODBUS AFTER READING MQTT VIA QUEUE  ###################
   
   

   # exit()

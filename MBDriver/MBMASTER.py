import signal,sys,time

def signal_handler(signal, frame):
        print('Exiting gracefully...')
        time.sleep(0.5)
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

import logging,loggingcolormod

import loadConf
import MBdrv
import MBscheduler

# Use the actual driver function not the dummy one provided above
MBscheduler.modbusPoll = MBdrv.readReg

lastConfUpdateTS = 0
lastDevDiscoveryTS = 0
now = last = time.time()

WriteRegMqttSubTopics=[]

while True:
    if now - lastDevDiscoveryTS > MBdrv.MB_DISCOVERY_INTERVAL:
        MBdrv.discoverNewDev()
        lastDevDiscoveryTS = now

    if now - lastConfUpdateTS > MBdrv.DEVICE_CONF_UPDATE_CHECK_INTERVAL:
        # print("\n"+ "-----"*8)
        logging.warning("|| Rechecking Config files for changes ||".upper())
        # print("-----"*8)
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
        entryNeedsWrite = list(filter(lambda x:x["mqttSubTopic"]==msg["subtopic"], write_entries))
        for entry in entryNeedsWrite:
            #logging.warning(entry)
            MBdrv.writeReg(entry["devID"],entry["addr"],20)



    ###################  WRITE MODBUS AFTER READING MQTT VIA QUEUE  ###################
   
   

   # exit()

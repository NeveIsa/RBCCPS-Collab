import logging
import loggingcolormod

import sched, time
from pprint import pprint

# Exploration is needed to be done to fid out how to make 
# sched.scheduler work with gevent time and sleep funtions
MBSCHED = sched.scheduler(time.time, time.sleep)

def modbusPoll(entry):
    """
    devID:                  modbus Dev ID
    addr:                   register Addr
    nRegs:                  no. of registers to read in contiguous read
    regType
    """

    devID,addr,nRegs,regType,devName,scaling,mqttSubTopic = entry["devID"],entry["addr"],entry["nRegs"],entry["regType"],entry["devName"],entry["scaling"],entry["mqttSubTopic"]
        
    
    logging.info("Dummy modbusPoll | %s | devID:%s addr:%s nReg:%s regType:%s devName:%s mqttSubTopic:%s" % (time.time(),devID,addr,nRegs,regType,devName,mqttSubTopic))
    #time.sleep(.0049)
    return

def generate_scheduler_entries(mbconfig,priorities):
    """
    Generates simple single entries from the global config file passed to it
    """
    scheduler_read_entries=[]
    scheduler_write_entries=[]

    for _filename in priorities:
        logging.info("\nNow Processing for scheduling entries in: " + _filename)
        thisConf=mbconfig[_filename]
        #pprint(thisConf)

        devID=thisConf["modbusDevID"]
        devName=thisConf["name"]
        devModbusEndianness = thisConf["devModbusEndianness"]


        if "readRegs" in thisConf:
            readRegs=thisConf["readRegs"]
        else:
            readRegs=[]

        #nRegs=thisConf["nRegs"]
        
        if "writeRegs" in thisConf:
            writeRegs=thisConf["writeRegs"]
        else:
            writeRegs=[]

        
        # INSERT IMPORTANT CONFIGS FROM CONFIG FILE INTO INDIVIDUAL ENRTRIES

        for i in range(len(readRegs)):
            readRegs[i]["devID"]=devID
            readRegs[i]["devName"]=devName
            readRegs[i]["devModbusEndianness"]=devModbusEndianness
            readRegs[i]["timeperiod"]=1.0/readRegs[i]["rate"]

        for i in range(len(writeRegs)):
            writeRegs[i]["devID"]=devID
            writeRegs[i]["devName"]=devName
            readRegs[i]["devModbusEndianness"]=devModbusEndianness
            
            if writeRegs[i]["rate"]>0:
                writeRegs[i]["timeperiod"]=1.0/writeRegs[i]["rate"]
            else:
                writeRegs[i]["timeperiod"]=0

        # INSERT IMPORTANT CONFIGS FROM CONFIG FILE INTO INDIVIDUAL ENRTRIES

        for r in readRegs:
            logging.info ("read--> %s " % r)
            scheduler_read_entries.append(r)

        """
        ToDo - ADD entries for write as well. Not done yet 
        Maybe writing to modbus registers are better left to be async, i.e write as message arrive 
        on MQTT topic rather than writing at scheduled intervals
        """
        for w in writeRegs:
            logging.info ("write(todo)--> %s " % w)
            scheduler_write_entries.append(w)

    return scheduler_read_entries,scheduler_write_entries
            
            
def oneshot_schedule(entries):
    #find max timeperiod
    maxTP=0
    for entry in entries:
        maxTP=max(entry["timeperiod"],maxTP)
    
    # Scheduler schedules(inserts into scheduler queue) once every maxTP seconds.
    # Then scheduler.run() is called which blocks for maxTP seconds

    # limit minimun of maxTP to 1sec, if maxTP less than 1sec, make it 1sec
    # This is to make scheduling atmost once in a second but no more
    # as we don't want too much scheduling overhead
    maxTP=max(maxTP,1)

    logging.warning("Scheduling modbus 'READ' entries for a time of maxTP = %s second(s)" % maxTP)

    for entry in entries:
        tp=entry["timeperiod"]
        args=(entry,)
        shots=int(maxTP/tp)
        
        logging.info("Adding scheduler entry --> devID:%s addr:%s" % (entry["devID"],entry["addr"]))
        logging.info ("Shots to fire in maxTP seconds: %s" % shots)
        

        #for _ in range(shots): #this has a logical problem -> think how (it fires at 0th, lets say 100Hz, ends at 99th and then when run is caled after scheduling, starts immediately at 99th clock. So the one at 99th and the next at 0th of next schedule are not their respective TP apart in time but are executed almost immediately. It also has another problem, think if shots=1. then it range(shots) is [0], so the call on run will execute at 0th clock and the next run will be started immediately after scheduling. So if TP=1s and shots=1, then this logic will lead to running continously without waiting for the next second as the call on run will not block till one second but return immediately as 0*tp = 0)
        for _ in range(1,shots+1):
            # each entry will be called only after scheduler.run is invoked 
            # and then the scheduler will call modbusPoll for each entry which
            # is a blocking call, hence there wont be collision on the serial bus

            # push the entries to scheduler.queues
            MBSCHED.enter( _ * tp ,1, modbusPoll,argument=args)
            #print ("--->" ,_ * tp,end=",")
        #print("\n")

    return maxTP




if __name__=="__main__":
    import loadConf
    import MBdrv

    # Use the actual driver function not the dummy one provided above
    modbusPoll=MBdrv.readReg

    lastConfUpdateTS=0
    lastDevDiscoveryTS=0
    now=last=time.time()
    while True:
        
        if now - lastDevDiscoveryTS > MBdrv.MB_DISCOVERY_INTERVAL:
            MBdrv.discoverNewDev()
            lastDevDiscoveryTS=now
        

        if now - lastConfUpdateTS > MBdrv.DEVICE_CONF_UPDATE_CHECK_INTERVAL:
            #print("\n"+ "-----"*8)
            logging.warning ("|| Rechecking Config files for changes ||".upper())
            #print("-----"*8)
            mbconfig,priorities=loadConf.mainLoadConfig()
            read_entries,write_entries=generate_scheduler_entries(mbconfig,priorities)
            lastConfUpdateTS=now
            #time.sleep(3)
        
        maxTP=oneshot_schedule(read_entries)
        
        past=time.time()
        logging.info("scheduler run started: %s" % str(past))
        MBSCHED.run()
        now=time.time()
        logging.info("scheduler stopped: %s" % str(now))
        scheduler_running_time=now-past
        
        # Check if it took scheduler more time than maxTP as we should  
        # complete one round of scheduling within maxTP

        if scheduler_running_time > maxTP:
            logging.error("Scheduler run took (blocking): %s seconds | this is more than allowed maxTP=%s seconds" % (scheduler_running_time,maxTP))
        else:
            logging.warning("Scheduler run took (blocking): %s second(s)" % scheduler_running_time)
        #exit()


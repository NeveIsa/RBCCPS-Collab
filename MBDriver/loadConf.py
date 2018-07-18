#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import json
import yaml

from pprint import pprint

# Validate YAML per conf file
import cerberus


# COLORS FOR TERMINAL
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


CONFIG_DIR = "conf.d"
LAST_SCANNED = 0
MODBUS_CONFIG = {}
MAX_NO_POLLS = 500 # @115200 freq. is ~750

def findConfFiles(_dir):
    global CONFIG_DIR, LAST_SCANNED
    if os.path.exists(_dir) :
        #print("Config files' path found.")
        confFiles=os.listdir(_dir)
        confFiles=filter(lambda x:x.endswith(".yml"),confFiles)
        confFiles=list(confFiles)
        #print (confFiles)
        return confFiles
    else:
        print("Config files' path NOT found:",_dir)
        
        
    
def isFileUpdated(_file):
    if LAST_SCANNED < os.path.getmtime(_file):
        return True
    else:
        return False
    
def readConfigFile(_file):
    with open(_file) as f:
        conf = f.read()
    try:
        conf=yaml.load(conf)
        return conf
    except Exception as e:
        print(e)
    
            
def validateConfigFile(_file):
    with open("conf.d/schema/schema.yml") as f:
        schema=f.read()
    
    with open(_file) as f:
        conf=f.read()
    
    schema=yaml.load(schema)
    #pprint(schema)
    #print ("\n====\n"*2)
    conf=yaml.load(conf)

    v=cerberus.Validator(allow_unknown=False)
    if v.validate(conf,schema):
        return True
    else:
        print("VALIDATION_ERROR:")
        pprint(v.errors)
        return False

def mainLoadConfig():
    print("\n" + "-----"*10)
    global LAST_SCANNED, MODBUS_CONFIG
    confFiles=findConfFiles(CONFIG_DIR)
    tempTime = int(time.time())
    print("FILES FOUND:\n--> "+"\n--> ".join(confFiles)+"\n" )

    for curFile in confFiles:
        curFile = CONFIG_DIR+"/"+ curFile
        print("....."*10)
        print("NOW PROCESSING CONF_FILE: "+curFile)  # HERE
            
        if isFileUpdated(curFile):
            print(bcolors.WARNING + "--> Found modified" + bcolors.ENDC)
            if validateConfigFile(curFile):
                print(bcolors.OKGREEN + "--> Valid Conf..." + bcolors.ENDC)
                MODBUS_CONFIG[curFile]=readConfigFile(curFile)
            else:
                print(bcolors.WARNING + "--> Invalid Conf... Ignoring" + bcolors.ENDC)
        
        else:
            print("--> Found unmodified")

        #print("\n" + "-----"*10)       

    # Filtering if more than MAX_RATE
    with open("drvConf.yml") as f:
        drvConf=yaml.load(f.read())
        MAX_POLL_RATE=drvConf["MAX_POLL_RATE"]

    # Sort the filenames by the priority defined in them
    priorities=sorted(MODBUS_CONFIG,key=lambda x:MODBUS_CONFIG[x]["priority"])
    
    LAST_SCANNED = tempTime
    #pprint(MODBUS_CONFIG)
    print ("\nPRIORITIES:\n",priorities)

    # Reject when MAX_POLL_RATE is exceeded
    accumulatedRate=0
    priorities_allowed_files_within_maxrate=[]
    
    print("\nFiltering for MAX_POLL_RATE")
    for _filename in priorities:
        thisConf=MODBUS_CONFIG[_filename]
        
        if "readRegs" in thisConf:
            for rreg in thisConf["readRegs"]:
                accumulatedRate+=rreg["rate"]

        if "writeRegs" in thisConf:
            for wreg in thisConf["writeRegs"]:
                accumulatedRate+=wreg["rate"]

        if accumulatedRate <= MAX_POLL_RATE:
            print ("-->Total poll rate till file:",_filename,bcolors.HEADER + str(accumulatedRate) + bcolors.ENDC)
            priorities_allowed_files_within_maxrate.append(_filename)
        else:
            print (bcolors.FAIL + "\nWARNING:\n---> REACHED MAX POLLING LIMIT >>> " + bcolors.UNDERLINE + _filename + bcolors.ENDC)
            print (bcolors.FAIL + "---> SOME CONF FILES WILL BE DROPPED !!!" + bcolors.ENDC)
            break

    print("\nPRIORITIES AFTER FILTERING TILL MAX_POLL_RATE:\n", priorities_allowed_files_within_maxrate)
    print( "-----"*10)       
    return MODBUS_CONFIG,priorities_allowed_files_within_maxrate         
            
    
if __name__ =="__main__":
    while (1):
        mainLoadConfig()
        break
        time.sleep(10)

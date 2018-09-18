
import yaml
import json
import requests


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
import loggingcolormod

from simple_rest_client.api import API


class Helper(object):
    def __init__(self):
        self.HTTPOK=200
        self.HTTPNOTFOUND=400
        self.HTTPERROR=500
    
    def loadYaml(self,filename):
        return yaml.load(open(filename+".yaml").read())

    def checkHTTPResponse(self,resp):
        status = resp.status_code

        if status in range(self.HTTPOK,self.HTTPOK+99):
            return True,status
        else:
            return False,status

    def loadDeviceByName(self,_name,_server):
        devicesConf=self.loadYaml("config/devices")
        if not _name in devicesConf:
            logging.error("Helper.loadDeviceByName --> Device by name: {} not present in config/devices.yaml")
            return None

        devConf = devicesConf[_name]
        device = Device(_name,devConf["apikey"],_server)
        logging.info("Helper.loadDeviceByName --> Loaded device: %s" % _name)

        return device

    def loadDeviceByIndex(self,_index,_server):
        devicesConf=self.loadYaml("config/devices")
        if _index > len(devicesConf)-1:
            logging.error("Helper.loadDeviceByName --> given index is more than devices found in config/devices.yaml")
            return None

        _name = list(devicesConf.keys())[_index]
        #print (_name)
        devConf = devicesConf[_name]
        print (devConf)
        device = Device(_name,devConf["apikey"],_server)
        logging.info("Helper.loadDeviceByName --> Loaded device: %s" % _name)

        return device

    def listDevices(self):
        devicesConf=self.loadYaml("config/devices")
        index=0
        print ("Listing devices in config file...")
        for devName in devicesConf:
            print ("{} - {}".format(index,devName))
            index+=1





class Server(object):
    def __init__(self,host,port,relative_api_base_url):
        self.host = host
        self.port = port
        self.relativeApiBase = relative_api_base_url

        if port:
            self.baseUrl = "https://{}:{}/{}".format(self.host,self.port,self.relativeApiBase)
        else:
            self.baseUrl = "https://{}/{}".format(self.host,self.relativeApiBase)

        logging.info("Server.__init__ -> baseUrl: %s" % self.baseUrl)


        self.api = API(
                api_root_url=self.baseUrl,
                params={},
                headers={'Cache-Control':'no-cache','Content-Type':'application/json'},
                timeout=2,
                append_slash=False,
                json_encode_body=True
                )

        self.api.add_resource(resource_name='register')

    def publishUrl(self,exchange):
        return "{}/publish/{}".format(self.baseUrl,exchange)
    
    def subscribeUrl(self,queue,nMsgs):
        return "{}/subscribe/{}/{}".format(self.baseUrl,queue,nMsgs)

            
class User(object):
    def __init__(self,user,apikey,server):
        self.server = server
        self.helper = Helper()
        logging.info("User.__init__ -> server registered")

class Device(object):
    def __init__(self,devName,devApiKey,server):
        self.devName = devName
        self.server = server
        self.devApiKey = devApiKey
        self.helper = Helper()
        
        logging.info("Device.__init__ -> device:%s instantiated with apikey: %s" % (self.devName,self.devApiKey) )
        


    def register(self,schema=None):
        if not schema:
            schema = {}
        r=self.api.register.create(body=schema, headers={'apikey':'guest'})
        

    def publish(self,exchangeName,data,relative=True):
        headers = {"Cache-Control": "no-cache","apikey": self.devApiKey,'routingKey':'#'}
        
        #jayload={"exchange":exchange,"body":data}
        #result=requests.post(server.publishUrl(),headers=headers,json=jayload)
        if relative:
            exchange = "{}.{}".format(self.devName,exchangeName)
        else:
            exchange = exchangeName
        
        result=requests.post(self.server.publishUrl(exchange),headers=headers,json=data,verify=False)
        ok,status = self.helper.checkHTTPResponse(result)
       
        if ok:
            logging.warning("Device.publish -> %s" % status)
            return result
        else:
            logging.warning("Device.publish -> Failed with HTTP code: %s" % status)
            logging.info(result.text)
            return None
        

    def subscribe(self,queueName,nMessages=1,relative=True):
        headers = {"Cache-Control": "no-cache","apikey": self.devApiKey}
        
        if relative:
            queue = "{}.{}".format(self.devName,queueName)
        else:
            queue = queueName
        logging.info("Subscribing to queue -> %s" % queue) 
        result = requests.get(self.server.subscribeUrl(queue ,nMessages), headers=headers, verify=False)
        ok,status=self.helper.checkHTTPResponse(result)
        
        if ok:
            logging.info("In ideamclient:subscribe -> status: %s" % status)
            return result
        else:
            logging.error("In ideamclient:subscribe -> Failed with status: %s" % status)
            return None

helper = Helper()

serverConf=helper.loadYaml("config/server")
server = Server(serverConf["host"],serverConf["port"],serverConf["relativeApiBase"])

helper.listDevices()
device = helper.loadDeviceByIndex(0,server)
    

if __name__ == "__main__":

    import time
    while True:

        #r=device.publish("protected","world")
        r=device.subscribe(device.devName,1,False)
        r=r.json()
        print(r)
        if len(r):
            pass
        else:
            time.sleep(5)
            pass
            #break

    print("======="*10)
    print("Flushed the queue")
    print("======="*10)
    time.sleep(2)

    for _ in range(10):
        #r=device.publish("follow","world:%s"%_)
        r=device.publish("protected","world:%s"%_)
        print(r.request.url)
        logging.info("Received -> %s" % r.text)
        r=device.subscribe(device.devName,1,False)
        print(r.json())
        time.sleep(1)

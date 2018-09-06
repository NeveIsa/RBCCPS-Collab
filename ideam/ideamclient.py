
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
        return yaml.load(open(filename+".yml").read())

    def checkHTTPResponse(self,resp):
        status = resp.status_code

        if status in range(self.HTTPOK,self.HTTPOK+99):
            return True,status
        else:
            return False,status

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
                headers={},
                timeout=2,
                append_slash=False,
                json_encode_body=True
                )

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
        


    def register(self):
        pass
        

    def publish(self,relativeExchangeName,data):
        headers = {"Cache-Control": "no-cache","apikey": self.devApiKey,'routingKey':'#'}
        
        #jayload={"exchange":exchange,"body":data}
        #result=requests.post(server.publishUrl(),headers=headers,json=jayload)
        exchange = "{}.{}".format(self.devName,relativeExchangeName)
        
        result=requests.post(self.server.publishUrl(exchange),headers=headers,json=data,verify=False)
        ok,status = self.helper.checkHTTPResponse(result)
       
        if ok:
            logging.warning("Device.publish -> %s" % status)
            return result
        else:
            logging.warning("Device.publish -> Failed with HTTP code: %s" % status)
            logging.info(result.text)
            return None
        

    def subscribe(self,relativeQueueName="follow",nMessages=1):
        headers = {"Cache-Control": "no-cache","apikey": self.devApiKey}
        
        queue = "{}.{}".format(self.devName,relativeQueueName)        
        
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

devicesConf=helper.loadYaml("config/devices")
for devName in devicesConf:
    devConf = devicesConf[devName]

logging.info("Loaded device -> %s" % devName)
device = Device(devName,devConf["apikey"],server)


    

if __name__ == "__main__":

    import time
    while True:
        r=device.subscribe("follow")
        r=r.json()
        print(r)
        if len(r):
            pass
        else: 
            break

    print("======="*10)
    time.sleep(2)

    for _ in range(10):
        #r=device.publish("follow","world:%s"%_)
        r=device.publish("protected","world:%s"%_)
        print(r.request.url)

        logging.info("Received -> %s" % r.text)
        #r=device.subscribe("follow")
        #print(r.json())
        #time.sleep(1)

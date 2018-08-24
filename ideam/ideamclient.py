import yaml
import json
import requests

import logging
import loggingcolormod




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

    def publishUrl(self):
        return "{}/{}".format(self.baseUrl,"publish")

            
class User(object):
    def __init__(self,user,apikey,server):
        self.server = server
        self.helper = Helper()
        logging.info("User.__init__ -> server registered")

class Device(object):
    def __init__(self,devApiKey,server):
        self.server = server
        self.devApiKey = devApiKey
        self.helper = Helper()
        logging.info("Device.__init__ -> device instantiated with apikey: %s" % self.devApiKey)

    def publish(self,exchange,data):
        headers = {"Cache-Control": "no-cache","apikey": self.devApiKey,'routingKey':'#'}
        
        #jayload={"exchange":exchange,"body":data}
        #result=requests.post(server.publishUrl(),headers=headers,json=jayload)
        
        result=requests.post("{}/{}".format(server.publishUrl(),exchange),headers=headers,json=data)
        ok,status = self.helper.checkHTTPResponse(result)
       
        if ok:
           logging.warning("Device.publish -> %s" % status)
        else:
            logging.warning("Device.publish -> Failed with HTTP code: %s" % status)
            logging.info(result.text)
        
        return result




helper = Helper()

serverConf=helper.loadYaml("config/server")
server = Server(serverConf["host"],serverConf["port"],serverConf["relativeApiBase"])

devicesConf=helper.loadYaml("config/devices")
for dConf in devicesConf:
    devConf = devicesConf[dConf]

logging.info("Loaded device -> %s" % dConf)
device = Device(devConf["apikey"],server)

if __name__ == "__main__":

    r=device.publish("hello","world")
    logging.info("Received -> %s" % r.text)

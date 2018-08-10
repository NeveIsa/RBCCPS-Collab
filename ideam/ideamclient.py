import yaml
import json

import requests


class Server(object):
    def __init__(self,host,port,api_base_url):
        self.host = host
        self.port = port
        self.relativeApiBase = api_base_url

        if port:
            self.baseUrl = "{}:{}/{}/".format(self.host,self.port,self.relativeApiBase) 

class User(object):
    def __init__(self,user,apikey,server):
        self.server = server
        pass

class Device(object):
    
    def __init__(self,devApiKey):
        self.devApiKey = devApiKey

    def publish(self,exchange,data):
        headers = {"Cache-Control": "no-cache","apikey": self.devApiKey}
        result=requests.post()


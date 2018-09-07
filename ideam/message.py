import datetime
import json

class Message:
    def __init__(self,msgtype="observation"):
        self.msgtype = msgtype
        self.messageID=1

    def create(self,jsonmsg={}):
        jsonmsg["timestamp"]=datetime.datetime.now().isoformat()
        jsonmsg["type"]=self.msgtype
        jsonmsg["messageID"]=self.messageID

        self.messageID+=1

        finalmsg = {self.msgtype: jsonmsg}

        return finalmsg



if __name__=="__main__":
    m=Message()
    print(m.create({"temp":"10"}))
    print(m.create({"temp":"20"}))
    print(m.create({"temp":"30"}))
    print(m.create({"temp":"40"}))

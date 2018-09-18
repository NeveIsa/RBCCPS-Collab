import datetime
import json

class Message:
    def __init__(self,msgtype="observation"):
        self.msgtype = msgtype
        self.messageID=1

    def pack(self,msg={}):
        msg["timestamp"]=datetime.datetime.now().isoformat()
        msg["type"]=self.msgtype
        msg["messageID"]=self.messageID

        self.messageID+=1

        finalmsg = {self.msgtype: msg}

        return finalmsg

    def unpack(self,msg):
        if self.msgtype in msg.keys():
            payload = msg[self.msgtype]
            return payload
        else:
            return False



if __name__=="__main__":
    m=Message()
    print(m.pack({"temp":"10"}))
    print(m.pack({"temp":"20"}))
    
    print(m.unpack(m.pack({"temp":"30"})))
    print(m.unpack(m.pack({"temp":"40"})))
 

import struct

import sys

if sys.version_info.major==2:
    print ("--> Only Python3 support available..."+"...from MBdatatypes.py | EXITING...")
    sys.exit(1)


class mbType16():
    """
    fmt :           H , h
    suffixes:       > , <
    (optional-default <)
    
    """

    def __init__(self,fmt,endian):
        self.fmt = fmt
        self.endian= endian
    def pack(self,value):
        assert type(value)==int
        if self.endian=='big':
                return struct.pack(">"+self.fmt,value)
        elif self.endian=='little':
                return struct.pack("<"+self.fmt,value)
    def unpack(self,value):
        if self.endian=='big':
                return struct.unpack(">"+self.fmt,value)
        elif self.endian=='little':
                return struct.unpack("<"+self.fmt,value)


class mbInt(mbType16):
    def __init__(self,endian="big"):
        super().__init__("H",endian)



class mbFloat():
    def __init__(self,wordEndian="big", byteEndian="big"):
        self.wordEndian=wordEndian
        self.byteEndian=byteEndian  

    def pack(self,value):
        if self.wordEndian==self.byteEndian:
            if self.wordEndian=="little":
                # aabb | ccdd -> ddcc | bbaa
                return struct.pack("<f",value)
            elif self.wordEndian=="big":
                # aabb | ccdd -> aabb | ccdd
                return struct.pack(">f",value)
        else:
            temp=[0,0,0,0]
            
            if self.wordEndian=="little":
                # byteEndian - big
                # aabb | ccdd -> ccdd | aabb
                orig=struct.pack("<f",value)
            
            elif self.wordEndian=="big":
                # byteEndian - little
                # aabb | ccdd - bbaa | ddcc
                orig=struct.pack(">f",value)

            temp[0]=orig[1]
            temp[1]=orig[0]
            temp[2]=orig[3]
            temp[3]=orig[2]
            tempBytes=map(lambda x: bytes((x,)),temp)
            tempBytes = list(tempBytes)
            return struct.pack("cccc",tempBytes[0],tempBytes[1],tempBytes[2],tempBytes[3])
    
    def unpack(self,blob):
        if self.wordEndian==self.byteEndian:
            blob = bytes(blob)
            if self.wordEndian=="big":
                # aabb|ccdd <- aabb|ccdd
                return struct.unpack(">f",blob)
            elif self.wordEndian=="little":
                # aabb|ccdd <- ddcc|bbaa
                return struct.unpack("<f",blob)
        
        else:
            newblob=[0,0,0,0]
            
            newblob[0]=blob[1]
            newblob[1]=blob[0]
            newblob[2]=blob[3]
            newblob[3]=blob[2]
            
            # blob -> aabb|ccdd, newblob -> bbaa|ddcc
            newblob = bytes(newblob)

            if self.wordEndian=="big":
                # byte endian is little
                # aabb|ccdd (newblob) <- bbaa|ddcc (blob)
                return struct.unpack(">f",newblob)
            elif self.wordEndian=="little":
                # byte endian is big
                # ddcc|bbaa (newblob) <- ccdd|aabb (blob)
                return struct.unpack("<f",newblob)
                



if __name__=="__main__":
    print("Checking mbInt with 4")
    print("big")
    mbi=mbInt("big")
    a=mbi.pack(4)
    print(a)
    print(mbi.unpack(a),"\n")

    print("Checking mbInt with 4")
    print("little")
    mbi=mbInt("little")
    a=mbi.pack(4)
    print(a)
    print(mbi.unpack(a),"\n")
    
    print("Checking mbFloat with 10.11")

    endian=("big","big")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    #for i in f:print (i)
    print(f)
    print (mbf.unpack(f),"\n")
    
    endian=("little","little")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    #for i in f:print (i)
    print(f)
    print (mbf.unpack(f),"\n")


    endian=("big","little")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    #for i in f:print (i)
    print(f)
    print (mbf.unpack(f),"\n")


    endian=("little","big")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    #for i in f:print (i)
    print(f)
    print (mbf.unpack(f),"\n")




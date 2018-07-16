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
            if self.wordEndian=="big":
                # aabb | ccdd -> ddcc | bbaa
                return struct.pack(">f",value)
            elif self.wordEndian=="little":
                # aabb | ccdd -> aabb | ccdd
                return struct.pack("<f",value)
        else:
            temp=[0,0,0,0]
            
            if self.wordEndian=="big":
                # byteEndian - little
                # aabb | ccdd -> ccdd | aabb
                orig=struct.pack(">f",value)
            
            elif self.wordEndian=="little":
                # byteEndian - big
                # aabb | ccdd - bbaa | ddcc
                orig=struct.pack("<f",value)

            temp[0]=orig[1]
            temp[1]=orig[0]
            temp[2]=orig[3]
            temp[3]=orig[2]
            tempBytes=map(lambda x: bytes((x,)),temp)
            tempBytes = list(tempBytes)
            return struct.pack("cccc",tempBytes[0],tempBytes[1],tempBytes[2],tempBytes[3])


if __name__=="__main__":
    print("Checking mbInt...")
    mbi=mbInt("big")
    a=mbi.pack(4)
    print(a)
    print(mbi.unpack(b'\x00\xff'))

    print("Checking mbFloat")

    endian=("big","big")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    for i in f:print (i)
    
    endian=("little","little")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    for i in f:print (i)


    endian=("big","little")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    for i in f:print (i)


    endian=("little","big")
    print("word,byte",endian)
    mbf=mbFloat(*endian)
    f=mbf.pack(10.11)
    for i in f:print (i)

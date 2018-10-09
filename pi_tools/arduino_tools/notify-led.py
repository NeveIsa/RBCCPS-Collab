from pyfirmata import Arduino, util
import serial

def getport():
    import serial.tools.list_ports
    for x in list(serial.tools.list_ports.comports()):
        print (x)

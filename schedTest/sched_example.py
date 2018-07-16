import sched
import time
import struct
now=time.time()

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print('EVENT:', time.time()-now, name)
    
'''def modbus_poll():
    print(client.connect())
    time.sleep(2)
    result= client.read_holding_registers(0x00,4,unit=0x01)
    #values=struct.unpack('>ffff',struct.pack('>HHHH',*result.registers))
    print(values)
    client.close()'''

if __name__=="__main__":
    print('START:', time.time())
    # client=ModbusClient(method = "rtu", timeout=1, port='/dev/ttyACM0',stopbits = 1, bytesize = 8, parity = 'N', baudrate = 9600)
    #scheduler.enter(3, 1, print_event, ('second',))
    #scheduler.run()
    while(True):
      #time.sleep(1)
      scheduler.enter(1,1,print_event, ('first',))
      scheduler.enter(1,1, print_event, ('second',)) # changed the execution time to 1 to check if its blocking
      now=time.time()
      print("before run",now)
      scheduler.run() #Infered that this blocks
      now=time.time()
      print("after run",now)
      exit()

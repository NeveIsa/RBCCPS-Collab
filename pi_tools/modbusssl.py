#import serial
import time
#import pymodbus
#from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient 
#from pymodbus.transaction import ModbusRtuFramer
#import sys
#import paho.mqtt.client as mqtt
#import msvcrt
#import getch
#import RPi.GPIO as GPIO

import sys
import select

import serial.tools.list_ports

portdetected = serial.tools.list_ports.comports()
print (portdetected)

portdetected = list(filter(lambda x: "USB" in x.name, portdetected))
print (portdetected)

if (len(portdetected)):
  portdetected= portdetected[0].device
  print ("Using port:",portdetected)
else:
  print("Serial port not found....Exiting")
  exit()


deviceID=2
#portdetected= "/dev/ttyACM0"

mbclient= ModbusClient(method = "rtu", timeout=1, port=portdetected, stopbits = 1, bytesize = 8, parity = 'N', baudrate = 19200)
connection = mbclient.connect()
print(connection)
time.sleep(3)

#ALL SENSOR DATA ARE IN INPUT REGISTERS

temp_adc_addr=3000
voltage_adc_addr=3001
current_adc_addr=3002
ldr_addr=3003

#CHIP TEMPERATURE IN HOLDING REGISTER
chip_temp_adc_adr=3000
brightness_reg_adr=2000
vlc_data_reg_ard=1000

#VLC ENABLE 
vlc_enable_addr=4001
lamp_enable_addr=4000


while (1):
    print("=====================================================================")
    result=mbclient.read_input_registers(temp_adc_addr, unit=deviceID)
    temp_adc=result.registers[0]
    temp=(temp_adc*75)/4096
    print("Temperature: "+str(round(temp,2))+"C. ADC value: "+str(temp_adc)+".")
    time.sleep(.1)
    result=mbclient.read_input_registers(voltage_adc_addr, unit=deviceID)
    voltage_adc=result.registers[0]
    voltage=(voltage_adc*15.18)/4096
    print("Voltage: "+str(round(voltage,2))+"V. ADC value: "+str(voltage_adc)+".")
    result=mbclient.read_input_registers(current_adc_addr, unit=deviceID)
    current_adc=result.registers[0]
    current=(current_adc*5.5)/4096
    print("Current: "+str(round(current,2))+"A. ADC value: "+str(current_adc)+".")
    result=mbclient.read_input_registers(ldr_addr, unit=deviceID)
    ldr=result.registers[0]
    print("LDR ADC value: "+str(ldr)+".")
    result=mbclient.read_holding_registers(chip_temp_adc_adr, unit=deviceID)
    chip_temp_adc=result.registers[0]
    chip_temp=(1475 - ((2475*chip_temp_adc)/4096))/10
    print("Chip Temperature: "+str(round(chip_temp,2))+"C. ADC value: "+str(chip_temp_adc)+".")
    if (sys.stdin in select.select([sys.stdin], [], [], 0)[0]):
        line=sys.stdin.readline()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        op=input("1 - Change brightness\n2 - Change VLC status\n3 - Change VLC data\nSelect option number: ")
        op=int(op)
        if op==1:
            br=input("Enter Brightness Value: ")
            br=int(br)
            # print(br)
            print(mbclient.write_register(brightness_reg_adr, br, unit=deviceID))
        elif op==2:
            vlcstaus=input("Enter 1 to enable VLC or 0 to disable vlc: ")
            vlc_en=1
            if int(vlcstaus)<1:
                vlc_en=0
            print(mbclient.write_register(vlc_enable_addr, vlc_en, unit=deviceID))

        elif op==3:
            vlcdata=input("Enter new VLC data string: ")
            arrdata=list(vlcdata)
            for i in range(len(arrdata)):
                intdata=int((ord(arrdata[i])))
                print(arrdata[i])
                mbclient.write_register(vlc_data_reg_ard+i, intdata, unit=deviceID)
            mbclient.write_register(vlc_data_reg_ard+i+1, 0, unit=deviceID)
        else:
            print("Invalid option!!")
        time.sleep(3)
        continue
    else:
        time.sleep(3)
        continue

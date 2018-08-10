#include <modbus.h>
#include <modbusDevice.h>
#include <modbusRegBank.h>
#include <modbusSlave.h>

/*
This example code shows a quick and dirty way to get an
arduino to talk to a modbus master device with a
device ID of 1 at 9600 baud.
*/

//Setup the brewtrollers register bank
//All of the data accumulated will be stored here
modbusDevice regBank;
//Create the modbus slave protocol handler
modbusSlave slave;

void setup()
{   

//Assign the modbus device ID.  
  regBank.setId(2);

/*
modbus registers follow the following format
00001-09999  Digital Outputs, A master device can read and write to these registers
10001-19999  Digital Inputs, A master device can only read the values from these registers
30001-39999  Analog Inputs, A master device can only read the values from these registers
40001-49999  Analog Outputs, A master device can read and write to these registers 

Analog values are 16 bit unsigned words stored with a range of 0-32767
Digital values are stored as bytes, a zero value is OFF and any nonzer value is ON

It is best to configure registers of like type into contiguous blocks.  this
allows for more efficient register lookup and and reduces the number of messages
required by the master to retrieve the data
*/



//Add Analog Output registers 40001-40020 to the register bank
  regBank.add(40001);  
  regBank.add(40002);  
  regBank.add(40003);  
  regBank.add(40004);  
  regBank.add(40005);  
  regBank.add(40006);  
  regBank.add(40007);  
  regBank.add(40008);  
  regBank.add(40009);  
  regBank.add(40010);  
  regBank.add(40011);  
  regBank.add(40012);  
  regBank.add(40013);  
  regBank.add(40014);  
  regBank.add(40015);  
  regBank.add(40016);  
  regBank.add(40017);  
  regBank.add(40018);  
  regBank.add(40019);  
  regBank.add(40020);  

/*
Assign the modbus device object to the protocol handler
This is where the protocol handler will look to read and write
register data.  Currently, a modbus slave protocol handler may
only have one device assigned to it.
*/
  slave._device = &regBank;  

// Initialize the serial port for coms at 9600 baud  
  slave.setBaud(19200);   
}

void loop()
{

  
 while(1)
  {
    //put a random number into registers 1, 10001, 30001 and 40001
    //regBank.set(1, 100);
    regBank.set(1, (byte) random(0, 2));
    regBank.set(10001, (byte) random(0, 2));
    //regBank.set(30001, (word) random(0, 32767));
    regBank.set(30001, (word)100);

    
    union xxx
    {
      float y;
      word z[2];
    };

    union xxx yyy;
    
    float t = 10.7;
    yyy.y = t;

    /*Serial.begin(115200);
    
    Serial.println(yyy.x[0],BIN);
    Serial.println(yyy.x[1],BIN);
    Serial.println(yyy.x[2],BIN);
    Serial.println(yyy.x[3],BIN);while(1);*/

   /* byte temp;
    temp=yyy.x[1];
    yyy.x[1] = yyy.x[0];
    yyy.x[0] = temp;

    //byte temp;
    temp=yyy.x[2];
    yyy.x[2] = yyy.x[3];
    yyy.x[3] = temp;*/
    
    regBank.set(40001, yyy.z[1] );
    regBank.set(40002, yyy.z[0] );


    double u= 12345.6789;

    union sss
    {
      double d;
      word w[2];
    }sss;

    sss.d=u;
    
    regBank.set(40003,sss.w[1]);
    regBank.set(40004,sss.w[0]);


    ///////////// IN ARDUINO 8BIT MCUS, DOUBLE = FLOAT
    

    //regBank.set(40001, (int16_t) -500 );
    //regBank.set(40002, (int16_t) -32123 );
    
     slave.run();  
  }
}

#include"config.h"

void setup(){
  Serial.begin(9600);
  int i;
  for (i=0;feedpin[i];i++)
  {
    if(connectiontype[i]== "zigbee" )
    {
       if(feedtype[i]=="sensor"){
          pinMode(feedpin[i],INPUT);
        }
       else{
          pinMode(feedpin[i],OUTPUT);
        }
    }
  }
}

void loop(){
  int b,j,i=0;
  String x,c,a,y;
  if (a=Serial.readStringUntil('*'))
  if (a.substring(0,8)=="Read pin")
  {
     c=a.substring(9,10);
     j=c.toInt();
     b=sensor_read(j);
     Serial.print(b);
    }
  else
  {
     if (a.substring(0,4)=="GPIO")
     //Serial.println (a);
     if (a.substring(7,9)=="ON")
     {
      x=a.substring(5,6);
      j=x.toInt();
      sensor_write(j,HIGH);
     }
     else if (a.substring(7,10)=="OFF")
     {
      x=a.substring(5,6);
      j=x.toInt();
      sensor_write(j,LOW);
     }
  }
     delay(2000);
  }

int sensor_read(int pin)
{
  int a ;
  a=digitalRead(pin);
  return a;
}

void sensor_write(int pin,int state)
{
  digitalWrite(pin,state);
}

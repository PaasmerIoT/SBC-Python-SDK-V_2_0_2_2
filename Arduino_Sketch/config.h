#define devicename "Zigbee" //your device name

#define timePeriod 2 //change the time delay as you required for sending sensor values to paasmer cloud

char feedname[][10]={"Feed1","Feed2","Feed3","feed4","feed5","feed6"};

String feedtype[]={"sensor","sensor","sensor","actuator","actuator","actuator"};

String connectiontype[]= {"GPIO","GPIO","zigbee","GPIO","GPIO","zigbee"};

int feedpin[]={2,4,5,6,32,8};



import os 
import argparse 
import fnmatch 

#struct thing to hold device info 
class DevicePair: 
  def _init_(self):
    self.boardName   = ''
    self.ftdiSerial  = ''
    self.devicePath  = ''
    self.ttyUSB      = []

    
# start of program 

Version = 'V1.0'

#setup argument parsing 
cmdParser = argparse.ArgumentParser(description='FTDI Device to TTYUSB Utility')
cmdParser.add_argument('-s','--serial', help='Board Serial Number', default="none")
cmdParser.add_argument('-i','--identifier', help='Prefix of the Product field to search for (Default = AMDA)', default="AMDA")

args = vars(cmdParser.parse_args())
boardSerial = args['serial']
identifier  = args['identifier']

devicesDirectory = []

# find directors that contain a file called serial 
for root, dirs, files in os.walk("/sys/devices"):
  for name in files:
    if (name == 'serial'):
      devicesDirectory.append(os.path.join(root))
 

devices = []

#look in all dirctories for the 'product' file 
#if found and it matches the identifier prefix, create a devicePair stuct to store product and serial info 
for names in devicesDirectory: 
  with open(os.path.join(names,'product')) as productFile: 
    for line in productFile: 
      if (fnmatch.fnmatch(line,(identifier.rstrip()+'*'))):
        dev = DevicePair()
        dev.boardName  = line
        dev.devicePath = names
        tty = []
        dev.ttyUSB = tty
        
        with open(os.path.join(names,'serial')) as serialFile:
          for line in serialFile:
            dev.ftdiSerial = line 
          
        serialFile.close()   
        devices.append(dev)
  productFile.close()
  
#find ttyUSB devices for each FTDI device found 
for devs in devices: 
  for root, dirs, files in os.walk(devs.devicePath): 
    for d in dirs: 
      if (fnmatch.fnmatch(d,'ttyUSB*')):
        if d not in devs.ttyUSB:
          devs.ttyUSB.append(d)

        
#print results 
for devs in devices: 
    print "---------------------------------------------------------------------------------"
    print ""
    if (devs.boardName.rstrip() == boardSerial.rstrip()) | (boardSerial == 'none'): 
      if (devs.ftdiSerial.rstrip() == '00'):
        print "ARM & NFP JTAG FTDI DEVICE"
        
      elif (devs.ftdiSerial.rstrip() == '01'):
        print "DUAL I2C FTDI DEVICE"
        
      elif (devs.ftdiSerial.rstrip() == '02'):
        print "JTAG, SPI, UART, AND GPIO FTDI DEVICE"
        
      else: 
        print "UNDEFINED DEVICE"
        
      print "Board Serial Number: " + devs.boardName.rstrip()
      print "FTDI Device  Number: " + devs.ftdiSerial.rstrip()
      print "Device Path        : " + devs.devicePath.rstrip() 
      print "ttyUSB Devices     : "
      for d in devs.ttyUSB:
        print "\t" + d
        
      print "\n"
  
print "Finished"

  
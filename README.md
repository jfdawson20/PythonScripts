PythonScripts
=============

Various python scripts 

tty2ftdi.py : script scans /sys/devices for all usb devices with a product file that matches the specified
              'identifier'. For each device found it displays the USB devices associated ttyUSBn ids if any.
              useful for determing which ttyUSB device is associated with a particular ftdi device 

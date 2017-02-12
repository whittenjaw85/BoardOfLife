import serial
import sys
import time

''' 
info: must use python 2.7 to run this script

dependencies: pyserial module, sys module (for checking python version)

'''
PORTNUM = "/dev/cu.wchusbserial1410"

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "(x:%d, y:%d)" % (self.x, self.y)
    
def run_script():
    
    #prepare serial port
    ser = serial.Serial()
    ser.port = PORTNUM
    ser.timeout = 1
    ser.baudrate = 9600
    
    ser.open()
    if ser.readable():
        #run for several thousand messages
        for i in range(5000):
            vals = ser.read(12) # read ten bytes
            
            if len(vals) < 2:
                time.sleep(1)
                continue
                
            #inspect for start bit
            while ord(vals[0]) != 0xaa:
                vals.pop(0)
                vals = vals + ser.read()
                print(vals)
        
        
            #decode message to values
            p1 = Point((ord(vals[1])<<8) + ord(vals[2]), \
                (ord(vals[3])<<8) + ord(vals[4]) )
        
            p2 = Point((ord(vals[5])<<8) + ord(vals[6]), \
                (ord(vals[7])<<8) + ord(vals[8]) )
                
            b1 = ord(vals[9])
            b2 = ord(vals[10])

            #print output
            print(p1)  
            print(p2)
            if b1 == 0:
                print("click1")
            if b2 == 0:
                print("click2")
        
    ser.close()
            
if __name__ == "__main__":
    assert sys.version_info[0] == 2
    run_script()
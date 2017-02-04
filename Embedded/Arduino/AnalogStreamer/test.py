import serial
import sys

''' 
info: must use python 2.7 to run this script

dependencies: pyserial module, sys module (for checking python version)

'''
PORTNUM = "COM23"

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
    ser.timeout = 0.1
    ser.baudrate = 9600
    
    ser.open()
    if ser.readable():
        #run for several thousand messages
        for i in range(5000):
            if ser.in_waiting > 10:
                vals = ser.port.read(10) # read ten bytes
            
                #inspect for start bit
                while int(vals[0]) != 0xaa:
                    vals.pop(0)
                    vals = vals + ser.read()
                
                
                #decode message to values
                p1 = Point((int(vals[1])<<8) + (int(vals[2])), \
                    (int(vals[3])<<8) + int(vals[4]) )
                
                p2 = Point((int(vals[5])<<8) + (int(vals[6])), \
                    (int(vals[7])<<8) + int(vals[8]) )

                #print output
                print(p1)
                print(p2)
        
        ser.close()
            
if __name__ == "__main__":
    assert sys.version_info[0] == 2
    run_script()
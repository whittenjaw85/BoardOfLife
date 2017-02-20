import serial
import time
import struct
import _thread as thread, queue, time

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(x:%d, y:%d)" % (self.x, self.y)
        
DEFAULTPORT = "/dev/cu.wchusbserial1420"
class SerialManager(object):
    def __init__(self, qInst, port=DEFAULTPORT):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.timeout = 1
        self.ser.baudrate = 9600
        self.kill = False
        #self.q = queue.Queue()
        self.q = qInst
        print(self.ser) 
        
    def workerFunction(self):
        try:
            print("Opening serial port")
            self.ser.open()
            time.sleep(1)
            
        except Exception:
            print(Exception)
            
        while self.kill == False:
            #read the port data into the queue for processing
            if self.ser.in_waiting > 12:
                vals = self.ser.read(12) # read datapoints
                #print(vals)
            else:
                time.sleep(0.1)
                continue
            
            #ensure that start bit is 0xaa
            while vals[0] != 170:
                vals = vals[1:] + self.ser.read()
            
            #package into meaningful data
            #decode message to values
            print(vals)
            data = struct.unpack(">xhhhh??x", vals)
            #print(data)
            
            p1 = Point((data[0]-512)*150/512, (data[1]-512)*150/512)
        
            p2 = Point((data[2]-512)*150/512, (data[3]-512)*150/512)
                
            b1 = data[4]
            b2 = data[5]
            
            #notify the listener by adding queue
            self.q.put([p1, p2, b1, b2])
            
        try:
            print("closing serial port")
            self.ser.close()
        except Exception:
            print(Exception)
            
    def killThread(self):
        self.kill = True
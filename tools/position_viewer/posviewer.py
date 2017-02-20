'''
Author: Jonathan Whitten
Date: 10FEB2017
Description: Program displays the x-y coordinates of two point inputs
'''
import tkinter as tk
import serialmanager as serman
import _thread as thread, queue, time

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def offset(self, x, y):
        self.x += x
        self.y += y

    def __str__(self):
        return "(x:%d, y:%d)" % (self.x, self.y)

class PositionViewer(object):
    def __init__(self, parent, qInst):
        
        self.parent = parent
        self.q = qInst #queue variable
        
        #draw points locations
        self.p = dict()
        
        self.p['zeroleft'] = Point(150, 150)
        self.p['zeroright'] = Point(450, 150)
        self.p['left'] = Point(0,0)
        self.p['right'] = Point(0,0)
        self.p['button1'] = False
        self.p['button2'] = False
        
        #setup the viewer
        self.canvas = tk.Canvas(self.parent, width = 600, height=480)
        self.canvas.pack()
        
        self.refresh()
        
    def update_points(self):
        '''
        Takes a Point object and updates it to the new point position.
        Does not redraw the scene.
        '''
        try:
            data = self.q.get(block=False)
            self.p["right"] = data[0]
            self.p["left"] = data[1]
            self.p["button2"] = data[2]
            self.p["button1"] = data[3]
        except queue.Empty:
            pass
            #print('no data')
        
    
    def refresh(self):
        #print("updating screen")
        self.update_points()
        self.canvas.delete('all')
        self.draw_background()
        self.draw_content()
        self.parent.after(5, self.refresh)
        
    def draw_background(self):
        self.draw_circles()
        
    def draw_circles(self):
        if self.p['button1'] == True:
            self.canvas.create_oval(0, 0, 300, 300, outline="gray", fill='')
        else:
            self.canvas.create_oval(0, 0, 300, 300, outline="gray", fill='pink')
        
        if self.p['button2'] == True:    
            self.canvas.create_oval(300, 0, 600, 300, outline='gray', fill='')
        else:
            self.canvas.create_oval(300, 0, 600, 300, outline='gray', fill='pink')
            
        
    def draw_content(self):
        self.draw_crosshatch(Point(self.p['left'].x + self.p['zeroleft'].x, 
            self.p['left'].y + self.p['zeroleft'].y))
        self.draw_crosshatch(Point(self.p['right'].x + self.p['zeroright'].x, 
            self.p['right'].y + self.p['zeroright'].y))
        #self.draw_crosshatch(self.p['right'])
        
    def draw_crosshatch(self, point):
        #initialize the drawing points
        h1 = Point(point.x - 10, point.y)
        h2 = Point(point.x + 10, point.y)
        v1 = Point(point.x, point.y + 10)
        v2 = Point(point.x, point.y - 10)
        
        #draw the points on the canvas
        self.canvas.create_line(h1.x, h1.y, h2.x, h2.y, fill='red')
        self.canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill='red')
        
if __name__ == "__main__":
    
    q = queue.Queue()
    
    #start main window
    root = tk.Tk()
    
    #create viewer
    pv = PositionViewer(root, q)
    sm = serman.SerialManager(q)
    thread.start_new_thread(sm.workerFunction, ())
    
    #start program
    root.mainloop()
        
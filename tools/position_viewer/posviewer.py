'''
Author: Jonathan Whitten
Date: 10FEB2017
Description: Program displays the x-y coordinates of two point inputs
'''
import tkinter as tk

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(x:%d, y:%d)" % (self.x, self.y)

class PositionViewer(object):
    def __init__(self, parent):
        
        self.parent = parent
        
        #draw points locations
        self.p = dict()
        self.p['left'] = Point(150, 150)
        self.p['right'] = Point(450, 150)
        
        #setup the viewer
        self.canvas = tk.Canvas(self.parent, width = 600, height=480)
        self.canvas.pack()
        
    def update_point(self, select, point):
        '''
        Takes a Point object and updates it to the new point position.
        Does not redraw the scene.
        '''
        if select in self.p.keys():
            self.p[select] = point
    
    def refresh(self):
        self.canvas.delete('all')
        self.draw_background()
        self.draw_content()
        
    def draw_background(self):
        self.draw_circles()
        
    def draw_circles(self):
        self.canvas.create_oval(0, 0, 300, 300, outline="gray")
        self.canvas.create_oval(300, 0, 600, 300, outline='gray')
        
    def draw_content(self):
        self.draw_crosshatch(self.p['left'])
        self.draw_crosshatch(self.p['right'])
        
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
    #start main window
    root = tk.Tk()
    
    #create viewer
    pv = PositionViewer(root)
    pv.refresh()
    
    #start program
    root.mainloop()
        
#contains class User, which has User, and User functions 

from tkinter import *   
import random 


class User(object):

    def __init__(self, data):
        
        #initialize a center and radius for drawing the teddy bear 
        
        self.xdisplace = 0 
        self.ydisplace = 0 
        self.radius = min(data.width / 20, data.height / 20) 
        self.xc = (random.randint(self.radius, data.width - self.radius)) 
        self.yc = (random.randint(self.radius, data.height - self.radius))  
        self.x = self.xc + self.xdisplace 
        self.y = self.yc + self.ydisplace
        data.UsersCenters.append((self.x, self.y))  
        
        
    def verticalMoveBy(self, moveBy, data): 
    
        #move y by this much amount if you press up or down 
    
        self.ydisplace += moveBy 
        if self.yc + self.ydisplace + (2 * self.radius) > data.height: 
            self.ydisplace -= moveBy  
            
        if self.yc + self.ydisplace - self.radius < 0: 
            self.ydisplace -= moveBy 
        
    
    def horizontalMoveBy(self, moveBy, data): 
    
        #move x by this much amount if you press left or right  
    
        self.xdisplace += moveBy 
        if self.xc + self.xdisplace + self.radius > data.width: 
            self.xdisplace -= moveBy 
            
        if self.xc + self.xdisplace - self.radius < 0: 
            self.xdisplace -= moveBy  
        
        
    def cameraMoveBy(self, data): 
    
        #use the camera to find the center of the object you are tracking and then 
        #set the instances center to that 
        
        if self.Found: 
             
            data.sheight, data.swidth = data.frame.shape[:2] 
            
            x, y = self.center 
            
            ratiox = (data.swidth - x)/(data.swidth) 
            
            ratioy = (y)/(data.sheight) 
            
            self.x = (ratiox * data.width) 
            self.y = (ratioy * data.height) 
            
            
        else: 
             
            self.x = self.x 
            self.y = self.y 
            
    def setEqual(self): 
    
        self.x = self.xc + self.xdisplace 
        self.y = self.yc + self.ydisplace 
        
    def draw(self, canvas):
        #got this function and associated drawing functions from a 15112 lab assignment I did 
        faceMove = self.radius
        noseMove = self.radius/2
        snoseMove = self.radius/5 
        arcMove = snoseMove
        eyeMove = self.radius/2
        widthSet = self.radius/10 
        noseSet = self.radius / 4 
        
        # draw overall face 
        canvas.create_oval(self.x - faceMove, self.y - faceMove, self.x 
        + faceMove, self.y + faceMove, fill = "gray", width = widthSet) 
        
        # draw snout 
        
        canvas.create_oval(self.x - noseMove, self.y - noseMove + noseSet, self.x 
        + noseMove, self.y +  noseMove + noseSet, fill = "tan", width = 
        widthSet)  
        
        # draw the nose 
        canvas.create_oval(self.x - snoseMove, self.y - snoseMove, self.x + 
        snoseMove, 
        self.y + snoseMove, fill = "black") 
        
        # draw the eyes 
        canvas.create_oval(self.x - snoseMove - eyeMove, self.y - snoseMove - 
        eyeMove,
        self.x + snoseMove - eyeMove, self.y + snoseMove - eyeMove, fill = "black") 
        #draw the eys 
        canvas.create_oval(self.x - snoseMove + eyeMove, self.y - snoseMove - 
        eyeMove,
        self.x + snoseMove + eyeMove, self.y + snoseMove - eyeMove, fill = "black") 
    
        # call teddyarc help cause arcs are hella lines 
        self.drawUserHelp(canvas) 
    

    def drawUserHelp(self, canvas): 
        
        faceMove = self.radius 
        noseMove = self.radius/2
        snoseMove = self.radius/5 
        arcMove = snoseMove 
        eyeMove = self.radius/2
        arcDisplace = self.radius / 2.5 
        widthSet = self.radius / 18 
        mini = arcMove/1.5
        arcSet = 1.5 * arcMove 
        
        
        #made four arcs to construct the mouth 
        
        canvas.create_arc(self.x - arcSet, self.y - mini + arcDisplace
        , self.x, self.y + mini + arcDisplace,style = ARC, fill = "black", 
        start = 180, width = widthSet) 
        
        canvas.create_arc(self.x - arcSet , self.y - mini + arcDisplace, self.x, 
        self.y + mini + arcDisplace, style = ARC, fill = "black", 
        start = 270, width = widthSet) 
        
        canvas.create_arc(self.x, self.y - mini +  arcDisplace, self.x + arcSet, 
        self.y + mini + arcDisplace, style = ARC, fill = "black", 
        start = 180, width = widthSet) 
        
        canvas.create_arc(self.x, self.y - mini + arcDisplace, self.x + arcSet, 
        self.y + mini + arcDisplace, style = ARC, fill = "black", 
        start = 270, width = widthSet) 
         
        
        
        
        
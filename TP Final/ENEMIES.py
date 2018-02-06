#Contains class Enemy and associated functions 

from tkinter import * 
import random
import math  



class Enemy(object): 

    def __init__(self, data, rand):
        
        self.position = random.randint(1, 4)
        self.radius = min(data.width / 20, data.height / 20) 
    
        #randomizes from 1 through 4, which decides whether the enemy appears from bottom, top, left, or right 
    
        if self.position == 1: 
            
            self.initHelpTop(data)
            
        if self.position == 2:
            self.initHelpBottom(data) 
            
        if self.position == 3:
            self.initHelpRight(data)
              
        if self.position == 4:
            self.initHelpLeft(data)  
        
        self.xdisplace = 0 
        self.ydisplace = 0 
        
        self.x = self.xc + self.xdisplace 
        self.y = self.yc + self.ydisplace 
        self.color = "brown" 
        
            
    def initHelpTop(self, data):
        
        self.xc = random.randint(self.radius, data.width - self.radius) 
        self.yc = random.randint(-data.height/10, 0)
        self.ydirection = 1 
        #starts at top, goes bottom 
   
    def initHelpBottom(self, data): 
        self.xc = random.randint(self.radius, data.width - self.radius) 
        self.yc = random.randint(data.height, data.height + data.height / 10) 
        self.ydirection = -1 
        #starts at bottom, goes top 
        
    def initHelpRight(self, data):
        self.xdirection = -1 
        self.xc = random.randint(data.width, data.width + data.width/10) 
        self.yc = random.randint(self.radius, data.height - self.radius) 
    
    def initHelpLeft(self, data):
        self.xdirection = 1 
        self.xc = random.randint(- data.width/10, 0) 
        self.yc = random.randint(self.radius, data.height - self.radius) 
        
         
    def timeMove(self, data, moveBy):
             
        #move over time in your direction and by a predetermined move amount 
        if self.position == 1:
            self.ydisplace += self.ydirection * moveBy 
        
        if self.position == 2: 
            self.ydisplace += self.ydirection * moveBy 
        
        if self.position == 3: 

            self.xdisplace += self.xdirection * moveBy 
        
        if self.position == 4: 

            self.xdisplace += self.xdirection * moveBy 
  
    def draw(self, canvas): 
    
        #got this and associated draw functions from a lab assignment I did for 15112 

        self.x = self.xc + self.xdisplace 
        self.y = self.yc + self.ydisplace 
    
        faceMove = self.radius
        noseMove = self.radius/2
        snoseMove = self.radius/5 
        arcMove = snoseMove
        eyeMove = self.radius/2
        widthSet = self.radius/10 
        noseSet = self.radius / 4 
        
        # draw overall face 
        canvas.create_oval(self.x - faceMove, self.y - faceMove, self.x 
        + faceMove, self.y + faceMove, fill = self.color, width = widthSet) 
        
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
        self.drawEnemyHelp(canvas) 
    

    def drawEnemyHelp(self, canvas): 
        
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
        

 
        
#class RecurseEnemy(Enemy): 

    #def __init__(self, data) 
    
    

    
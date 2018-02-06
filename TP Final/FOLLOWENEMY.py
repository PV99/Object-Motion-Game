#contains class followEnemy, which inherits from class Enemy, but comes with associated functions 

from tkinter import * 
import random
import math  
from ENEMIES import Enemy 

class followEnemy(Enemy): 
    
    def __init__(self, data, rand):
        
        super().__init__(data, rand)
        self.color = "Green" 
        
        if data.Survived < 10:  #timer for the instance to disappear 
            self.timer = 250
            
        else: 
            self.timer = data.Survived * 25 
            
 
    def timeMove(self, data, moveBy):
        
        try: #find the angle between the user and the instance, then use that angle 
        #to guide the direction of the followEnemy to follow 
        
            minDist = (data.width ** 2 + data.height ** 2) ** 2 
            
            for hero in data.UserBase:
                for element in hero: 
                
                    x, y = element.x, element.y  
                    dist = ((x - self.x) ** 2)  + ((y - self.y) ** 2) 
                    if dist < minDist: 
                        minDist = dist 
                        ux, uy = x, y 
            
            angle = math.atan2(uy - self.y, ux - self.x) 
            self.ydisplace += math.sin(angle) * moveBy 
            self.xdisplace += math.cos(angle) * moveBy 

        except:
            
            pass
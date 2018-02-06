#This file is the base file, it executes all the code 

###################################

#Copied framework for integrating tkinter and opencv from Vasu Agrawal, TA 
#for CMU CS, course 15112. 

####################################
# customize these functions
####################################

import time
import sys
from USER import User 
from ENEMIES import Enemy
from FOLLOWENEMY import followEnemy   
import numpy as np
import math,random, cv2, time, copy, string  
from SF import *
from CV import * 

# Tkinter selector
if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as tk
else:
    from tkinter import *
    from tkinter import ttk 
    import tkinter as tk
    
from Buttons import *
from PIL import Image, ImageTk   



    
def init(data):

    data.Survived = 0 #counts the number you've survived 
    data.EnemyGenerate = 0 #a timer to track when to generate enemies
    #use will become apparent in timerFired 
    data.mode = "Beginning" #initial mode 
    data.Enemies = [] #keeps track of all instances of Enemy Class 
    rand = random.randint(1, 3) #if 1, then create a Follower Enemy Class 
    data.Enemies.append(followEnemy(data, rand))
    #in the beginning make a follow enemy  
    
    data.Users = [] 
    data.UsersCenters = [] 
      
    data.vMoveBy = data.height/20  #the amount you - the user move by, seen in user class later on 
    data.hMoveBy = data.width/20   #The vertical and horizontal amounts ^ 
    data.numPlayers = None         #at the moment, no players 
    data.validNum = False          #used to decide if user entry for number of players is valid 
    data.defined = False 
    
    #data.Play = "camera" 
    # data.FastMotionDetection = cv2.createBackgroundSubtractorMOG2()
    beginningButtons(data) #initialize the beginning buttons 
    data.frameChoice = 1    #initalize the frame you play in the beginning 
    data.UserBase = []      #similar to data.Users, but you can manipulate this list whereas you don't want to with
                            #data.Users 

def mainMenu(data): 

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
        
    init(data)

def initPlay(data):
    
    for userNum in range(data.numPlayers): 
            
        data.Users.append(User(data))
        
        #once you click the play button, and enter a number in the entry widget(tk), create that number of users  
        
        
    for item in data.Users: 
        item.FirstCenter = False #initialize the first center to be false, necessary for drawing over frame 
        item.Found = False #initialize to False, necessary for drawing over frame 
        item.FirstFastMotion = 1 #used to decide 
        item.shape = "circle"
        item.live = True 
        #initialize the shape you draw on the item to a circle 
    
    data.secondDelay = 250 
    
    #countdown for mode - "second". In this mode you will ready yourself for playing the game 
    data.mode = "SetHSV" 
    data.frameChoice = 1
    
    hsvButtonDestroy(data) #forget all the buttons you created for this mode and make new ones  

def keyPressed(event, data):
    if event.keysym == "q":
        data.root.destroy()
        #common control in OPEN CV community, if you press q stop the program 
    
    if data.mode == "Beginning":
        
        if event.keysym == "Return":
            #after you click the play button,
            # you get an entry. When you click enter, this grabs the value in the entry
            #and returns it.
            returned = data.Entry.get() 
            returned = returned.strip() 
            if returned in string.digits: 
            
                data.numPlayers = int(returned) 
                data.validNum = True 
                #if its a valid entry, then you alter a bool variable to True to represent that 
            else: 
                data.validNum = False 
                data.numPlayers = "Invalid Input" 
            
            if data.validNum: #then go to next mode, forget all the buttons you currently have
                for item in range(len(data.Buttons)):
                    data.Buttons[item].grid_forget()
                    
                buttons = [] 
                initPlay(data)
        
    
    if data.mode == "Middle": 
        if event.keysym == "Up":  #manual controls if your open cv isn't working
            for item in data.Users: 
                item.verticalMoveBy(-1 * data.vMoveBy, data) 
                
        if event.keysym == "Down": 
            for item in data.Users: 
                item.verticalMoveBy(data.vMoveBy, data) 
                
        if event.keysym == "Right": 
            for item in data.Users: 
                item.horizontalMoveBy(data.hMoveBy, data) 
                
        if event.keysym == "Left": 
            for item in data.Users: 
                item.horizontalMoveBy( -1 * data.hMoveBy, data) 
                
        for item in data.Users: 
            item.setEqual() 

def timerFired(data):
    
    if data.mode == "Second": #in second mode, once this ticker hits zero you go to middle mode 
        data.secondDelay -= 1
        
        if data.secondDelay == 0: 
            data.mode = "Middle"
            middleMode(data) 
            
    
    if data.mode == "Middle": 
         
        data.EnemyGenerate += 1 #once you reach a certain value, add a new enemy 
        
        if data.EnemyGenerate == 70:
            rand = random.randint(1, 3) 
            if rand == 1: 
                data.Enemies.append(followEnemy(data, rand)) 
            else: 
                data.Enemies.append(Enemy(data, rand)) 
            data.EnemyGenerate = 0 
            
            
            
        for item in data.Enemies: #set a timer for the following Enemies because 
            #if they follow you forever you will die pretty quickly 
            if type(item) == followEnemy:
                item.timer -= 1 
                
                if item.timer == 0:
                    
                    data.Enemies.remove(item) 
                    data.Survived += 1
                 
            item.timeMove(data, min(data.width/175, data.height/175)) 
            
                
        if not data.mode == "Pause": #during pause mode you don't wanna check for collisions
            checkCollision(data)
        
        checkBounds(data) 
        
        if len(data.Enemies) > 10: #don't let enemy length get to big or else it's not fair for you  
        
            data.Enemies.pop(0) 
            data.Survived += 1 
            
def cameraFired(data):
    """Called whenever new camera frames are available.
    Camera frame is available in data.frame. You could, for example, blur the
    image, and then store that back in data. Then, in drawCamera, draw the
    blurred frame (or choose not to).
    """

    
    if data.mode == "Middle" or data.mode == "Second" or data.mode == "Pause":
        

        modifyFrame(data) #get a mask 
        erodeAndFastTrack(data) #erode the mask, create a fastmotion frame 
        findMovements(data) #find contours which give you the center for your object 
        makeCircle(data) #draw a shape based on your object 
        
        for list in data.UserBase: 
            for item in list: 
                item.cameraMoveBy(data)#move each user 
        
    if data.mode == "SetHSV":  
        
        try:  
            modifyFrame(data) #refer to comments in previous part of this function 
            erodeAndFastTrack(data) 
            findMovements(data)
            makeCircle(data)
        
        except: 
         
            pass 
    
   
def checkBounds(data):  
        
    for item in data.Enemies: 
    
        #check if Enemies are out of bounds, if they are, make a new enemy that is randomly located 
    
        rand = random.randint(1, 3) 
    
        if item.position == 1: 
            if ((item.x + item.radius) < 0) or ((item.x - item.radius) > 
            data.width) or((item.y - item.radius) > data.height): 
                data.Enemies.remove(item) 
                data.Survived += 1 
                data.Enemies.append(Enemy(data, rand)) 
                
                
        if item.position == 2: 
            if ((item.x + item.radius) < 0) or ((item.x - item.radius)
             > data.width) or ((item.y + item.radius) < 0): 
                
                data.Enemies.remove(item) 
                data.Survived += 1 
                data.Enemies.append(Enemy(data, rand)) 
            
            
        if item.position == 3: 
            if ((item.x + item.radius) < 0) or ((item.y - item.radius) > 
            data.height) or ((item.y + item.radius) < 0): 
            
                data.Enemies.remove(item) 
                data.Survived += 1 
                data.Enemies.append(Enemy(data, rand)) 
        
        if item.position == 4: 
            if ((item.x - item.radius) > data.width) or ((item.y - item.radius)> 
            data.height) or (( item.y + item.radius )< 0): 
            
                data.Enemies.remove(item) 
                data.Survived += 1 
                data.Enemies.append(Enemy(data, rand)) 
         
def checkCollision(data): 

    for enemyItem in data.Enemies: 
        for hero in data.UserBase: 
            for userItem in hero:
                #for every enemy and every user, check if there is a collision by 
                #seeing if the distance between their centers is less than their radiuses added together 
                currentGapx = userItem.x - enemyItem.x 
                currentGapy = userItem.y - enemyItem.y 
                currentGap = math.sqrt(currentGapx ** 2 + currentGapy ** 2) 
                minGap = userItem.radius + enemyItem.radius 
        
                if currentGap <= minGap:
                    userItem.live = False 
                    hero.remove(userItem) #if collided, then remove a hero, and increase the amount you survived 
                    #cause you also kill an enemy when you collide with them 
                    data.Enemies.remove(enemyItem) 
                    data.Survived += 1 
                    
                    bool2 = False 
                    for baseList in data.UserBase: 
                        if len(baseList) > 0: 
                            bool2 = True 
                            
                    #if there's more than one instance of a user in a UserBase, 
                    #pause the game, if not, end the game 
                    
                    if bool2: 
                        pause(data)
                        
                    
                    bool = True 
                    for baseList in data.UserBase: 
                        if len(baseList) > 0: 
                            bool = False 
                        
                    if bool:
                        data.mode = "End"
                        end(data) 
        
        for enemyItem2 in data.Enemies: 
        
            #check if enemies collide with each other 
        
            if enemyItem != enemyItem2: 
                currentGapx = enemyItem2.x - enemyItem.x 
                currentGapy = enemyItem2.y - enemyItem.y 
                currentGap = math.sqrt(currentGapx ** 2 + currentGapy ** 2) 
                minGap = enemyItem2.radius + enemyItem.radius 
                
                if currentGap <= minGap:
                    if type(enemyItem2) == type(enemyItem):  
                        data.Enemies.remove(enemyItem) 
                        data.Survived += 1 
                    else: 
                        if type(enemyItem2) == followEnemy: 
                            data.Enemies.remove(enemyItem) 
                            data.Survived += 1 
                        else: 
                            data.Enemies.remove(enemyItem2) 
                            data.Survived += 1 
        
def drawCamera(canvas, data, center = None):
    
    if center == None: #place the center to draw on at the right hand side of the 
        #canvas 
        center =(data.width * 3/2, data.height/2)
    
    #choose the frame you want to pass through 
    if data.frameChoice == 1: 
        frame = data.frame 
    
    if data.frameChoice == 2: 
        frame = data.Users[data.currPlayer].mask 
        
    if data.frameChoice == 3: 
        frame = data.Users[data.currPlayer].FastMotion 
    
    #get an image then put it in canvas 
    data.tk_image = opencvToTk(frame, data)
    canvas.create_image(center, image=data.tk_image)
    
def opencvToTk(frame, data):
    """Convert an opencv image to a tkinter image, to display in canvas."""
    #resize your frame to the size you need for the canvas 
    frame = cv2.resize(frame, (data.width, data.height)) 
    if data.frameChoice == 1:
        #if you're passing through a color image, convert it from BGR to RGB, if 
        #its grey convert it from gray to RGB 
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        
    #use pillow to extract an RGB image and format it in a suitable way 
    pil_img = Image.fromarray(rgb_image)
    
    #use tk's builtin function to convert a pillow imagei into a TK image 
    
    tk_image = ImageTk.PhotoImage(image=pil_img)
    
    return tk_image

    
def drawBeginning(canvas, data): 
    
    #draw the beginning texts 
    canvas.create_text(data.width/2, data.height/3  
    , text ="Run Teddy Bear Game", fill = "black", font = 
    "Times 15 bold italic", anchor = N)
    
    canvas.create_text(data.width/2, data.height / 2  
    , text ="Press on play and enter in the # of players", fill = "black", font = 
    "Times 15 bold italic") 
    
    if data.numPlayers == None: 
        canvas.create_text(data.width/2, 2 * data.height / 3, 
        text = "Enter the number of players", fill = "black", font = 
        "Times 15 bold italic", anchor = S) 
    
    else: 
        if data.numPlayers == "Invalid Input": 
            canvas.create_text(data.width/2, 2 * data.height / 3, 
            text = ("Number of Players: " + str(data.numPlayers)), fill = "black", 
            font = "Times 15 bold italic", anchor = S) 
    #draw the image on the screen 
    drawCamera(canvas, data)
   
def drawHSV(canvas, data): 

    drawCamera(canvas, data, (data.width * 3/2, data.height/2))

def drawSecond(canvas, data): 
     
    #draw each user  
    for hero in data.UserBase:
        for subhero in hero: 
            subhero.draw(canvas)
        
    canvas.create_text(data.width/2, data.height / 2, 
    text = "Time Remaining Till Game Starts: " + str(data.secondDelay//25), 
    fill = "black", font = "Times 15 bold italic") 
    
    drawCamera(canvas, data)
    
def drawPause(canvas, data):
    
    canvas.create_text(data.width/2, data.height / 2, 
    text = "If a player collided please remove their object", 
    fill = "black", font = "Times 15 bold italic") 
    
    status = (str(data.currPlayer) + ": Alive - " +  str(data.Users[data.currPlayer].live))
    
    canvas.create_text(data.width/2, data.height/4 * 3, text = status, fill = "black", font = "Times 15 bold italic") 
    
    #draw enemies and user 
    
    for item in data.Enemies: 
        item.draw(canvas) 
        
    for hero in data.UserBase:
        for subhero in hero: 
            subhero.draw(canvas)
    
    drawCamera(canvas, data) 
    
def drawMiddle(canvas, data): 

    #draw enemies and user 
 
    canvas.create_text(data.width/2, data.height/4, text = 
        "Teddy Bears Survived: " + str(data.Survived), fill="darkblue", 
        font="Times 15 italic bold", anchor = N) 
        
    canvas.create_text(data.width/2, data.height/4, text = 
        "Current Number of Teddy Bears " + str(len(data.Enemies)), 
        fill="darkblue", font ="Times 15 italic bold", anchor = S) 

    for item in data.Enemies: 
        item.draw(canvas) 
        
    for hero in data.UserBase:
        for subhero in hero: 
            subhero.draw(canvas)
        
    drawCamera(canvas, data)
     
        
def drawEnd(canvas, data): 
    

    canvas.create_text(data.width/2, data.height/4, text = "You Lose", 
    fill="darkblue", font="Times 15 italic bold", anchor = N) 
        
    canvas.create_text(data.width/2, data.height/2, text =  
    "Teddy Bears Survived: " + str(data.Survived), 
    fill="darkblue", font="Times 15 italic bold", anchor = N) 
        
     
    
def redrawAll(canvas, data):
    
    if data.mode == "Beginning": 
        
        drawBeginning(canvas, data) 
        
    if data.mode == "SetHSV": 
        drawHSV(canvas, data)
    
        
    if data.mode == "Second": 
    
        drawSecond(canvas, data) 
        
    if data.mode == "Pause": 
        drawPause(canvas, data)
    
    
    if data.mode == "Middle": 
        drawMiddle(canvas, data) 
        
            
    if data.mode == "End": 
        drawEnd(canvas, data) 


def run(width, height):

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    
    data.camera_index = 0
    data.timer_delay = 10 # ms
    data.redraw_delay = 50 # ms
   
    # Initialize the webcams
    camera = cv2.VideoCapture(data.camera_index)
    data.camera = camera

    # Make tkinter window and canvas
    data.root = Tk()
    data.root.title('Run Teddy')
    #make a frame for your buttons in tkinter 
    data.optionsFrame = Frame(data.root, width = int(data.width * 2.2), height =
    data.height, bg = "dim grey", padx = 5, pady = 5)
    
    #make your frame a grid 
    data.optionsFrame.grid(row = 1, sticky="ew")

    canvas = Canvas(data.root, width=data.width * 2, height=data.height, bg = "dim gray")
    #make your canvas a grid 
    canvas.grid(row = 0, sticky = "n") 
    
    # data.optionsFrame2 = Frame(data.root, width = data.width * 2, height =
    # data.height, bg = "blue", padx = 5, pady = 5)
    # 
    # data.optionsFrame.grid(row = 2, sticky="ew")

    init(data)
   
    # Basic bindings. Note that only timer events will redraw.
    data.root.bind("<Key>", lambda event: keyPressed(event, data))

    # Timer fired needs a wrapper. This is for periodic events.
    def timerFiredWrapper(data):
        # Ensuring that the code runs at roughly the right periodicity
        start = time.time()
        timerFired(data)
        end = time.time()
        diff_ms = (end - start) * 1000
        delay = int(max(data.timer_delay - diff_ms, 0))
        data.root.after(delay, lambda: timerFiredWrapper(data))

    # Wait a timer delay before beginning, to allow everything else to
    # initialize first.
    data.root.after(data.timer_delay, 
        lambda: timerFiredWrapper(data))
 

    def redrawAllWrapper(canvas, data):
        start = time.time()

        # Get the camera frame and get it processed.
        _, data.frame = data.camera.read()
        cameraFired(data)
        
        # Redrawing code
        canvas.delete(ALL)
        redrawAll(canvas, data)

        # Calculate delay accordingly
        end = time.time()
        diff_ms = (end - start) * 1000

        # Have at least a 5ms delay between redraw. Ideally higher is better.
        delay = int(max(data.redraw_delay - diff_ms, 5))

        data.root.after(delay, lambda: redrawAllWrapper(canvas, data))

    # Start drawing immediately
    data.root.after(0, lambda: redrawAllWrapper(canvas, data))

    # Loop tkinter
    data.root.mainloop()

    # Once the loop is done, release the camera.
    print("Releasing camera!")
    data.camera.release()

if __name__ == "__main__":
        
    run(420, 420)

 

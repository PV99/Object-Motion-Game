#this file contains all the buttons for the UI, and associated functions for pressing the buttons 
import sys
import random 

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as tk
else:
    from tkinter import *
    from tkinter import ttk 
    import tkinter as tk
    
from USER import User 
from ENEMIES import Enemy
from FOLLOWENEMY import followEnemy   
     
def configStyle(data): 
    
    #got layout for style from http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-style-layer.html
    
    styleName = "TButton"
    
    ttk.Style().configure(styleName, padx = 8, pady = 8, relief="flat",
    background="#000")

    return styleName 
    
def beginningButtons(data):
    
    #create a pressPlay button and grid it  

    data.Buttons = []

    playButton(data) 
    
    data.Buttons.append(data.playButton) 

    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 1, column = item, sticky = 'ew')
    
def playButton(data): 


    styleName = configStyle(data) 
    
    data.playButton = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Play", command = lambda: playMode(data), style = styleName) 
        

def playMode(data): 

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
         
    data.Buttons = []
    
    stylename = configStyle(data)
    
    data.Entry = ttk.Entry(data.optionsFrame, width = 
    int(data.width/50), text = "# of Players", style = stylename ) 
    
    data.Entry.insert(0, '# of Players')
    
    data.Buttons.append(data.Entry) 

        #make an entry button, if the entry is valid (function in tkinter base), then
        #move on 

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
        
    
def hsvButtonDestroy(data):
        
    styleName = configStyle(data)
    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
        
    #forget all your prev buttons, make a bunch of new buttons with new commands 
     
    data.setHSVEntry = ttk.Entry(data.optionsFrame, width = 
    int(data.width/50), style = styleName) 
    
    data.setHSVEntry.insert(0, 'Player #')
    
    data.setHSVEntry.grid(column = 0) 
    
    data.ButtonSet = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Set HSV", command = lambda: setHSV(data), style = styleName) 
    
    data.ButtonTennis = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Tennis", command = lambda: tennis(data), style = styleName) 
    
    data.ButtonView = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "View Player", command = lambda: setView(data), style = styleName)
    
    data.ButtonCopy= ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Copy", command = lambda: copy(data), style = styleName)
    
    data.ButtonCF= ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Change Frame", command = lambda: changeFrame(data), style = styleName)
    
    data.ButtonShape = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Shape", command = lambda: changeShape(data), style = styleName)
    
    
    data.ButtonMove = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Play", command = lambda: secondMode(data), style = styleName)
    
    data.Buttons.append(data.ButtonView) 
    data.Buttons.append(data.ButtonSet) 
    data.Buttons.append(data.ButtonCopy) 
    data.Buttons.append(data.ButtonTennis) 
    data.Buttons.append(data.ButtonCF) 
    data.Buttons.append(data.ButtonShape) 
    data.Buttons.append(data.ButtonMove) 

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
        
    hsvGridScale(data) 
    
def hsvGridScale(data): 

    #for every item, give it 8 scales 
    for item in range(len(data.Users)): 
        
        data.Users[item].hmin = Scale(data.optionsFrame, from_=0, to_= 255, 
        orient = HORIZONTAL, label = "Hue Min") 
        data.Users[item].hmax = Scale(data.optionsFrame, from_=0, to_= 255,
        orient = HORIZONTAL, label = "Hue Max")   
        data.Users[item].smin = Scale(data.optionsFrame, from_=0, to_= 255, 
        orient = HORIZONTAL, label = "Sat Min") 
        data.Users[item].smax = Scale(data.optionsFrame, from_=0, to_= 255,
        orient = HORIZONTAL, label = "Sat Max") 
        data.Users[item].vmin = Scale(data.optionsFrame, from_=0, to_= 255, 
        orient = HORIZONTAL, label = "Val Min") 
        data.Users[item].vmax = Scale(data.optionsFrame, from_=0, to_= 255,
        orient = HORIZONTAL, label = "Val Max") 
        data.Users[item].radmin = Scale(data.optionsFrame, from_=0, to_= 150,
        orient = HORIZONTAL, label = "Radius Min") 
        data.Users[item].NF = Scale(data.optionsFrame, from_=0, to_= 5, 
        orient = HORIZONTAL, label = "Noise Filter") 
        data.Users[item].scaleShow = False
        
        data.Users[item].sett = False 
        
        #preset the values associated with the scales 
        data.Users[item].hminv = 0 
        data.Users[item].hmaxv = 0 
        
        data.Users[item].sminv = 0
        data.Users[item].smaxv = 0 
        
        data.Users[item].vminv = 0 
        
        data.Users[item].vmaxv = 0 
        
        data.Users[item].minRad =70 
        
        data.Users[item].noiseFilter = 2
        
def secondMode(data): 

    #remove any and all buttons, remove all scales, then grid the buttons ones from the player you currently called 
    try: 
        for usert in data.Users: 
            if usert.sett == False: 
                print(1/0) 
        
        for index in range(len(data.Users)): 
            if data.Users[index].scaleShow == True: 
                data.Users[index].hmin.grid_remove() 
                data.Users[index].hmax.grid_remove() 
                data.Users[index].smin.grid_remove()  
                data.Users[index].smax.grid_remove() 
                data.Users[index].vmin.grid_remove() 
                data.Users[index].vmax.grid_remove()
                data.Users[index].radmin.grid_remove() 
                data.Users[index].NF.grid_remove() 
                data.Users[index].scaleShow = False  
    
        for item in range(len(data.Buttons)):
            data.Buttons[item].grid_forget()
            
        data.Buttons = [] 
        
        styleName = configStyle(data)
    
        data.mode = "Second" 
        
        data.ButtonSkip = ttk.Button(data.optionsFrame, width = int(data.width/50), 
        text = "Ready", command = lambda: skip(data), style = styleName)
        
        data.Buttons.append(data.ButtonSkip) 
        
        for item in range(len(data.Buttons)):
            data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
    
    except: 
        
        data.setHSVEntry.insert(0, "set all players first") 
    
        
def changeShape(data): 
    #function associated with shapes 
    try: 
    
        if data.Users[data.currPlayer].shape == "circle": 
            data.Users[data.currPlayer].shape = "square"
            
        else: 
            data.Users[data.currPlayer].shape = "circle" 
            
    except: 
        
        data.setHSVEntry.insert(0, "View First") 
        
def skip(data): 

    #if user presses this button, skip to middle 
    data.mode = "Middle"
    
    middleMode(data)
    
    
def changeFrame(data): 

    #if user presses this button, move onto nextFrame option 
    #three options - motion sensing, mask, and colored frame 
    
    currFrame = data.frameChoice 

    if currFrame == 2: 
        data.frameChoice = 1
        
        
    if currFrame == 1:  
        data.frameChoice = 3 
        pass
        
    if currFrame == 3: 
        data.frameChoice = 2
        pass  
    
    
def copy(data): 

    #copy one users mask attributes to another 

    try: 
        type(data.currPlayer) 
        
        
        value = data.setHSVEntry.get() 
        value = value.strip() 
        try: 
             
            x, y = value.split("copy") 
            x, y = int(x), int(y) 
            data.Users[x-1].hmin.set(data.Users[y-1].hmin.get()) 
            data.Users[x-1].hmax.set(data.Users[y-1].hmax.get()) 
            data.Users[x-1].smin.set(data.Users[y-1].smin.get()) 
            data.Users[x-1].smax.set(data.Users[y-1].smax.get()) 
            data.Users[x-1].vmin.set(data.Users[y-1].vmin.get()) 
            data.Users[x-1].vmax.set(data.Users[y-1].vmax.get()) 
            data.Users[x-1].radmin.set(data.Users[y-1].radmin.get())
            data.Users[x-1].NF.set(data.Users[y-1].NF.get()) 
             
            
        except: 
        
            data.setHSVEntry.insert(0, "Invalid Input") 
        
    except:
        
        data.setHSVEntry.insert(0, "View First") 
        
def tennis(data): 

    #set the mask attributes to satisfy a tennis ball 

    try: 
        type(data.currPlayer) 
        
        data.Users[data.currPlayer].hmin.set(29) 
        data.Users[data.currPlayer].hmax.set(81) 
        data.Users[data.currPlayer].smin.set(65) 
        data.Users[data.currPlayer].smax.set(255) 
        data.Users[data.currPlayer].vmin.set(21) 
        data.Users[data.currPlayer].vmax.set(255) 
        data.Users[data.currPlayer].radmin.set(70) 
        data.Users[data.currPlayer].NF.set(2) 
         
    except: 
    
        data.setHSVEntry.insert(0, "View First") 
    
def setHSV(data):
    
    try: 
        type(data.currPlayer) 
        
        try: 
            
            
            value = data.setHSVEntry.get() 
            
            if not int(value) == data.currPlayer + 1: 
                print(1/0)
                
            
            
            try: 
            

                t = int(value)
                
                if t > len(data.Users) or t < 1:
                    print(1/0) 
                    
                hmin(data, t)
                hmax(data, t)
                smin(data, t)
                smax(data, t)
                vmin(data, t)
                vmax(data, t)
                noise(data, t) 
                rad(data, t)
                
                data.frameChoice = 2 
                #set frameChoice to mask 
                
                getUserDB(data)
                #make a another list with instances of users, but organized in 
                #a special way 
                
                
            except: 
                data.setHSVEntry.insert(0, "Invalid Number") 
                
        except: 
            
            data.setHSVEntry.insert(0, "View Player First") 
            
    except: 
        data.setHSVEntry.insert(0, "View First") 
        
def getUserDB(data): 

    data.UserBase = [] 

    for index in range(len(data.Users)): 
    
        if data.Users[index].sett: 
            count, forNowList = copies(data, index) 
            temp = [] 
            for i in range(count): 
                temp.append(data.Users[forNowList[i]])
             
            if temp not in data.UserBase: 
                data.UserBase.append(temp) 
                
    #in a list with instances of classes, if certain instances share the same attributes, 
    #pack them into a subList, which is contained under a headerList which has all the instances.
    #this accounts for same colored Balls because the algorithm for dealing with these is different 

def copies(data, index): 
    
    if data.Users[index].live: 
        count = 1 
        forNowList = [index] 
    else: 
        count = 0 
        forNowList = [] 
    #if they share a bunch of attributes, add to a temporary list and add to the count, which is used 
    #to exectue stuff in parent functon 
    for index2 in range(len(data.Users)): 
        if (index != index2) and (data.Users[index2].sett): 
            if data.Users[index].hminv == data.Users[index2].hminv:
                if data.Users[index].hmaxv == data.Users[index2].hmaxv:  
                    if data.Users[index].vminv == data.Users[index2].vminv:
                        if data.Users[index].vmaxv == data.Users[index2].vmaxv:
                            if data.Users[index].sminv == data.Users[index2].sminv: 
                                if data.Users[index].smaxv  == data.Users[index2].smaxv: 
                                    if data.Users[index].minRad == data.Users[index2].minRad: 
                                        if data.Users[index].noiseFilter == data.Users[index2].noiseFilter: 
                                            if data.Users[index2].live: 
                                                count += 1 
                                                forNowList.append(index2) 
                                                forNowList.sort() 
    return count, forNowList 
    

def setView(data):
    
    item = data.setHSVEntry.get() 
    try: 
        
        t = int(item)
        if t > len(data.Users) or t < 1:
            print(1/0) 
            
        #remove all the previous grids and pull up your shiz 
        for index in range(len(data.Users)): 
            if data.Users[index].scaleShow == True: 
                data.Users[index].hmin.grid_remove() 
                data.Users[index].hmax.grid_remove() 
                data.Users[index].smin.grid_remove()  
                data.Users[index].smax.grid_remove() 
                data.Users[index].vmin.grid_remove() 
                data.Users[index].vmax.grid_remove()
                data.Users[index].radmin.grid_remove() 
                data.Users[index].NF.grid_remove() 
                data.Users[index].scaleShow = False  
        
        
        #grid the scales for the user in your entry, and set that user to the current user 
        item = int(item) - 1 
        data.Users[item].scaleShow = True 
        
        data.Users[item].hmin.grid(sticky = "ew", row = 1, column = 0, columnspan = 2) 
        
        data.Users[item].hmax.grid(sticky = "ew", row = 1, column = 2, columnspan = 2) 
        
        data.Users[item].smin.grid(sticky = "ew", row = 2, column = 0, columnspan = 2) 
        
        data.Users[item].smax.grid(sticky = "ew", row = 2, column = 2, columnspan = 2)    
        
        data.Users[item].vmin.grid(sticky = "ew", row = 3, column = 0, columnspan = 2) 
        
        data.Users[item].vmax.grid(sticky = "ew", row = 3, column = 2, columnspan = 2) 
            
        data.Users[item].radmin.grid(sticky = "ew", row = 4, column = 0, columnspan = 2)
        
        data.Users[item].NF.grid(sticky = "ew", row = 4, column = 2, columnspan = 2) 
        
        data.currPlayer = item 
        
        data.Users[item].sett = True
        
         
        
    except: 
        data.setHSVEntry.insert(0, "Invalid Number") 
    
        

        
def hmin(data, value): 

    data.Users[value - 1].hminv = data.Users[value - 1].hmin.get() 
     

def hmax(data, value): 

    data.Users[value - 1].hmaxv = data.Users[value - 1].hmax.get() 
    
def smin(data, value): 

    data.Users[value - 1].sminv = data.Users[value - 1].smin.get() 
     

def smax(data, value): 

    data.Users[value - 1].smaxv = data.Users[value - 1].smax.get() 
    
def vmin(data, value): 

    data.Users[value - 1].vminv = data.Users[value - 1].vmin.get() 
     
def vmax(data, value): 

    data.Users[value - 1].vmaxv = data.Users[value - 1].vmax.get() 
    
def rad(data, value): 
    data.Users[value - 1].minRad = data.Users[value - 1].radmin.get() 
    
def noise(data, value): 

    data.Users[value - 1].noiseFilter = data.Users[value - 1].NF.get() 

def middleMode(data): 

    for index in range(len(data.Users)): 
        if data.Users[index].scaleShow == True: 
            data.Users[index].hmin.grid_remove() 
            data.Users[index].hmax.grid_remove() 
            data.Users[index].smin.grid_remove()  
            data.Users[index].smax.grid_remove() 
            data.Users[index].vmin.grid_remove() 
            data.Users[index].vmax.grid_remove()
            data.Users[index].radmin.grid_remove() 
            data.Users[index].NF.grid_remove() 
            data.Users[index].scaleShow = False  

    for item in range(len(data.Buttons)):
        
        data.Buttons[item].grid_forget()
        
    data.setHSVEntry.grid_forget() 
        
    data.Buttons = [] 
    
    styleName = configStyle(data)
    
    data.ButtonPause = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Pause", command = lambda: pause(data), style = styleName)
    
    data.Buttons.append(data.ButtonPause)
    
    #add a pause button, which when called, pulls up all your separate options 
    #in the pause() function 
    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
    
def pause(data): 

    data.mode = "Pause"

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
        
    data.Buttons = [] 
    
    styleName = configStyle(data)
    
    data.setHSVEntry = ttk.Entry(data.optionsFrame, width = 
    int(data.width/50), style = styleName) 
    
    data.setHSVEntry.insert(0, 'Player #')
    
    data.ButtonSet = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Set HSV", command = lambda: setHSV(data), style = styleName) 
    
    data.ButtonTennis = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Tennis", command = lambda: tennis(data), style = styleName) 
    
    data.ButtonView = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "View Player", command = lambda: setView(data), style = styleName)
    
    data.ButtonCopy= ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Copy", command = lambda: copy(data), style = styleName)
    
    data.ButtonShape = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Shape", command = lambda: changeShape(data), style = styleName)
    
    data.ButtonCF= ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Change Frame", command = lambda: changeFrame(data), style = styleName)
    
    
    
    data.ButtonBack = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Play", command = lambda: skip(data), style = styleName)
    
    data.Buttons.append(data.setHSVEntry) 
    data.Buttons.append(data.ButtonView) 
    data.Buttons.append(data.ButtonSet) 
    data.Buttons.append(data.ButtonCopy) 
    data.Buttons.append(data.ButtonTennis) 
    data.Buttons.append(data.ButtonCF) 
    data.Buttons.append(data.ButtonShape) 
    data.Buttons.append(data.ButtonBack)
    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
    
def end(data): 

    #add a replay button if you die 

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
        
    data.Buttons = [] 
    
    styleName = configStyle(data)
    
    data.ButtonReplay = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Replay", command = lambda: replay(data), style = styleName) 
    data.ButtonMainMenu = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Main Menu", command = lambda: mainMenu(data), style = styleName) 
    
    data.Buttons.append(data.ButtonReplay) 
    data.Buttons.append(data.ButtonMainMenu) 
    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
        
def replay(data): 

    #if the replay button is pressed, reinitialize certain data so that you can play again 
    for item in data.Users: 
        item.live = True 
    
    getUserDB(data)
    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
        
    data.Buttons = [] 
    data.secondDelay = 250 
    data.mode = "Second" 
    
    styleName = configStyle(data)
    
    data.ButtonSkip = ttk.Button(data.optionsFrame, width = int(data.width/50), 
    text = "Ready", command = lambda: skip(data), style = styleName)
    
    
    
    data.Buttons.append(data.ButtonSkip) 
    
    
    for item in range(len(data.Buttons)):
        data.Buttons[item].grid(row = 0, column = item, sticky = 'ew')
        
    replayinit(data)
    
def replayinit(data): 
    
    data.Survived = 0 #counts the number you've survived 
    data.EnemyGenerate = 0 #a timer to track when to generate enemies
    data.Enemies = [] #keeps track of all instances of Enemy Class 
    rand = random.randint(1, 3) #if 1, then create a Follower Enemy Class 
     
def mainMenu(data): 

    for item in range(len(data.Buttons)):
        data.Buttons[item].grid_forget()
        
    init(data)
    
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

        
    

    

    
    
    
    
    

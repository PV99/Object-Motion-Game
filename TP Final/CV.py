#contains all the Open CV code - where all the OPEN CV Magic happens 
#functions directly pulled from OPEN CV Documentation 
import numpy as np
import cv2
import time
import math
import copy 
import random 
  

def diffImg(t0, t1, t2): 
    #Recieved code for the diffImg function from the following link... 
    #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
    
    d1 = cv2.absdiff(t2, t1)
    
    d2 = cv2.absdiff(t1, t0)
    
    return cv2.bitwise_and(d1, d2)
    
def modifyFrame(data):
    
    frame = data.frame 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert the frame into the HSV color space 
    
    #recieved code for the following 3 lines from the following link, 
    #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/

    for index in range(len(data.Users)): 
        
        data.Users[index].lower = (data.Users[index].hminv, data.Users[index].sminv,  
        data.Users[index].vminv)
        data.Users[index].upper = (data.Users[index].hmaxv, data.Users[index].smaxv,  
        data.Users[index].vmaxv)
        
        #for every instance of user create a lower and upper range of HSV values to use to filter for mask 
        
        mask = cv2.inRange(hsv, data.Users[index].lower, data.Users[index].upper) 
    
        res = cv2.bitwise_and(frame, frame, mask = mask) 

        mask = cv2.medianBlur(mask, 5)
         
        data.Users[index].mask = mask 
    
def erodeAndFastTrack(data): 

    kernel = np.ones((5,5),np.uint8)
    
    for item in range(len(data.Users)): 
   
        data.Users[item].mask = cv2.erode(data.Users[item].mask, kernel, 
        iterations=data.Users[item].noiseFilter)
        data.Users[item].mask = cv2.dilate(data.Users[item].mask, kernel, 
        iterations=data.Users[item].noiseFilter)
        
        #erode and dilate the mask you created for each user 
        
        if data.frameChoice == 3: 
            
            if data.Users[item].sett: 
            #recieved logic for the following 3 lines from the following link, 
            #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
                 
                data.Users[item].t_minus = data.Users[item].t 
                data.Users[item].t = data.Users[item].t_plus
                data.Users[item].t_plus = data.Users[item].mask
               
                FastMotion = diffImg(data.Users[item].t_minus, data.Users[item].t, data.Users[item].t_plus) 
                data.Users[item].FastMotion = cv2.erode(FastMotion, kernel, iterations=data.Users[item].noiseFilter)
                
                continue 
                
            #recieved logic for the following 3 lines from the following link, 
            #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
            
        if data.Users[item].FirstFastMotion == 1: 
            data.Users[item].t_minus = data.Users[item].mask
            data.Users[item].t = data.Users[item].mask
            data.Users[item].t_plus = data.Users[item].mask
        
            FastMotion = diffImg(data.Users[item].t_minus, data.Users[item].t, data.Users[item].t_plus) 
            data.Users[item].FastMotion = cv2.erode(FastMotion, kernel, iterations=data.Users[item].noiseFilter)
            data.Users[item].FastMotion = cv2.dilate(FastMotion, kernel, iterations=data.Users[item].noiseFilter)
            data.Users[item].FirstFastMotion += 1
            #only execute this code once, after that you don't need to execute it anymore 
            
def findMovements(data): 

    # data.FastMotion = data.FastMotionDetection.apply(data.mask) 
    # data.FastMotion = cv2.erode(data.mask, kernel, iterations=8) 
    
    for item in data.UserBase:
        
        if len(item) > 0: 
        
            goon, contours, hierarchy = (cv2.findContours
            (item[0].mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
        
            #find contours of objects of the same color from mask of one object  

            if len(contours) >= len(item): 
                    
                counter = 0 
            
                #find the contours of that object 
                for cnt in contours: 
                    if counter >= len(item): 
                        
                        break 
                    #find the min enclosing circle and rectangle 
                    (x,y),radius = cv2.minEnclosingCircle(cnt)
                    square = cv2.minAreaRect(cnt)
                    minBox = cv2.boxPoints(square)
                    minBox = np.int0(minBox)
                    radius = int(radius)
                    if radius > item[counter].minRad:
                        
                        #if the radius of min enclosing circle is great enough 
                        #find Movements of your contour     
                        Movements = cv2.moments(cnt)
                        cx = int(Movements["m10"] / Movements["m00"])
                        cy = int(Movements["m01"] / Movements["m00"])
                        if findUserCloseTo(item,counter, cx, cy): 
                            try: 
                                item[counter].Found = False 
                            except: 
                                pass 
                                
                        else: 
                        
                            #if your object is not right next to a previously identified object of the same color, 
                            #set your obejcts radius and such
                            item[counter].boxus = minBox 
                            item[counter].rad = radius 
                            item[counter].center = (cx, cy)
                            item[counter].Found = True
                        
                            if item[counter].FirstCenter == False: 
                                item[counter].FirstCenter = True 
                            counter += 1   
                        
                
                    else: 
                        item[counter].Found = False 
                        
            else: 
                for hero in item: 
                    hero.Found = False 
                         
                        
        else: 
            continue 
        
def findUserCloseTo(item, counter, cx, cy): 

    for object in range(counter): 
        #checks if the suggested center value is right next to an already identified user. If so, this contour is 
        #from an already identified object 
         
        if item[object].FirstCenter: 
            currX, currY = item[object].center 
            distX = abs(currX - cx)  
            distY = abs(currY - cy) 
            if (distX + distY) < 2 * (item[object].rad): 
                        
                    return True 
        
    return False 
    
         
def makeCircle(data): 
    #if your item was Found, draw a circle or square to enclose it on the frame 
    try: 
        for hero in data.UserBase:
            for subhero in hero: 
                if subhero.FirstCenter:
                    if subhero.Found:  
                        if subhero.shape == "circle": 
                             
                            cv2.circle(data.frame, (subhero.center), subhero.rad,(85,122,195),2)
                            cv2.circle(data.frame, subhero.center, 5, (0, 0, 255), -1)
                            
                        else: 
                            cv2.drawContours(data.frame, [subhero.boxus], 0,(194,82,16),2)
 
    except: 
        pass 
        
 
                         
 

# def diffImg(t0, t1, t2): 
#   #Recieved code for the diffImg function from the following link... 
#   #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#   #
#   d1 = cv2.absdiff(t2, t1)
# 
#   d2 = cv2.absdiff(t1, t0)
#   
#    
#   return cv2.bitwise_and(d1, d2)
#  
#  
# def findFrame(data):
# 
#     frame = data.frame
#     mask = modifyFrame(frame) 
#     
#     
#     try: 
#         
#         
#         data.Found = True 
#         center, mask, FastMotion, frame = erodeAndFastTrack(mask, frame, 
#         data)
#                 
#                 #print("data.center =" + str(data.center)) 
#                 #print("data.prevcenter =" + str(data.prevcenter)) 
#         
#     except: 
#         
#         data.Found = False
#         FastMotion = erodeAndFastTrack(mask, frame, data) 
#         
#         
#      
#     
#     data.frame = frame
#     data.mask = mask 
#     data.FastMotion = FastMotion 
# 
#     
#     
# def modifyFrame(frame): 
# 
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
#     
#     #recieved code for the following 3 lines from the following link, 
#     #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
# 
# 
#     
#     lowergreen = np.array([29,86,70]) 
#     uppergreen = np.array([64, 255, 255]) 
#     
#     mask = cv2.inRange(hsv, lowergreen, uppergreen) 
#     
#     res = cv2.bitwise_and(frame, frame, mask = mask) 
#     
#     
#     mask = cv2.medianBlur(mask,5)
#     
#      
#     return mask
#         
#     
#     
# def erodeAndFastTrack(mask, frame, data): 
#     
#     kernel = np.ones((5,5),np.uint8)
#     
#     
#     mask = cv2.erode(mask, kernel, iterations=2)
#     mask = cv2.dilate(mask, kernel, iterations=2)
#     
#     if data.t_minus == None: 
#         #recieved code for the following 3 lines from the following link, 
#         #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#         data.t_minus = mask 
#         data.t = mask 
#         data.t_plus = mask
#       
#     
#     else: 
#         #recieved code for the following 3 lines from the following link, 
#         #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#         data.t_minus = data.t
#         data.t = data.t_plus
#         data.t_plus = mask 
#         
#     
#     
#     FastMotion = diffImg(data.t_minus, data.t, data.t_plus) 
#      
#     FastMotion = cv2.erode(FastMotion, kernel, iterations=1)
#      
#      
#     
#     image, contours, hierarchy = (cv2.findContours
#     (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
#      
#     imageFM, contoursFM, hierarchyFM = (cv2.findContours
#     (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
#     
#     
#     # if len(contours) > 0: 
#     #     c = max(contours, key=cv2.contourArea)
#     #     (x,y),maxRadius = cv2.minEnclosingCircle(c)
#     if len(contours) > 0:
#         maxRadius = 0 
#         for cnt in contours: 
#             (x,y),radius = cv2.minEnclosingCircle(cnt)
#             radius = int(radius)
#             if radius > maxRadius: 
#                 maxRadius = radius 
#                 maxcnt = cnt 
#                 
#         Movements = cv2.moments(maxcnt)
#         cx = int(Movements["m10"] / Movements["m00"])
#         cy = int(Movements["m01"] / Movements["m00"])
#         center = (cx, cy) 
#     
#         if not data.FirstCenter:
#             data.center = center
#             data.prevCenter = center  
#             data.FirstCenter = True
#             
#         data.center = center 
#      
#      
#     
#     if contours == []: 
#         
#         
#         return FastMotion 
#     
#     else: 
# 
#             maxRadius = int(maxRadius) 
#             frame = makeCircle(mask,
#             frame, contours, contoursFM, data, center, maxRadius) 
#         
#         
#             return center, mask, FastMotion, frame
#             
#     
#     
# def makeCircle(mask, frame, contours, contoursFM, data, center, maxRadius): 
#     
#     listx = [] 
#     listy = [] 
#     
#    
#     if len(contoursFM) >= 0: 
#          
#         data.prevCenter = data.center 
#         data.FM = True 
#         cv2.circle(frame, (center), maxRadius,(0,255,0),2)
#         cv2.circle(frame, center, 5, (0, 0, 255), -1)
#                 
#                
#             
#         return frame
#         
#     else: 
#     
#         if data.FirstCenter: 
#             
#             data.center = data.prevCenter 
#             
#             print("howdy") 
#             
#             data.FM = False 
#             #print("Found contours, but not movements, center should equal previous value") 
#             
#             cv2.circle(frame, (data.center), maxRadius,(0,255,0),2)
#             cv2.circle(frame, data.center, 5, (0, 0, 255), -1)
#     
#     return frame  
# 
'''
def diffImg(t0, t1, t2): 
  #Recieved code for the diffImg function from the following link... 
  #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
  #
  d1 = cv2.absdiff(t2, t1)

  d2 = cv2.absdiff(t1, t0)
  
   
  return cv2.bitwise_and(d1, d2)
 
 
def findFrame(data):

    frame = data.frame
    mask = modifyFrame(frame) 
    
    
    try: 
        
        
        data.Found = True 
        center, mask, FastMotion, frame = erodeAndFastTrack(mask, frame, 
        data)
        
        if data.FirstCenter == True:
            if data.FM: 
                data.prevCenter = data.center 
                print("data.center =" + str(data.center)) 
                print("data.prevcenter =" + str(data.prevcenter)) 
            else: 
                data.center = data.prevCenter 
                print("Found contours, but no movements") 
                print("data.center =" + str(data.center)) 
                print("data.prevcenter =" + str(data.prevcenter)) 
            
        data.center = center
            
        if data.FirstCenter == False:
            data.FirstCenter = True
            data.prevCenter = data.center
        
          
        
    except: 
        
        data.Found = False
        FastMotion = erodeAndFastTrack(mask, frame, data) 
        
        if data.FirstCenter: 
            data.Center = data.prevCenter 
         
         
    
    data.frame = frame
    data.mask = mask 
    data.FastMotion = FastMotion 
    
    
def modifyFrame(frame): 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    #recieved code for the following 3 lines from the following link, 
    #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/


    
    lowergreen = np.array([40,70,70]) 
    uppergreen = np.array([80, 200, 200]) 
    
    mask = cv2.inRange(hsv, lowergreen, uppergreen) 
    
    res = cv2.bitwise_and(frame, frame, mask = mask) 
    
    
    mask = cv2.medianBlur(mask,5)
    
     
    return mask
        
    
    
def erodeAndFastTrack(mask, frame, data): 
    
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    
    
    if data.t_minus == None: 
        #recieved code for the following 3 lines from the following link, 
        #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
        data.t_minus = mask 
        data.t = mask 
        data.t_plus = mask
      
    
    else: 
        #recieved code for the following 3 lines from the following link, 
        #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
        data.t_minus = data.t
        data.t = data.t_plus
        data.t_plus = mask 
        
    
    
    FastMotion = diffImg(data.t_minus, data.t, data.t_plus) 
    #FastMotion = FastMotionDetection.apply(mask) 
    FastMotion = cv2.erode(FastMotion,kernel,iterations = 5)
    
    
      
    
    image, contours, hierarchy = (cv2.findContours
    (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
     
    imageFM, contoursFM, hierarchyFM = (cv2.findContours
    (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
    
    center = None 
    #got following 5 lines from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), maxRadius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
     
    
    if contours == []: 
        
        
        return FastMotion
    
    else: 

            maxRadius = int(maxRadius) 
            frame = makeCircle(mask,
            frame, contours, contoursFM, data, center, maxRadius) 
        
        
            return center, mask, FastMotion, frame
            
    
    
def makeCircle(mask, frame, contours, contoursFM, data, center, maxRadius): 
    
    listx = [] 
    listy = [] 
    
   
    if len(contoursFM) >= 8: 
        
        data.FM = True 
        cv2.circle(frame, (center), maxRadius,(0,255,0),2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
               
            
        return frame
        
    else: 
    
        if data.FirstCenter: 
        
            data.FM = False 
            print("Found contours, but not movements, center should equal previous value") 
            
            cv2.circle(frame, (data.center), maxRadius,(0,255,0),2)
            cv2.circle(frame, data.center, 5, (0, 0, 255), -1)
    
    return frame  
    
cap = cv2.VideoCapture(0) 
while True: 
    
    _, frame = cap.Read() 
    
    findFrame(frame) 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
 
cap.release()
cv2.destroyAllWindows()
'''

# 
# class OpenCV(object): 
# 
#     def diffImg(self, t0, t1, t2): 
#         #Recieved code for the diffImg function from the following link... 
#         #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#         #
#         d1 = cv2.absdiff(t2, t1)
#         
#         d2 = cv2.absdiff(t1, t0)
#         
#         return cv2.bitwise_and(d1, d2)
#  
#  
#     def __init__(self): 
#         self.cap = cv2.VideoCapture(0) 
#         #FastMotionDetection = cv2.createBackgroundSubtractorMOG2() 
#         self.FirstCenter = False 
#         self.t_minus = None 
#         self.t = None 
#         self.t_plus = None
#           
#     
#     def findCircle(self): 
# 
#         #Capture frame-by-frame
#         ret, frame = self.cap.read()
#         
#             
#         mask = self.modifyFrame(frame) 
#         
#         try: 
#         
#             if self.FirstCenter == True:
#                 self.prevCenter = self.center 
#         
#             center, mask, FastMotion, frame = self.erodeAndFastTrack(mask, frame)
#             self.Found = True 
#             
#             if self.FirstCenter == False:
#                 self.FirstCenter = True
#                 self.prevCenter = center
#                 
#             self.center = center 
#             print(self.center, self.prevCenter)
#                 
#         except: 
#             
#             FastMotion = self.erodeAndFastTrack(mask, frame)
#             self.Found = False  
#                 
#                 
#          
#              
#     
#         # cv2.namedWindow('frame',cv2.WINDOW_FULLSCREEN) 
#         # cv2.imshow("frame", frame) 
#         # cv2.namedWindow('mask',cv2.WINDOW_NORMAL) 
#         # cv2.imshow("mask", mask) 
#         # cv2.namedWindow('FastMotion',cv2.WINDOW_NORMAL) 
#         # cv2.imshow("FastMotion", FastMotion) 
# 
#         
#     
#             
#             
#     def modifyFrame(self, frame): 
#     
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
#         
#         #recieved code for the following 3 lines from the following link, 
#         #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#     
#     
#         
#         lowergreen = np.array([35,85,85]) 
#         uppergreen = np.array([92, 230, 230]) 
#         
#         mask = cv2.inRange(hsv, lowergreen, uppergreen) 
#         
#         res = cv2.bitwise_and(frame, frame, mask = mask) 
#         
#         
#         mask = cv2.medianBlur(mask,5)
#         
#         return mask
#             
#         
#         
#     def erodeAndFastTrack(self, mask, frame): 
#         
#         kernel = np.ones((5,5),np.uint8)
#         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#         
#         
#         
#         if self.t_minus == None: 
#             #recieved code for the following 3 lines from the following link, 
#             #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#             self.t_minus = mask 
#             self.t = mask 
#             self.t_plus = mask 
#             
#         
#         else: 
#             #recieved code for the following 3 lines from the following link, 
#             #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
#             self.t_minus = self.t
#             self.t = self.t_plus
#             self.t_plus = mask 
#         
#         FastMotion = self.diffImg(self.t_minus, self.t, self.t_plus) 
#         #FastMotion = FastMotionDetection.apply(mask) 
#         FastMotion = cv2.erode(FastMotion,kernel,iterations = 2)
#         
#         mask = cv2.dilate(mask, kernel, iterations = 3) 
#         
#         image, contours, hierarchy = ( 
#         cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)) 
#         
#         imageFM, contoursFM, hierarchyFM = (cv2.findContours
#         (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
#         
#         
#         
#         if contours == [] and contoursFM == []: 
#             
#             
#             return FastMotion
#         
#         else: 
#             
#             try: 
#             
#                 center, mask, frame = self.makeCircle(mask,
#                 frame, contours, contoursFM) 
#                 
#                 
#                 
#             
#                 return center, mask, FastMotion, frame, 
#                 
#             except:  
#             
#                 
#                 return FastMotion
#         
#     def makeCircle(self, mask, frame, contours, contoursFM): 
#         maxRadius = 0 
#         listx = [] 
#         listy = [] 
#         if len(contours) > 0 and len(contoursFM) > 5: 
#         
#             for cnt in contours: 
#                 
#                 (x,y),radius = cv2.minEnclosingCircle(cnt)
#                 listx.append(int(x)) 
#                 listy.append(int(y)) 
#                 radius = int(radius)
#                 if radius > maxRadius: 
#                     maxRadius = radius 
#         
#         
#             cx, cy = removeOutliers(listx, listy)
#             
#             # print(cx, cy) 
#             # if cx - radius < 0: 
#             #     print ('bruh') 
#             
#             # - you can find the max radius initially, while testing 
#             # initially, ask to place in center of screen and wait for radius to 
#             # eclipse entire ball, then use that radius and center for testing if 
#             # edge 
#             
#             
#         
#             if (maxRadius) > 250: #make sure not to hardcode this later on 
#                 print("move that shit back") 
#                 
#                 
#             if not cx == None: 
#                 center = (int(cx), int(cy)) 
#                 cv2.circle(frame,center,maxRadius,(0,255,0),2)
#             
#                 print(center) 
#                 return center, mask, frame  
#         
#             
#             return None  
#             
#         return None  

# OpenCV() 
# 
# while True: 
#     happy.findCircle() 
#     
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# 
#     # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()






''' 
actual 
import numpy as np
import cv2
import time
import math
import copy 
import random 
from SF import * 

def diffImg(t0, t1, t2): 
  #Recieved code for the diffImg function from the following link... 
  #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
  #
  d1 = cv2.absdiff(t2, t1)

  d2 = cv2.absdiff(t1, t0)
  
   
  return cv2.bitwise_and(d1, d2)
 
 
def findFrame(data):

    frame = data.frame
    mask = modifyFrame(frame) 
    
    
    try: 
        
        
        data.Found = True 
        center, mask, FastMotion, FastMotion2, frame = erodeAndFastTrack(mask, frame, 
        data)
                
                #print("data.center =" + str(data.center)) 
                #print("data.prevcenter =" + str(data.prevcenter)) 
             
        
    except: 
        
        data.Found = False
        FastMotion, FastMotion2 = erodeAndFastTrack(mask, frame, data) 
        
        
     
    
    data.frame = frame
    data.mask = mask 
    data.FastMotion = FastMotion 
    data.FastMotion2 = FastMotion2 
    
    
def modifyFrame(frame): 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    #recieved code for the following 3 lines from the following link, 
    #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/


    
    lowergreen = np.array([29,70,21]) 
    uppergreen = np.array([64, 255, 255]) 
    
    mask = cv2.inRange(hsv, lowergreen, uppergreen) 
    
    res = cv2.bitwise_and(frame, frame, mask = mask) 
    
    
    mask = cv2.medianBlur(mask,5)
    
     
    return mask
        
    
    
def erodeAndFastTrack(mask, frame, data): 
    
    kernel = np.ones((5,5),np.uint8)
    
    
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    if data.t_minus == None: 
        #recieved code for the following 3 lines from the following link, 
        #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
        data.t_minus = mask 
        data.t = mask 
        data.t_plus = mask
      
    
    else: 
        #recieved code for the following 3 lines from the following link, 
        #http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
        data.t_minus = data.t
        data.t = data.t_plus
        data.t_plus = mask 
        
    
    
    FastMotion = diffImg(data.t_minus, data.t, data.t_plus) 
    FastMotion2 = data.FastMotionDetection.apply(mask) 
    FastMotion = cv2.erode(FastMotion, kernel, iterations=1)
    FastMotion2 = cv2.erode(FastMotion2, kernel, iterations=3)
     
    
    image, contours, hierarchy = (cv2.findContours
    (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
     
    imageFM, contoursFM, hierarchyFM = (cv2.findContours
    (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
    
    imageFM2, contoursFM2, hierarchyFM2 = (cv2.findContours
    (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
    
    # if len(contours) > 0: 
    #     c = max(contours, key=cv2.contourArea)
    #     (x,y),maxRadius = cv2.minEnclosingCircle(c)
    if len(contours) > 0:
        maxRadius = 0 
        for cnt in contours: 
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            radius = int(radius)
            if radius > maxRadius: 
                maxRadius = radius 
                maxcnt = cnt 
                
        Movements = cv2.moments(maxcnt)
        cx = int(Movements["m10"] / Movements["m00"])
        cy = int(Movements["m01"] / Movements["m00"])
        center = (cx, cy) 
    
        if not data.FirstCenter:
            data.center = center
            data.prevCenter = center  
            data.FirstCenter = True
            
        data.center = center 
     
     
    
    if contours == []: 
        
        
        return FastMotion, FastMotion2
    
    else: 

            maxRadius = int(maxRadius) 
            frame = makeCircle(mask,
            frame, contours, contoursFM, contoursFM2, data, center, maxRadius) 
        
        
            return center, mask, FastMotion, FastMotion2, frame
            
    
    
def makeCircle(mask, frame, contours, contoursFM, contoursFM2, data, center, maxRadius): 
    
    listx = [] 
    listy = [] 
    
   
    if len(contoursFM) >= 0 and len(contoursFM2) > 0: 
         
        data.prevCenter = data.center 
        data.FM = True 
        cv2.circle(frame, (center), maxRadius,(0,255,0),2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
               
            
        return frame
        
    else: 
    
        if data.FirstCenter: 
            
            data.center = data.prevCenter 
            
            print("howdy") 
            
            data.FM = False 
            #print("Found contours, but not movements, center should equal previous value") 
            
            cv2.circle(frame, (data.center), maxRadius,(0,255,0),2)
            cv2.circle(frame, data.center, 5, (0, 0, 255), -1)
    
    return frame  
''' 
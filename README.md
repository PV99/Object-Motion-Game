#Open CV Object Tracking Game 


High Level: 
Teddy Bear Run is a game based on color tracking of physical, player-controlled objects. 
The game starts with a prompt, asking about the number of players for the game. The user/users
can then define HSV ranges, radius sizes, etc for objects they are tracking. They can test out 
their tracking real time, and accordingly change the values of their objects until they are 
satisfied with the results. When their object is tracking well enough, they can start playing. 
The goal of the game is to have the players guide their associated game characters away from 
enemies. 


How to Run: 
Go to the code folder, do not move any files out of place, and run the “Tkinter Base” file.  
Press on play and then enter in a digit representing the amount of players you want. Then, 
in the entry bar, enter in a digit representing the player you are controlling and press 
Set View.  Similarly, enter in the digit of the player you want to modify before pressing 
any of the buttons. Once all players have been modified, press Play. Then guide the user on
the screen to avoid the enemies. 

Libraries/Modules Used: 
Following instructions are based on a user with a Macbook, python3, and latest macOS. User can
still complete instructions with simple fixes 

1. time, math, random, time, copy, string, sys, tkinter(and ttk – add on to tkinter): (should come with python) 
2. numpy as np: go to terminal and type in “pip install numpy” 
3. open cv: Download XCODE or update to latest version and check yes on the developer’s agreement. 
then, in terminal, type in: 

ruby -e "$(curl –fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	brew tap homebrew/science

brew  install open cv 

Alternatively - if this does not work – having downloaded xcode and brew, type in 
pip install opencv-python 


4. Pillow: go to terminal and type in “pip install pillow” 







	
	 




### IMPORTING-MODULES ###

import pygame,sys,random #pygame,sys and time module
from pygame.locals import * #pygame.locals contain constants like KEYUP etc

### SETTING THE CONSTANTS TO BE USED IN MEMEORY GAME ###

FPS=30 #means 30 times the screen is going to be updated per second
WINDOWWIDTH=640 #width of the window is 640 pixels
WINDOWHEIGHT=480 #height of the window is 480 pixels
REVEALSPEED=8 #how fast the boxes reveal
BOXSIZE=40 #width and height of the boxes in pixels
BOXGAP=10 #separation between the boxes is 10 pixels
BOARDWIDTH=10 #10 columns
BOARDHEIGHT=7 #7 rows
##assertion for checking whether the number of boxes are even or not
assert((BOARDWIDTH*BOARDHEIGHT)%2==0),'even number of boxes are required'


## RGB COLOR CODES ##

GRAY=(100,100,100) #GRAY
NAVYBLUE=(60,60,100) #NAVYBLUE
WHITE=(255,255,255) #WHITE
RED=(255,0,0) #RED
GREEN=(0,255,0) #GREEN
BLUE=(0,0,255) #BLUE
YELLOW=(255,255,0) #YELLOW
ORANGE=(255,128,0) #ORANGE
PURPLE=(255,0,255) #PURPLE
CYAN=(0,255,255) #CYAN
BGCOLOR=NAVYBLUE 
BOXCOLOR=WHITE
LIGHTBGCOLOR=GRAY
HIGHLIGHTCOLOR=BLUE
XMARGIN=int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+BOXGAP)))/2)
## represents the space between between the window and the first/last white box
YMARGIN=int((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+BOXGAP)))/2)
## STORING STRINGS IN VARIABLES TO AVOID CONFUSION AND ERRORS
DONUT="donut" 
SQUARE="square"
DIAMOND="diamond"
LINES="lines"
OVAL="oval"

ALLCOLORS=(RED,YELLOW,BLUE,GREEN,ORANGE,PURPLE,CYAN)
ALLSHAPES=(DONUT,SQUARE,DIAMOND,LINES,OVAL)
assert len(ALLCOLORS)*len(ALLSHAPES)*2==BOARDWIDTH*BOARDHEIGHT,'number of icons are not enough'
def main():
    global DISPLAYSURF,FPSCLOCK #these are declared as global so that other functions can also access them
    pygame.init() #before calling any pygame function call pygame.init()
    FPSCLOCK=pygame.time.Clock() #the object will control the speed of the game
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) #window
    pygame.display.set_caption('MEMORY GAME') #caption
    mousex=0 #stores mouse's x coordinate,initialised with 0
    mousey=0 #stores mouse's y coordinate,initialsed with 0
    mainboard=getRandomizedBoard() #this will return the complete board representation in the form of a 2dimensional list
    revealedBoxes=generateRevealedBoxesData(False) #this returns a boolean value of true or false in a 2d list .true means uncovered and false means covered
    DISPLAYSURF.fill(BGCOLOR)#colors the screen with the specified bgcolor
    firstSelection=None #it keeps tract of whether the first icon of a partiular pair is clicked or the second icon
    startGameAnimation(mainboard) #gives some time in the beginning and shows the uncovered boxes for a short interval of time
    while True: #game loop
        mouseClicked=False #checks whether the mouse is clicked or not
        DISPLAYSURF.fill(BGCOLOR) #again fills the background
        drawBoard(mainBoard,revealedBoxes) #draws the state onto the screen
        for event in pygame.event.get():#returns an event object
            if event.type==QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
                pygame.quit()#quit pygame
                sys.exit()#quit program
            elif event.type==MOUSEMOTION: #if the mouse is in motion keep 
                mousex,mousey=event.pos#tract of its coordinates
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos#if it is clicked along with coordinated
                mouseClicked=True #make mouse pressed point to true
            boxx,boxy=getBoxAtPixel(mousex,mousey) #this function returns the the coordinated of box on the board
            if boxx!=None and boxy!=None: # if the cursor was not on any valid position None will be returned for that coordinate and we are interested only on checking the condition if both the coordinates are valid
                if not revealedBoxes[boxx][boxy]: #checks from a 2d list of boolean values if the box is covered or not
                    drawHighlightBox(boxx,boxy)#if the box is uncovered highlight its boundary
                if not revealedBoxes[boxx][boxy] and mouseClicked: #if the box is not revealed and clicked on
                    revealBoxesAnimation(mainboard,[(boxx,boxy)]) #this function reveals the boxes
                    revealedBoxes[boxx][boxy]=True #this makes this change permanent
                    if firstSelection==None: #if the first box of a pair was selected we need to store the box cordinates of it
                        firstSelection=(boxx,boxy) #storing the box coordinates if it was the first icon of a pair
                    else: #or if it was the second icon of a pair then theses instructions will be followed
                        icon1shape,icon1color=getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1]) #getting the shape and color of the first selected icon
                        icon2shape,icon2color=getShapeAndColor(mainBoard,boxx,boxy) #getting the shape and icon of the second selected icon                       
                        if icon1shape!=icon2shape or icon1color!=icon2color: #if either of them dont match
                            pygame.time.wait(1000) #wait for 1000 milliseconds or 1 second
                            coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1])],[(boxx,boxy)]) #coverBoxesAnimation will cover the two selected boxes with the help of box coordinates
                            revealedBoxes[boxx][boxy]=False #also in order to make these changes permanent we need to make changes in the 2 dimensional list
                            revealedBoxes[firstSelection[0]][firstSelection[1]]=False # this line does the same
                        elif hasWon(revealedBoxes): #well if the two boxes selected were right changes have already been made and hence nothing needs to be done except when the user has selected all the boxes correctly
                            gameWonAnimation(mainBoard) #this function will do something when the user winds the game
                            pygame.time.wait(2000) #wait for 2000 milliseconds ie 2 seconds
                            pygame.quit() # close the pygame module
                            sys.exit() # exit the game
                        firstSelection=None #even if the 2 boxes selected were right or wrong we need to create a new platform for selection 
                    pygame.display.update() #updates the game state and draws it to the screen
                    FPSCLOCK.tick(FPS) #controls the speed of the game
def generateRevealedBoxesData(val):# this function will return a 2d list containing boolean values ,false for covered and true foe uncovered
    revealedBoxes=[] #empty list
    for i in range(BOARDWIDTH): #runs for 10 times
        revealedBoxes.append([val]*BOARDHEIGHT) #creates a list of size seven and appends it into the list for 10 times
    return revealedBoxes #returns the generated list
def getRandomizedBoard(): #this function will generate a randomly new 2d list every time the user starts the game
    icons=[] #empty list
    for color in ALLCOLORS: #runs ALLCOLOR.length time
        for shape in ALLSHAPES: #runs ALLSHAPES.length time
            icons.append((shape,color)) #append a possible pair into the list
    random.shuffle(icons) #shuffle the tuples present in a list
    icons=icons*2 #string replication ie increase the contents of a string by 2 times
    random.shuffle(icons) #again shuffle the items of the final list 
    board=[] #empty list
    for x in range(BOARDWIDTH): #runs 10 times
        column=[] #empty list
        for y in range(BOARDHEIGHT): #runs 7 times
            column.append(icons[0]) #appends the first tuple into the columns list
            del icons[0] #simultaneously deletes the first tuple in the icons least so that all icons shift one to left
        board.append(column) # inserts 7 items in a list and then appends these 7 items to a new list.repeat the process 10 times   
    return board #return the board
def leftTopCoordsOfBox(boxx,boxy): #this function returns the coordinates of the top left and right coordinates of the box by referring to the box coordinates
    left=boxx*(BOXSIZE+GAPSIZE)+XMARGIN #top left coordinate
    top=boxy*(BOXSIZE+GAPSIZE)+YMARGIN #top coordinate
    return (left,top) #return the tuple of coordinates
 

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
                    if firstSelection==None:
                        firstSelection=(boxx,boxy)
                    else:
                        icon1shape,icon1color=getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                        icon2shape,icon2color=getShapeAndColor(mainBoard,boxx,boxy)                        
                        if icon1shape!=icon2shape or icon1color!=icon2color:
                            pygame.time.wait(1000)
                            coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1])],[(boxx,boxy)])
                            revealedBoxes[boxx][boxy]=False
                            revealedBoxes[firstSelection[0]][firstSelection[1]]=False
                        elif hasWon(revealedBoxes):
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit()
                        firstSelection=None
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
def generateRevealedBoxesData(val):
    revealedBoxes=[]
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGHT)
    return revealedBoxes
def getRandomizedBoard():
    icons=[]
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape,color))
    random.shuffle(icons)
    icons=icons*2
    random.shuffle(icons)
    board=[]
    for x in range(BOARDWIDTH):
        column=[]
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)    
    return board
def leftTopCoordsOfBox(boxx,boxy):
    left=boxx*(BOXSIZE+GAPSIZE)+XMARGIN
    top=boxy*(BOXSIZE+GAPSIZE)+YMARGIN
    return (left,top)
 

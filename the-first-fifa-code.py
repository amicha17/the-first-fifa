from tkinter import *
import copy
import math
import random

def init(data):
    data.cornerRadius=30
    data.gameState=-5
    data.players=[]
    data.opposingPlayers=[]
    data.selectedPlayer=7
    data.selectedOtherPlayer=7
    data.dx=0
    data.dy=0
    data.otherDx=0
    data.otherDy=0
    data.ballSpeedX=0
    data.ballSpeedY=0
    data.gk=Player(100,data.height//2)
    data.gk2=Player(data.width-100,data.height//2)
    data.gk2.setCol("red")
    data.gkSpeed=-30
    data.gk2Speed=30
    data.ballX=data.width//2
    data.ballY=data.height//2
    data.dir=0
    data.pPressed=False
    data.score1=0
    data.score2=0
    data.twoPlayer=False
    data.team=""
    data.time=0
    data.timeCounter=0
    data.mPressed=False
    data.closestPlayer=7
    data.closestOtherPlayer=7
    data.lPressed=False
    data.fieldPic=0
    data.winPic=0
    data.ballPic=0
    data.arrowPic=0
    data.AI=1
    data.stage=0.5
    data.tournament=False
    data.text=""

def mousePressed(event, data):
    if(event.x<200 and event.y<100):
        data.gameState=-4
    if(event.x>1000 and event.y>700):
        data.gameState=-5
    if(data.gameState!=2):
        if(data.gameState==-4):
            if(event.x>200 and event.x<1000):
                if(event.y<data.height//4+100 and event.y>100):
                    data.gameState=-1
                elif(event.y>data.height*3//4-50):
                    data.tournament=True
                    data.gameState=-3
        elif(data.gameState==-1):
            if(event.x<100 and event.y<100):
                data.gameState=-4
            elif(event.x<data.width//2):
                data.twoPlayer=False
                data.gameState=-2
            else:
                data.AI=1
                data.twoPlayer=True
                data.gameState=0
        elif(data.gameState==-2):
            if(event.x<data.width//4+75):
                data.AI=.75
                data.gameState=0
            elif(event.x<data.width*3//4-75):
                data.AI=1
                data.gameState=0
            else:
                data.AI=1.25
                data.gameState=0

def distance(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def keyPressed(event, data):
    if(event.keysym=="Left"):
        player=data.players[data.selectedPlayer%8]
        player.setCol("black")
        if(player.hasBall(data)):
            data.dir=1
            data.ballY=player.getPos()[1]
            data.ballX=player.getPos()[0]-20
            data.ballX-=20
        data.dx=-20
        player.move(data.dx,0,data)
    elif(event.keysym=="Right"):
        player=data.players[data.selectedPlayer%8]
        player.setCol("black")
        if(player.hasBall(data)):
            data.dir=2
            data.ballY=player.getPos()[1]
            data.ballX=player.getPos()[0]+20
            data.ballX+=20
        data.dx=20
        player.move(data.dx,0,data)
    elif(event.keysym=="Down"):
        player=data.players[data.selectedPlayer%8]
        player.setCol("black")
        if(player.hasBall(data)):
            data.dir=3
            data.ballX=player.getPos()[0]
            data.ballY=player.getPos()[1]+20
            data.ballY+=10
        data.dy=10
        player.move(0,data.dy,data)
    elif(event.keysym=="Up"):
        player=data.players[data.selectedPlayer%8]
        player.setCol("black")
        if(player.hasBall(data)):
            data.dir=4
            data.ballX=player.getPos()[0]
            data.ballY=player.getPos()[1]-20
            data.ballY-=10
        data.dy=-10
        player.move(0,data.dy,data)
    elif(event.keysym=="l"):
        close=data.width
        if(len(data.players)!=0 and len(data.opposingPlayers)!=0):
            for i in range(len(data.players)):
                dist=distance(data.players[i].getPos()[0],
                                    data.players[i].getPos()[1],
                                        data.ballX,data.ballY)
                if(dist<close):
                    close=dist
                    data.closestPlayer=i
            data.selectedPlayer=data.closestPlayer
        data.dx=0
        data.dy=0
    elif(event.keysym=="m"):
        data.selectedPlayer=7
        data.dir=0
        data.gameState=-4
        data.pPressed=False
        data.ballX=data.width//2
        data.ballY=data.height//2
        data.time=0
        data.score1=0
        data.score2=0  
    elif(event.keysym=="p"):
        player=data.players[data.selectedPlayer%8]
        if(player.hasBall(data)):
            data.pPressed=True
    elif(event.keysym=="o"):
        if(data.gk.hasBall(data)):
            closestDistance=data.width
            for player in data.players:
                dist=distance(player.getPos()[0],player.getPos()[1],
                                data.gk.getPos()[0],data.gk.getPos()[1])
                if(dist<closestDistance):
                    closestDistance=dist
                    closestPlayer=player
            data.ballX=closestPlayer.getPos()[0]+30
            data.ballY=closestPlayer.getPos()[1]
    if(data.twoPlayer==True):
        if(event.keysym=="z"):
            close=data.width
            if(len(data.opposingPlayers)!=0):
                for i in range(len(data.opposingPlayers)):
                    dist=distance(data.opposingPlayers[i].getPos()[0],
                                        data.opposingPlayers[i].getPos()[1],
                                            data.ballX,data.ballY)
                    if(dist<close):
                        close=dist
                        data.closestOtherPlayer=i
                data.selectedOtherPlayer=data.closestOtherPlayer
            data.otherDx=0
            data.otherDy=0
        elif(event.keysym=="c"):
                if(data.gk2.hasBall(data)):
                    closestDistance=data.width
                    for player in data.opposingPlayers:
                        dist=distance(player.getPos()[0],player.getPos()[1],
                                        data.gk2.getPos()[0],data.gk2.getPos()[1])
                        if(dist<closestDistance):
                            closestDistance=dist
                            closestPlayer=player
                    data.ballX=closestPlayer.getPos()[0]-30
                    data.ballY=closestPlayer.getPos()[1]
        elif(event.keysym=="w"):
            player=data.opposingPlayers[data.selectedOtherPlayer%8]
            player.setCol("pink")
            if(player.hasBall(data)):
                data.dir=4
                data.ballX=player.getPos()[0]
                data.ballY=player.getPos()[1]-20
                data.ballY-=10
            data.otherDy=-20
            player.move(0,data.otherDy,data)
        elif(event.keysym=="a"):
            player=data.opposingPlayers[data.selectedOtherPlayer%8]
            player.setCol("pink")
            if(player.hasBall(data)):
                data.dir=1
                data.ballY=player.getPos()[1]
                data.ballX=player.getPos()[0]-20
                data.ballX-=20
            data.otherDx=-20
            player.move(data.otherDx,0,data)
        elif(event.keysym=="s"):
            player=data.opposingPlayers[data.selectedOtherPlayer%8]
            player.setCol("pink")
            if(player.hasBall(data)):
                data.dir=3
                data.ballX=player.getPos()[0]
                data.ballY=player.getPos()[1]+20
                data.ballY+=10
            data.otherDy=20
            player.move(0,data.otherDy,data)
        elif(event.keysym=="d"):
            player=data.opposingPlayers[data.selectedOtherPlayer%8]
            player.setCol("pink")
            if(player.hasBall(data)):
                data.dir=2
                data.ballY=player.getPos()[1]
                data.ballX=player.getPos()[0]+20
                data.ballX+=20
            data.otherDx=20
            player.move(data.otherDx,0,data)
        elif(event.keysym=="x"):
            player=data.opposingPlayers[data.selectedOtherPlayer%8]
            if(player.hasBall(data)):
                data.pPressed=True
    if(event.keysym=="n"):
        if(data.gameState==-3):
            data.stage+=.5
            data.twoPlayer=False
            data.gameState=0
        elif(data.gameState==2):
            data.stage+=.5
            data.dir=0
            data.selectedPlayer=7
            data.gameState=-3
        
class Player(object):
    def __init__(self,x,y):
        self.spawnx=x
        self.spawny=y
        self.dx=0
        self.dy=0
        self.color="blue"

    def getPos(self):
        return (self.spawnx+self.dx,self.spawny+self.dy)

    def hasBall(self,data):
        if(distance(self.spawnx+self.dx,self.spawny+self.dy,data.ballX,
                        data.ballY)<=40):
            return True
        else:
            return False

    def setPos(self,x,y):
        self.spawnx=x
        self.spawny=y

    def setCol(self,color):
        self.color=color

    def move(self,dx,dy,data):
        data.dx+=dx
        self.dx+=dx
        self.dy+=dy
        data.dy+=dy

    def launchBall(self,data,dir):
        if(dir==2):
            data.ballX+=30
        elif(dir==1):
            data.ballX-=30
        elif(dir==3):
            data.ballY+=30
        elif(dir==4):
            data.ballY-=30
    
    def tackle(self,data):
        data.pPressed=False

    def drawPlayer(self,canvas):
        canvas.create_oval(self.spawnx+self.dx-10,self.spawny+self.dy-10,
                            self.spawnx+self.dx+10,self.spawny+self.dy+10,              
                            fill=self.color,width=0)

def drawBall(canvas,data,x,y):
    data.ball=canvas.create_oval(x-10,y-10,x+10,y+10,fill="white")
    data.ballPic=PhotoImage(file="ball.gif")
    canvas.create_image((x,y),image=data.ballPic)

def moveGKs(data):
    data.gk.move(0,data.gkSpeed,data)
    if(data.gk.getPos()[1]<=data.height*9//20):
        data.gkSpeed=10*data.AI
    elif(data.gk.getPos()[1]>=data.height*12//20-30):
        data.gkSpeed=-10*data.AI
    data.gk2.move(0,data.gk2Speed,data)
    if(data.gk2.getPos()[1]<=data.height*9//20):
        data.gk2Speed=10*data.AI
    elif(data.gk2.getPos()[1]>=data.height*12//20-30):
        data.gk2Speed=-10*data.AI
        
def keepTrackofPlayers(data):
    if(len(data.players)!=0 and len(data.opposingPlayers)!=0):
        for i in range(len(data.players)):
            if(data.players[i].hasBall(data)):
                data.selectedPlayer=i
        for player in data.players:
            if(player.getPos()[1]<=45):
                data.dy=20
                player.move(0,data.dy,data)
            elif(player.getPos()[1]>=data.height-45):
                data.dy=-20
                player.move(0,data.dy,data)
            if(player.getPos()[0]<=90):
                data.dx=20
                player.move(data.dx,0,data)
            elif(player.getPos()[0]>data.width-90):
                data.dx=-20
                player.move(data.dx,0,data)
            if(player.hasBall(data)):
                data.team="blue"
                player.tackle(data)
        for player in data.opposingPlayers:
            if(player.getPos()[1]<=45):
                data.otherDy=20
                player.move(0,data.otherDy,data)
            elif(player.getPos()[1]>=data.height-45):
                data.otherDy=-20
                player.move(0,data.otherDy,data)
            if(player.getPos()[0]<=90):
                data.otherDx=20
                player.move(data.otherDx,0,data)
            elif(player.getPos()[0]>data.width-90):
                data.otherDx=-20
                player.move(data.otherDx,0,data)
            if(player.hasBall(data)):
                player.tackle(data)
                data.team="red"
        if(data.twoPlayer):
            for i in range(len(data.opposingPlayers)):
                if(data.opposingPlayers[i].hasBall(data)):
                    data.selectedOtherPlayer=i

def keepTrackofGoal(data):
    if(data.width-data.ballX<=100 and data.ballY>=data.height*9//20
                        and data.ballY<=data.height*12//20):
        data.pPressed=False
        data.ballX=data.width//2
        data.ballY=data.height//2
        data.score1+=1
        data.gameState=0
    elif(data.width-data.ballX<=100 and (data.ballY<=data.height*9//20 or 
                        data.ballY>=data.height*12//20)):
        data.pPressed=False
        data.ballX=data.gk2.getPos()[0]-30
        data.ballY=data.height//2
    if(data.ballX<=100 and data.ballY>=data.height*9//20
                        and data.ballY<=data.height*12//20):
        data.pPressed=False
        data.ballX=data.width//2
        data.ballY=data.height//2
        data.score2+=1
        data.gameState=0
    elif(data.ballX<=100 and (data.ballY<=data.height*9//20 or 
                        data.ballY>=data.height*12//20)):
        data.pPressed=False
        data.ballX=data.gk.getPos()[0]+30
        data.ballY=data.height//2
    if(data.ballX-data.gk.getPos()[0]<=30 and 
                    abs(data.gk.getPos()[1]-data.ballY<=30)):
        data.pPressed=False
        data.ballX=data.gk.getPos()[0]+30
        data.ballY=data.gk.getPos()[1]
    if(data.gk2.getPos()[0]-data.ballX<=30 and
                    abs(data.gk2.getPos()[1]-data.ballY)<=30):
        data.pPressed=False
        data.ballX=data.gk2.getPos()[0]-30
        data.ballY=data.gk2.getPos()[1]

def swap(a, i, j):
    (a[i], a[j]) = (a[j], a[i])

def selectionSort(a):
    n = len(a)
    for startIndex in range(n):
        minIndex = startIndex
        for i in range(startIndex+1, n):
            if (a[i][0] < a[minIndex][0]):
                minIndex = i
        swap(a, startIndex, minIndex)
    return a

def blueOffensiveAI(data):
    if(data.selectedPlayer%8==0):
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[3].getPos()[1])>20):
            if(data.players[3].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[3].getPos()[0])<=100):
                data.dx=5
            else:
                data.dx=0
            data.players[3].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[1].getPos()[0])>20):
            if(data.players[1].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[1].getPos()[1])<=100):
                data.dy=5
            else:
                data.dy=0
            data.players[1].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==1):
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]!=
                    data.players[0].getPos()[0])>20):
            if(data.players[0].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[0].getPos()[1])<=100):
                data.dy=-5
            else:
                data.dy=0
            data.players[0].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[2].getPos()[0])>20):
            if(data.players[2].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[2].getPos()[1])<=100):
                data.dy=5
            else:
                data.dy=0
            data.players[2].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[3].getPos()[1])>20):
            if(data.players[3].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[3].getPos()[0])<=100):
                data.dx=5
            else:
                data.dx=0
            data.players[3].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==2):
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[4].getPos()[1])>20):
            if(data.players[4].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[4].getPos()[0])<=100):
                data.dx=5
            else:
                data.dx=0
            data.players[4].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[1].getPos()[0])>20):
            if(data.players[1].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[1].getPos()[1])<=100):
                data.dy=-5
            else:
                data.dy=0
            data.players[1].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==3):
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[0].getPos()[1])>20):
            if(data.players[0].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[0].getPos()[0])<=100):
                data.dx=-5
            else:
                data.dx=0
            data.players[0].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[4].getPos()[0])>20):
            if(data.players[4].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[4].getPos()[1])<=100):
                data.dy=5
            else:
                data.dy=0
            data.players[4].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[7].getPos()[1])>20):
            if(data.players[7].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[7].getPos()[0])<=100):
                data.dx=5
            else:
                data.dx=0
            data.players[7].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==4):
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[2].getPos()[1])>20):
            if(data.players[2].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[2].getPos()[0])<=100):
                data.dx=-5
            else:
                data.dx=0
            data.players[2].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[3].getPos()[0])>20):
            if(data.players[3].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[3].getPos()[1])<=100):
                data.dy=-5
            else:
                data.dy=0
            data.players[3].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[7].getPos()[1])>20):
            if(data.players[7].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[7].getPos()[0])<=100):
                data.dx=5
            else:
                data.dx=0
            data.players[7].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==5):
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[7].getPos()[1])>20):
            if(data.players[7].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[7].getPos()[0])<=100):
                data.dx=-5
            else:
                data.dx=0
            data.players[7].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[6].getPos()[0])>20):
            if(data.players[6].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[6].getPos()[1])<=100):
                data.dy=5
            else:
                data.dy=0
            data.players[6].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==6):
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[7].getPos()[1])>20):
            if(data.players[7].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[7].getPos()[0])<=100):
                data.dx=-5
            else:
                data.dx=0
            data.players[7].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[5].getPos()[0])>20):
            if(data.players[5].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[5].getPos()[1])<=100):
                data.dy=-5
            else:
                data.dy=0
            data.players[5].move(data.dx,data.dy,data)
    elif(data.selectedPlayer%8==7):
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[6].getPos()[0])>10):
            if(data.players[6].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[6].getPos()[1])<=100):
                data.dy=5
            else:
                data.dy=0
            data.players[6].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[0]-
                    data.players[3].getPos()[0])>10):
            if(data.players[3].getPos()[0]>
                    data.players[data.selectedPlayer%8].getPos()[0]):
                data.dx=-10
            else:
                data.dx=10
            if(abs(data.players[data.selectedPlayer].getPos()[1]-
                    data.players[3].getPos()[1])<=100):
                data.dy=-5
            else:
                data.dy=0
            data.players[3].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[4].getPos()[1])>10):
            if(data.players[4].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[4].getPos()[0])<=100):
                data.dx=-5
            else:
                data.dx=0
            data.players[4].move(data.dx,data.dy,data)
        if(abs(data.players[data.selectedPlayer%8].getPos()[1]-
                    data.players[5].getPos()[1])>10):
            if(data.players[5].getPos()[1]>
                    data.players[data.selectedPlayer%8].getPos()[1]):
                data.dy=-10
            else:
                data.dy=10
            if(abs(data.players[data.selectedPlayer].getPos()[0]-
                    data.players[5].getPos()[0])<=100):
                data.dx=5
            else:
                data.dx=0
            data.players[5].move(data.dx,data.dy,data)

def twoPlayerRedDef(data):
    if(len(data.players)!=0 and len(data.opposingPlayers)!=0):
        for x in range(len(data.opposingPlayers)):
            if(x%8!=data.closestOtherPlayer and x!=data.selectedOtherPlayer):
                if(x%8==0):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+5].getPos()[0]-60)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+5].getPos()[0]-60)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+5].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+5].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    if(data.opposingPlayers[x%8].getPos()[0]>data.width//2):
                        data.opposingPlayers[x%8].move(data.otherDx,
                                                            data.otherDy,data)
                elif(x%8==1):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+6].getPos()[0]-60)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+6].getPos()[0]-60)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+6].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+6].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    if(data.opposingPlayers[x%8].getPos()[0]>data.width//2):
                        data.opposingPlayers[x%8].move(data.otherDx,
                                data.otherDy,data)
                elif(x%8==2):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+4].getPos()[0]-60)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+4].getPos()[0]-60)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+4].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+4].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    if(data.opposingPlayers[x%8].getPos()[0]>data.width//2):
                        data.opposingPlayers[x%8].move(data.otherDx,
                                data.otherDy,data)
                elif(x%8==3 or x%8==4):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)
                elif(x%8==5):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-5].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-5].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-5].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-5].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)
                elif(x%8==6):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-4].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-4].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-4].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-4].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)
                elif(x%8==7):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-6].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-6].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-6].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-6].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)

def onePlayerRedDef(data):
    if(len(data.players)!=0 and len(data.opposingPlayers)!=0):
        if((data.opposingPlayers[data.closestOtherPlayer].
                getPos()[0]-data.ballX)>=40 and abs(data.opposingPlayers
                [data.closestOtherPlayer].getPos()[1]-data.ballY)<=40):
            data.otherDx=-20*data.AI
            data.opposingPlayers[data.closestOtherPlayer].move(data.otherDx,0,data)
        elif((data.ballY-data.opposingPlayers[data.closestOtherPlayer].
                getPos()[1])>=40 
                and (data.opposingPlayers[data.closestOtherPlayer].getPos()[0]-
                data.ballX)>=40):
            data.otherDy=20*data.AI
            data.opposingPlayers[data.closestOtherPlayer].move(0,data.otherDy,data)
        elif((data.opposingPlayers[data.closestOtherPlayer].
                getPos()[1]-data.ballY)>=40 
                and data.opposingPlayers[data.closestOtherPlayer].getPos()[0]-
                data.ballX>=40):
            data.otherDy=-20*data.AI
            data.opposingPlayers[data.closestOtherPlayer].move(0,data.otherDy,data)
        else:
            data.otherDx=20*data.AI
            data.opposingPlayers[data.closestOtherPlayer].move(data.otherDx,0,data)
        for x in range(len(data.opposingPlayers)):
            if(x%8!=data.closestOtherPlayer):
                if(x%8==0):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+5].getPos()[0]-60)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+5].getPos()[0]-60)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+5].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+5].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    if(data.opposingPlayers[x%8].getPos()[0]>data.width//2):
                        data.opposingPlayers[x%8].move(data.otherDx,
                                data.otherDy,data)
                elif(x%8==1):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+6].getPos()[0]-60)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+6].getPos()[0]-60)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+6].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+6].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    if(data.opposingPlayers[x%8].getPos()[0]>data.width//2):
                        data.opposingPlayers[x%8].move(data.otherDx,
                                data.otherDy,data)
                elif(x%8==2):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+4].getPos()[0]-60)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8+4].getPos()[0]-60)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+4].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8+4].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    if(data.opposingPlayers[x%8].getPos()[0]>data.width//2):
                        data.opposingPlayers[x%8].move(data.otherDx,
                                data.otherDy,data)
                elif(x%8==3 or x%8==4):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)
                elif(x%8==5):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-5].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-5].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-5].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-5].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)
                elif(x%8==6):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-4].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-4].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-4].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-4].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)
                elif(x%8==7):
                    if((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-6].getPos()[0]-40)>0):
                        data.otherDx=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[0]-
                            data.players[x%8-6].getPos()[0]-40)<0):
                        data.otherDx=10*data.AI
                    else:
                        data.otherDx=0
                    if((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-6].getPos()[1])>0):
                        data.otherDy=-10*data.AI
                    elif((data.opposingPlayers[x%8].getPos()[1]-
                            data.players[x%8-6].getPos()[1])<0):
                        data.otherDy=10*data.AI
                    else:
                        data.otherDy=0
                    data.opposingPlayers[x%8].move(data.otherDx,data.otherDy,data)

def blueDefensiveAI(data):
    for x in range(len(data.players)):
        data.selectedPlayer=data.closestPlayer
        if(x%8!=data.closestPlayer and x!=data.selectedPlayer):
            if(x%8==0):
                if((data.opposingPlayers[x%8+5].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8+5].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8+5].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8+5].getPos()[1]-
                        data.players[x%8].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                if(data.players[x%8].getPos()[0]<data.width//2):
                    data.players[x%8].move(data.dx,data.dy,data)
            elif(x%8==1):
                if((data.opposingPlayers[x%8+6].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8+6].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8+6].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8].getPos()[1]-
                        data.players[x%8+6].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                if(data.players[x%8].getPos()[0]<data.width//2):
                    data.players[x%8].move(data.dx,data.dy,data)
            elif(x%8==2):
                if((data.opposingPlayers[x%8+4].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8+4].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8+4].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8+4].getPos()[1]-
                        data.players[x%8].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                if(data.players[x%8].getPos()[0]<data.width//2):
                    data.players[x%8].move(data.dx,data.dy,data)
            elif(x%8==3 or x%8==4):
                if((data.opposingPlayers[x%8].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8].getPos()[1]-
                        data.players[x%8].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                data.players[x%8].move(data.dx,data.dy,data)
            elif(x%8==5):
                if((data.opposingPlayers[x%8-5].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8].getPos()[0]-
                        data.players[x%8-5].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8-5].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8].getPos()[1]-
                        data.players[x%8-5].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                data.players[x%8].move(data.dx,data.dy,data)
            elif(x%8==6):
                if((data.opposingPlayers[x%8-4].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8-4].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8-4].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8-4].getPos()[1]-
                        data.players[x%8].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                data.players[x%8].move(data.dx,data.dy,data)
            elif(x%8==7):
                if((data.opposingPlayers[x%8-6].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)>0):
                    data.dx=10
                elif((data.opposingPlayers[x%8-6].getPos()[0]-
                        data.players[x%8].getPos()[0]-40)<0):
                    data.dx=-10
                else:
                    data.dx=0
                if((data.opposingPlayers[x%8-6].getPos()[1]-
                        data.players[x%8].getPos()[1])>0):
                    data.dy=10
                elif((data.opposingPlayers[x%8-6].getPos()[1]-
                        data.players[x%8].getPos()[1])<0):
                    data.dy=-10
                else:
                    data.dy=0
                data.players[x%8].move(data.dx,data.dy,data)

def onePlayerRedOff(data):
    for player in range(len(data.opposingPlayers)):
        if(data.opposingPlayers[player].hasBall(data)):
            if(data.opposingPlayers[player].getPos()[0]<=data.width//5+100 and 
                data.opposingPlayers[player].getPos()[1]>data.height*9//20 and 
                data.opposingPlayers[player].getPos()[1]<data.height*12//20):
                data.dir=1
                data.pPressed=True
            if(player==0):
                if(data.opposingPlayers[player].getPos()[0]>data.width*2//3):
                    data.opposingPlayers[player].move(10,0,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[3].getPos()[1])>10):
                    if(data.opposingPlayers[3].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=-5*data.AI
                    data.opposingPlayers[3].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[1].getPos()[0])>10):
                    if(data.opposingPlayers[1].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=5*data.AI
                    data.opposingPlayers[1].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[3].getPos()[1])<=20 and
                            abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[1].getPos()[0])<=20):
                    x=random.randint(0,1)
                    if(x==0):
                        data.dir=3
                    else:
                        data.dir=1
                    data.pPressed=True
            elif(player==1):
                if(data.opposingPlayers[player].getPos()[0]>data.width*2//3):
                    data.opposingPlayers[player].move(10,0,data)
                if(abs(data.opposingPlayers[player].getPos()[0]!=
                            data.opposingPlayers[0].getPos()[0])>10):
                    if(data.opposingPlayers[0].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=-5*data.AI
                    data.opposingPlayers[0].move(data.otherDx,
                                                    data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[2].getPos()[0])>10):
                    if(data.opposingPlayers[2].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=5*data.AI
                    data.opposingPlayers[2].move(data.otherDx,
                                                    data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[3].getPos()[1])>10):
                    if(data.opposingPlayers[3].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=-5*data.AI
                    data.opposingPlayers[3].move(data.otherDx,
                                                    data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]!=
                            data.opposingPlayers[0].getPos()[0])<=20 and
                            abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[2].getPos()[0])<=20 and
                            abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[3].getPos()[1])<=20):
                    x=random.randint(0,2)
                    if(x==0):
                        data.dir=4
                    elif(x==1):
                        data.dir=1
                    else:
                        data.dir=3
                    data.pPressed=True
            elif(player==2):
                if(data.opposingPlayers[player].getPos()[0]>data.width*2//3):
                    data.opposingPlayers[player].move(10,0,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[4].getPos()[1])>10):
                    if(data.opposingPlayers[4].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=-5*data.AI
                    data.opposingPlayers[4].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[1].getPos()[0])>10):
                    if(data.opposingPlayers[1].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=-5*data.AI
                    data.opposingPlayers[1].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[4].getPos()[1])<=20 and
                            abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[1].getPos()[0])<=20):    
                    x=random.randint(1,2)
                    data.dir=x**2
                    data.pPressed=True
            elif(player==3):
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[4].getPos()[0])>10):
                    if(data.opposingPlayers[4].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=5*data.AI
                    data.opposingPlayers[4].move(data.otherDx,
                                                    data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[7].getPos()[1])>10):
                    if(data.opposingPlayers[7].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=-5*data.AI
                    data.opposingPlayers[7].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[4].getPos()[0])<=20 and
                            abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[7].getPos()[1])<=20):
                    x=random.randint(0,1)
                    if(x==0):
                        data.dir=1
                    else:
                        data.dir=3
                    data.pPressed=True
            elif(player==4):
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[3].getPos()[0])>10):
                    if(data.opposingPlayers[3].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=-5*data.AI
                    data.opposingPlayers[3].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[7].getPos()[1])>10):
                    if(data.opposingPlayers[7].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=-5*data.AI
                    data.opposingPlayers[7].move(data.otherDx,
                                                    data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[3].getPos()[0])<=20 and
                            abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[7].getPos()[1])<=20):
                    x=random.randint(1,2)
                    data.dir=x**2
                    data.pPressed=True
            elif(player==5):
                if(data.opposingPlayers[player].getPos()[0]>data.width//5-20):
                    data.otherDx=-10*data.AI
                    data.ballX=data.opposingPlayers[player].getPos()[0]-30
                    data.opposingPlayers[player].move(data.otherDx,0,data)
                elif(data.opposingPlayers[player].getPos()[1]<data.height//2):
                    data.otherDy=10*data.AI
                    data.ballY=data.opposingPlayers[player].getPos()[1]+30
                    data.ballX=data.opposingPlayers[player].getPos()[0]
                    data.opposingPlayers[player].move(0,data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[7].getPos()[1])>10):
                    if(data.opposingPlayers[7].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=0
                    data.opposingPlayers[7].move(data.otherDx,
                                                data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[6].getPos()[0])>10):
                    if(data.opposingPlayers[6].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=0
                    data.opposingPlayers[6].move(data.otherDx,
                                                            data.otherDy,data)
                for i in range(len(data.players)):
                    dist=distance(data.opposingPlayers[player].getPos()[0],
                        data.opposingPlayers[player].getPos()[1],
                        data.players[i].getPos()[0],data.players[i].
                                                                getPos()[1])
                    if(dist<50):
                        if(abs(data.opposingPlayers[player].getPos()[1]-
                                data.opposingPlayers[7].getPos()[1])<=20 and
                                abs(data.opposingPlayers[player].getPos()[0]-
                                data.opposingPlayers[6].getPos()[0])<=20):
                            data.dir=random.randint(2,3)
                            data.pPressed=True
            elif(player==6):
                if(data.opposingPlayers[player].getPos()[0]>data.width//5-20):
                    data.otherDx=-10*data.AI
                    data.ballX=data.opposingPlayers[player].getPos()[0]-30
                    data.opposingPlayers[player].move(data.otherDx,0,data)
                elif(data.opposingPlayers[player].getPos()[1]>data.height//2):
                    data.otherDy=-10*data.AI
                    data.ballY=data.opposingPlayers[player].getPos()[1]-30
                    data.ballX=data.opposingPlayers[player].getPos()[0]
                    data.opposingPlayers[player].move(0,data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[1]-
                            data.opposingPlayers[7].getPos()[1])>10):
                    if(data.opposingPlayers[7].getPos()[1]>
                            data.opposingPlayers[player].getPos()[1]):
                        data.otherDy=-10*data.AI
                    else:
                        data.otherDy=10*data.AI
                    data.otherDx=0
                    data.opposingPlayers[7].move(data.otherDx,
                                            data.otherDy,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                            data.opposingPlayers[5].getPos()[0])>10):
                    if(data.opposingPlayers[5].getPos()[0]>
                            data.opposingPlayers[player].getPos()[0]):
                        data.otherDx=-10*data.AI
                    else:
                        data.otherDx=10*data.AI
                    data.otherDy=-5*data.AI
                    data.opposingPlayers[5].move(data.otherDx,data.otherDy,data)
                for i in range(len(data.players)):
                    dist=distance(data.opposingPlayers[player].getPos()[0],
                        data.opposingPlayers[player].getPos()[1],
                        data.players[i].getPos()[0],data.players[i].
                                                            getPos()[1])
                    if(dist<50):
                        if(abs(data.opposingPlayers[player].getPos()[1]-
                                data.opposingPlayers[7].getPos()[1])<=20 and
                                abs(data.opposingPlayers[player].getPos()[0]-
                                data.opposingPlayers[5].getPos()[0])<=20):
                            x=random.randint(1,2)
                            data.dir=x*2
                            data.pPressed=True
            elif(player==7):
                if(data.opposingPlayers[player].getPos()[0]>
                            data.opposingPlayers[5].getPos()[0] and
                            data.opposingPlayers[player].getPos()[0]>
                            data.opposingPlayers[6].getPos()[0]):
                    data.otherDx=-10*data.AI
                    data.opposingPlayers[player].move(data.otherDx,0,data)
                    data.ballX=data.opposingPlayers[player].getPos()[0]-30
                data.opposingPlayers[5].move(-2.5*data.AI,-1*data.AI,data)
                data.opposingPlayers[6].move(-2.5*data.AI,1*data.AI,data)
                if(abs(data.opposingPlayers[player].getPos()[0]-
                        data.opposingPlayers[6].getPos()[0])<=20):
                    data.dir=3
                    data.pPressed=True
                if(abs(data.opposingPlayers[player].getPos()[0]-
                        data.opposingPlayers[5].getPos()[0])<=20):
                    data.dir=4
                    data.pPressed=True

def twoPlayerRedOff(data):
    if(data.selectedOtherPlayer%8==0):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[3].getPos()[1])>20):
            if(data.opposingPlayers[3].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[3].getPos()[0])<=100):
                data.otherDx=-5
            else:
                data.otherDx=0
            data.opposingPlayers[3].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[1].getPos()[0])>20):
            if(data.opposingPlayers[1].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[1].getPos()[1])<=100):
                data.otherDy=5
            else:
                data.otherDy=0
            data.opposingPlayers[1].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==1):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]!=
                    data.opposingPlayers[0].getPos()[0])>20):
            if(data.opposingPlayers[0].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[0].getPos()[1])<=100):
                data.otherDy=-5
            else:
                data.otherDy=0
            data.opposingPlayers[0].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[2].getPos()[0])>20):
            if(data.opposingPlayers[2].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[2].getPos()[1])<=100):
                data.otherDy=5
            else:
                data.otherDy=0
            data.opposingPlayers[2].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[3].getPos()[1])>20):
            if(data.opposingPlayers[3].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[3].getPos()[0])<=100):
                data.otherDx=-5
            else:
                data.otherDx=0
            data.opposingPlayers[3].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==2):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[4].getPos()[1])>20):
            if(data.opposingPlayers[4].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[4].getPos()[0])<=100):
                data.otherDx=-5
            else:
                data.otherDx=0
            data.opposingPlayers[4].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[1].getPos()[0])>20):
            if(data.opposingPlayers[1].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[1].getPos()[1])<=100):
                data.otherDy=-5
            else:
                data.otherDy=0
            data.opposingPlayers[1].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==3):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[0].getPos()[1])>20):
            if(data.opposingPlayers[0].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[0].getPos()[0])<=100):
                data.otherDx=5
            else:
                data.otherDx=0
            data.opposingPlayers[0].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[4].getPos()[0])>20):
            if(data.opposingPlayers[4].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[4].getPos()[1])<=100):
                data.otherDy=5
            else:
                data.otherDy=0
            data.opposingPlayers[4].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[7].getPos()[1])>20):
            if(data.opposingPlayers[7].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[7].getPos()[0])<=100):
                data.otherDx=-5
            else:
                data.otherDx=0
            data.opposingPlayers[7].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==4):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[2].getPos()[1])>20):
            if(data.opposingPlayers[2].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[2].getPos()[0])<=100):
                data.otherDx=5
            else:
                data.otherDx=0
            data.opposingPlayers[2].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[3].getPos()[0])>20):
            if(data.opposingPlayers[3].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[3].getPos()[1])<=100):
                data.otherDy=-5
            else:
                data.otherDy=0
            data.opposingPlayers[3].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[7].getPos()[1])>20):
            if(data.opposingPlayers[7].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[7].getPos()[0])<=100):
                data.otherDx=-5
            else:
                data.otherDx=0
            data.opposingPlayers[7].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==5):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[7].getPos()[1])>20):
            if(data.opposingPlayers[7].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[7].getPos()[0])<=100):
                data.otherDx=5
            else:
                data.otherDx=0
            data.opposingPlayers[7].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[6].getPos()[0])>20):
            if(data.opposingPlayers[6].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[6].getPos()[1])<=100):
                data.otherDy=5
            else:
                data.otherDy=0
            data.opposingPlayers[6].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==6):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[7].getPos()[1])>20):
            if(data.opposingPlayers[7].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[7].getPos()[0])<=100):
                data.otherDx=5
            else:
                data.otherDx=0
            data.opposingPlayers[7].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[5].getPos()[0])>20):
            if(data.opposingPlayers[5].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[5].getPos()[1])<=100):
                data.otherDy=-5
            else:
                data.otherDy=0
            data.opposingPlayers[5].move(data.otherDx,data.otherDy,data)
    elif(data.selectedOtherPlayer%8==7):
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[6].getPos()[0])>10):
            if(data.opposingPlayers[6].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[6].getPos()[1])<=100):
                data.otherDy=5
            else:
                data.otherDy=0
            data.opposingPlayers[6].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]-
                    data.opposingPlayers[3].getPos()[0])>10):
            if(data.opposingPlayers[3].getPos()[0]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[0]):
                data.otherDx=-10
            else:
                data.otherDx=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[1]-
                    data.opposingPlayers[3].getPos()[1])<=100):
                data.otherDy=-5
            else:
                data.otherDy=0
            data.opposingPlayers[3].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[4].getPos()[1])>10):
            if(data.opposingPlayers[4].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[4].getPos()[0])<=100):
                data.otherDx=5
            else:
                data.otherDx=0
            data.opposingPlayers[4].move(data.otherDx,data.otherDy,data)
        if(abs(data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]-
                    data.opposingPlayers[5].getPos()[1])>10):
            if(data.opposingPlayers[5].getPos()[1]>
                    data.opposingPlayers[data.selectedOtherPlayer%8].getPos()[1]):
                data.otherDy=-10
            else:
                data.otherDy=10
            if(abs(data.opposingPlayers[data.selectedOtherPlayer].getPos()[0]-
                    data.opposingPlayers[5].getPos()[0])<=100):
                data.otherDx=-5
            else:
                data.otherDx=0
            data.opposingPlayers[5].move(data.otherDx,data.otherDy,data)

def timerFired(data):
    if(data.stage==1):
        data.AI=.75
    elif(data.stage==2):
        data.AI=1
    elif(data.stage==3):
        data.AI=1.25
    if(data.gameState==-4):
        data.stage=0.5
        data.tournament=False
    if(data.gameState<=-2):
        data.selectedPlayer=7
        data.dir=0
        data.time=0
        data.score1=0
        data.score2=0
        data.pPressed=False
        data.ballX=data.width//2
        data.ballY=data.height//2
    if(data.gameState!=-1):
        data.timeCounter+=data.timerDelay
        if(data.timeCounter%1000==0):
            data.time+=1
        if(data.time>=15):
            data.time=15
            data.gameState=2
    moveGKs(data)
    #shoot
    if(len(data.players)!=0 and data.pPressed==True):
        player=data.players[data.selectedPlayer%8]
        if(data.dir!=0):
            player.launchBall(data,data.dir)
    #make sure ball doesn't go off vertically
    if(data.ballY<=50):
        data.pPressed=False
        data.ballY=50
    elif(data.ballY>=data.height-50):
        data.pPressed=False
        data.ballY=data.height-50
    keepTrackofPlayers(data)
    keepTrackofGoal(data)
    if(data.twoPlayer==False):
        if(data.gk2.hasBall(data)):
            closestDistance=data.width
            for player in data.opposingPlayers:
                dist=distance(player.getPos()[0],player.getPos()[1],
                                data.gk2.getPos()[0],data.gk2.getPos()[1])
                if(dist<closestDistance):
                    closestDistance=dist
                    closestPlayer=player
            data.ballX=closestPlayer.getPos()[0]-30
            data.ballY=closestPlayer.getPos()[1]
    if(data.team=="blue" and len(data.players)!=0 and len(data.opposingPlayers)!=0):
        #my (blue) offensive AI
        blueOffensiveAI(data)
        #red defensive AI
        if(data.twoPlayer):
            twoPlayerRedDef(data)
        else:
            onePlayerRedDef(data)
    if(data.team=="red" and len(data.opposingPlayers)!=0 and len(data.players)!=0):
        #blue def
        blueDefensiveAI(data)
        if(data.twoPlayer==False):
            #red off
            onePlayerRedOff(data)
        else:
            twoPlayerRedOff(data)
            
            
def initializeBoard(canvas,data):
    data.fieldPic=PhotoImage(file="soccerfield.gif")
    data.fieldPic=data.fieldPic.zoom(2,2)
    canvas.create_image((0,0),anchor=NW,image=data.fieldPic)

def drawPlayers(canvas, data):
    data.gk.drawPlayer(canvas)
    data.gk2.drawPlayer(canvas)
    for x in range(len(data.players)):
        if x%8 != data.selectedPlayer%8:
            player = data.players[x]
            player.setCol("blue")
            player.drawPlayer(canvas)
    player=data.players[data.selectedPlayer%8]
    player.setCol("black")
    player.drawPlayer(canvas)
    #other team
    if(data.twoPlayer==False):
        for x in range(len(data.opposingPlayers)):
            player = data.opposingPlayers[x]
            player.setCol("red")
            player.drawPlayer(canvas)
    else:
        for x in range(len(data.opposingPlayers)):
            if x%8 != data.selectedOtherPlayer%8:
                player = data.opposingPlayers[x]
                player.setCol("red")
                player.drawPlayer(canvas)
        player=data.opposingPlayers[data.selectedOtherPlayer%8]
        player.setCol("pink")
        player.drawPlayer(canvas)

def initPlayers(canvas,data):
    data.players=[]
    data.gk.drawPlayer(canvas)
    data.gk2.setCol="red" 
    data.gk2.drawPlayer(canvas)
    #defenders
    for i in range(3):
        player=Player(data.width//5,i*data.height//4+data.height//4)
        data.players.append(player)
        player.drawPlayer(canvas)
    #midfielders
    for i in range(2):
        player=Player(data.width//3,i*data.height*2//8+data.height*3//8)
        data.players.append(player)
        player.drawPlayer(canvas)
    #attackers
    for i in range(2):
        player=Player(data.width//2-40,i*data.height*2//3+data.height//6)
        data.players.append(player)
        player.drawPlayer(canvas)
    player=Player(data.width//2-100,data.height//2)
    data.players.append(player)
    player.drawPlayer(canvas)
    player=data.players[data.selectedPlayer%8]
    player.setCol("black")
    player.drawPlayer(canvas)
    #other team
    data.opposingPlayers=[]
    #defenders
    for i in range(3):
        player=Player(data.width*4//5,i*data.height//4+data.height//4)
        data.opposingPlayers.append(player)
        player.drawPlayer(canvas)
    #midfielders
    for i in range(2):
        player=Player(data.width*2//3,i*data.height*2//8+data.height*3//8)
        data.opposingPlayers.append(player)
        player.drawPlayer(canvas)
    #attackers
    for i in range(2):
        player=Player(data.width//2+40,i*data.height*2//3+data.height//6)
        data.opposingPlayers.append(player)
        player.drawPlayer(canvas)
    player=Player(data.width//2+100,data.height//2)
    data.opposingPlayers.append(player)
    player.drawPlayer(canvas)

def redrawAll(canvas, data):
    initializeBoard(canvas,data)
    canvas.create_text(50,20,text="Menu", font="Times 40")
    canvas.create_text(data.width-70,data.height-30,text="Tutorial",font="Times 40")
    if(data.gameState==-5):
        #tutorial screen
        canvas.create_text(data.width//2,70,
                    text="Press M at any time to go back to the Main Menu",
                    font="Times 50", anchor=N, fill="black")
        canvas.create_text(data.width//2,150,text="First Player",
                    font="Times 40", anchor=N, fill="blue")
        canvas.create_text(data.width//2,210,text="Arrow Keys to Move the Selected Player",
                    font="Times 40", anchor=N, fill="blue")
        canvas.create_text(data.width//2,270,text="P to shoot",
                    font="Times 40", anchor=N, fill="blue")
        canvas.create_text(data.width//2,330,
                    text="L to change selected player (to the one closest to the ball)",
                    font="Times 40", anchor=N, fill="blue")
        canvas.create_text(data.width//2,390,
                    text="When GK has the ball, O to pass to nearest player",
                    font="Times 40", anchor=N, fill="blue")
        canvas.create_text(data.width//2,450,text="Second Player",
                    font="Times 40", anchor=N, fill="red")
        canvas.create_text(data.width//2,510,text="WASD to Move the Selected Player",
                    font="Times 40", anchor=N, fill="red")
        canvas.create_text(data.width//2,570,text="X to Shoot",
                    font="Times 40", anchor=N, fill="red")
        canvas.create_text(data.width//2,630,
                    text="Z to change selected player (to the one closest to the ball)",
                    font="Times 40", anchor=N, fill="red")
        canvas.create_text(data.width//2,690,
                    text="When GK has the ball, C to pass to nearest player",
                    font="Times 40", anchor=N, fill="red")
    elif(data.gameState==-4):
        canvas.create_text(data.width//2,data.height//4, text="Quick Game",
                    font="Times 72", anchor=N)
        canvas.create_text(data.width//2,data.height*3//4,text="Tournament",
                    font="Times 72", anchor=N)
    elif(data.gameState==-3):
        #quarter final
        canvas.create_rectangle(data.width//4-75,data.height//2-50,data.width//4+75,
                                    data.height//2+50)
        canvas.create_text(data.width//4,data.height//2-50,text="Quarter",
                                font="Times 40",anchor=N)
        canvas.create_text(data.width//4,data.height//2,text="Finals",
                                font="Times 40",anchor=N)
        canvas.create_line(data.width//4+75,data.height//2,data.width//2-75,
                                    data.height//2)
        #semi final
        canvas.create_rectangle(data.width//2-75,data.height//2-50,data.width//2+75,
                                    data.height//2+50)
        canvas.create_text(data.width//2,data.height//2-50,text="Semi",
                                font="Times 40",anchor=N)
        canvas.create_text(data.width//2,data.height//2,text="Finals",
                                font="Times 40",anchor=N)
        canvas.create_line(data.width//2+75,data.height//2,data.width*3//4-75,
                                    data.height//2)
        #final
        canvas.create_rectangle(data.width*3//4-75,data.height//2-50,
                            data.width*3//4+75,data.height//2+50)
        canvas.create_text(data.width*3//4,data.height//2-20,text="Finals",
                                font="Times 40",anchor=N)
        #helpful text
        canvas.create_text(data.width//2,data.height//4,text="Press N to proceed",
                                font="Times 40", anchor=N)
        #arrow
        data.arrowPic=PhotoImage(file="arrow.gif")
        data.arrowPic=data.arrowPic.subsample(4,4)
        canvas.create_image(((data.stage-0.5)*data.width//4+data.width//4,
                        data.height*3//4),image=data.arrowPic)
    elif(data.gameState==-2):
        canvas.create_text(data.width//4,data.height//2,text="Easy",
                                font="Times 50",anchor=N)
        canvas.create_text(data.width//2,data.height//2,text="Medium",
                                font="Times 50", anchor=N)
        canvas.create_text(data.width*3//4,data.height//2,text="Hard",
                                font="Times 50", anchor=N)                      
    elif(data.gameState==-1):
        canvas.create_text(data.width//4,data.height//2,text="Single Player",
                    font="Times 72", anchor=N)
        canvas.create_text(data.width*3//4,data.height//2,text="2-Player",
                    font="Times 72", anchor=N)
    elif(data.gameState==0):
        initPlayers(canvas,data)
        data.gameState = 1
    else:
        if(data.tournament):
            #draw tournament stage
            if(data.stage==1):
                data.text="Quarter Finals"
            elif(data.stage==2):
                data.text="Semi Finals"
            elif(data.stage==3):
                data.text="Final"
            canvas.create_text(data.width//5,data.height-60,
                                text=data.text,font="Times 50", anchor=N)
        drawPlayers(canvas, data)
        drawBall(canvas,data,data.ballX,data.ballY)
    #draw score and time
    canvas.create_text(data.width//2-150,0,text="Blue: "+str(data.score1),
                    font="Times 50",anchor=N)
    canvas.create_text(data.width//2+150,0,text="Red: "+str(data.score2),
                    font="Times 50", anchor=N)
    canvas.create_text(data.width//2,data.height-55,text="Time: "+str(data.time),
                    font="Times 50", anchor=N)
    if(data.gameState==2):
        canvas.delete(ALL)
        if(data.tournament==False):
            if(data.score1>data.score2):
                canvas.create_text(data.width//2,data.height//2,text="Blue team wins!",
                        font="Times 72", anchor=N)
            elif(data.score2>data.score1):
                canvas.create_text(data.width//2,data.height//2,text="Red team wins!",
                        font="Times 72", anchor=N)
            else:
                canvas.create_text(data.width//2,data.height//2,text="It's a Tie!",
                        font="Times 72", anchor=N)
            canvas.create_text(data.width//2,data.height*3//4,
                        text="Press M to go back to Menu", font="Times 30", anchor=N)
        else:
            if(data.stage==3):
                #if you win the tournament
                if(data.score1>data.score2):
                    canvas.create_rectangle(0,0,data.width,data.height,fill="darkgreen")
                    canvas.create_text(data.width//2,data.height//10,
                            text="You Won the Tournament!",font="Times 72", anchor=N)
                    data.winPic=PhotoImage(file="trophy1.gif")
                    canvas.create_image((data.width//2,data.height//2),image=data.winPic)
                    canvas.create_text(50,20,text="Menu", font="Times 40")
                    canvas.create_text(data.width//2,data.height*4//5,
                        text="Press M to go back to Menu", font="Times 30", anchor=N) 
                else:
                    canvas.create_text(data.width//2,data.height//2,
                            text="Better Luck Next Time",font="Times 72", anchor=N)
                    canvas.create_text(data.width//2,data.height*3//4,
                        text="Press M to go back to Menu", font="Times 30", anchor=N) 
            else:
                if(data.score1>data.score2):
                    canvas.create_text(data.width//2,data.height//2,text="You Win!",
                            font="Times 72", anchor=N)
                    canvas.create_text(data.width//2,data.height*3//4,
                            text="Press N to go to next Stage", font="Times 30", anchor=N)
                else:
                    canvas.create_text(data.width//2,data.height//2,
                            text="Better Luck Next Time",font="Times 72", anchor=N)
                    canvas.create_text(data.width//2,data.height*3//4,
                            text="Press M to go back to Menu", font="Times 30", anchor=N)
            
            
##################
#runner, from the 112 course website
##################
def run(width=1200, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()
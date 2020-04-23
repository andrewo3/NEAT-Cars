import pygame, pickle, os
from sys import exit
from math import hypot

dimensions=(640,360)
WINDOW = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Build Track")
building=False
destroying=False
def distance(point1,point2):
    return hypot(point1[0]-point2[0],point1[1]-point2[1])
class SquareButton(object):
    def __init__(self,x,y,size,action,*params):
        self.pos = (x,y)
        self.size=size
        self.action = action
        self.params=params
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)
        self.lastMouse=False
    def update(self,surface):
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            if not(pygame.mouse.get_pressed()[0]):
                pygame.draw.rect(surface,(128,128,128),self.rect)
            elif pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(surface, (64,64,64), self.rect)
                if self.lastMouse!=pygame.mouse.get_pressed()[0]:
                    self.action(*self.params)
        elif not(self.rect.collidepoint(*pygame.mouse.get_pos())):
            pygame.draw.rect(surface, (192, 192, 192), self.rect)
        self.lastMouse=pygame.mouse.get_pressed()[0]
class RoadSegment(object):
    def __init__(self,start=None,snap=None):
        global dimensions
        self.constructing=True
        if start==None:
            self.bezierPoints=[]
        else:
            self.bezierPoints=[start]
        self.lastMouse=False
        self.allPoints=[]
        self.snap=snap
        self.space=pygame.Surface(dimensions)
        self.space.fill((0,0,0))
    def update(self,surface):
        self.mousePos=pygame.mouse.get_pos()
        if self.snap!=None:
            for i in self.snap:
                if distance(self.mousePos,i)<=15:
                    self.mousePos=i
                    break
        if self.constructing:
            if len(self.bezierPoints)<3:
                self.displayCurve=[i for i in self.bezierPoints]
                self.displayCurve.append(self.mousePos)
                if len(self.displayCurve)==2:
                    pygame.draw.circle(surface, (0, 255, 255), self.displayCurve[1], 10)
                    pygame.draw.line(surface, (0, 255, 255), self.displayCurve[0], self.displayCurve[1], 5)
                    pygame.draw.circle(WINDOW,(128,128,128),self.displayCurve[0],10)
                elif len(self.displayCurve)==3:
                    self.allPoints=[((1-(i/99))*((1-(i/99))*self.displayCurve[0][0]+(i/99)*self.displayCurve[1][0])+(i/99)*((1-(i/99))*self.displayCurve[1][0]+(i/99)*self.displayCurve[2][0]),(1-(i/99))*((1-(i/99))*self.displayCurve[0][1]+(i/99)*self.displayCurve[1][1])+(i/99)*((1-(i/99))*self.displayCurve[1][1]+(i/99)*self.displayCurve[2][1])) for i in range(100)]
                    #for i in range(len(self.allPoints)-1):
                        #pygame.draw.line(surface,(128,128,128),self.allPoints[i],self.allPoints[i+1],20)
                    for i in self.allPoints:
                        pygame.draw.circle(surface, (128, 128, 128), i, 20*dimensions[0]/640)
                    pygame.draw.circle(surface, (0, 255, 255), self.displayCurve[1], 10)
                    pygame.draw.line(surface, (0, 255, 255), self.displayCurve[0], self.displayCurve[1], 5)
                    pygame.draw.line(surface, (0, 255, 255), self.displayCurve[1], self.displayCurve[2], 5)
                if pygame.mouse.get_pressed()[0] and self.lastMouse!=pygame.mouse.get_pressed()[0]:
                    self.bezierPoints.append(self.mousePos)
            else:
                self.constructing=False
                for i in self.allPoints:
                    pygame.draw.circle(self.space, (255,255,255), i, 20*dimensions[0]/640)
        else:
            if self.snap!=None and not(self.bezierPoints[2] in self.snap):
                self.snap.append(self.bezierPoints[2])
            if self.snap!=None and not(self.bezierPoints[0] in self.snap):
                self.snap.append(self.bezierPoints[0])
            self.allPoints = [((1 - (i / 99)) * ((1 - (i / 99)) * self.bezierPoints[0][0] + (i / 99) * self.bezierPoints[1][0]) + (i / 99) * ((1 - (i / 99)) * self.bezierPoints[1][0] + (i / 99) * self.bezierPoints[2][0]), (1 - (i / 99)) * ((1 - (i / 99)) * self.bezierPoints[0][1] + (i / 99) * self.bezierPoints[1][1]) + (i / 99) * ((1 - (i / 99)) * self.bezierPoints[1][1] + (i / 99) * self.bezierPoints[2][1])) for i in range(100)]
            #for i in range(len(self.allPoints) - 1):
                #pygame.draw.line(surface, (128, 128, 128), self.allPoints[i], self.allPoints[i + 1], 20)
            for i in self.allPoints:
                pygame.draw.circle(surface,(128,128,128),i,20*dimensions[0]/640)
        self.lastMouse=pygame.mouse.get_pressed()[0]
class Road(object):
    def __init__(self):
        self.completed=False
        self.segments=[]
        self.lastMouse=False
        self.start=None
        self.looped=False
        self.snaps=[]
    def isLooped(self):
        self.changed=True
        loop=False
        try:
            self.loop=[[i for i in self.segments if i.bezierPoints[0]==self.start][0]]
        except IndexError:
            return False
        while loop==False and self.changed==True:
            self.changed=False
            for i in self.segments:
                if i.bezierPoints[0]==self.loop[len(self.loop)-1].bezierPoints[2] and not(i in self.loop):
                    self.loop.append(i)
                    self.changed=True
                    break
            if self.loop[len(self.loop)-1].bezierPoints[2]==self.loop[0].bezierPoints[0]:
                loop=True
        return loop
    def update(self,surface):
        global buildButton, destroyButton,building,destroying
        self.mousePos = pygame.mouse.get_pos()
        if building:
            if self.snaps != None:
                for i in self.snaps:
                    if distance(self.mousePos, i) <= 15:
                        self.mousePos = i
                        break
            if self.looped==False:
                pygame.draw.circle(surface,(128,128,128),self.mousePos,20*dimensions[0]/640)
            if len([i for i in self.segments if i.bezierPoints[0]==self.start])==0:
                if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[0] != self.lastMouse and not(buildButton.rect.collidepoint(*self.mousePos) or destroyButton.rect.collidepoint(*self.mousePos)):
                    self.segments.append(RoadSegment(snap=self.snaps))
                    self.start=pygame.mouse.get_pos()
            elif len(self.segments)>0:
                if len(self.segments[len(self.segments)-1].bezierPoints)==3:
                    if (len(self.segments)>1 and not(self.isLooped())) or len(self.segments)==1:
                        self.looped=False
                        if self.segments[len(self.segments)-1].constructing==False:
                            if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[0]!=self.lastMouse and not(buildButton.rect.collidepoint(*self.mousePos) or destroyButton.rect.collidepoint(*self.mousePos)):
                                self.segments.append(RoadSegment(snap=self.snaps))
                    else:
                        self.looped=True
            for i in self.segments:
                i.update(surface)
        else:
            self.remove=[]
            for i in self.segments:
                if i.constructing==True:
                    self.remove.append(i)
            for i in self.remove:
                self.segments.remove(i)
            for i in self.segments:
                for x in i.allPoints:
                    pygame.draw.circle(surface,(128,128,128),x,20*dimensions[0]/640)
        if destroying:
            self.destroy=None
            for i in self.segments:
                if i.space.get_at(self.mousePos)==(255,255,255):
                    self.destroy=i
                    for x in i.allPoints:
                        pygame.draw.circle(surface, (255,0,0), x, 20*dimensions[0]/640)
                    break
            if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[0] != self.lastMouse and self.destroy!=None:
                if self.destroy.bezierPoints[0] in self.snaps:
                    self.snaps.remove(self.destroy.bezierPoints[0])
                if self.destroy.bezierPoints[2] in self.snaps:
                    self.snaps.remove(self.destroy.bezierPoints[2])
                self.segments.remove(self.destroy)
        #print(len([i for i in self.segments if i.bezierPoints[0]==self.start]),self.start)
        if len([i for i in self.segments if i.bezierPoints[0]==self.start])==0:
            self.start=None
        if self.start != None:
            pygame.draw.circle(WINDOW, (255, 255, 0), self.start, 10)
        self.lastMouse = pygame.mouse.get_pressed()[0]
def build():
    global building,destroying
    if building==False:
        building=True
        destroying=False
    else:
        building=False
def destroy():
    global building, destroying
    if destroying == False:
        destroying = True
        building = False
    else:
        destroying = False
def save(road_):
    finalData=[dimensions,[i.bezierPoints for i in road_.segments],road_.start]
    data=pickle.dumps(finalData)
    number=0
    if not(os.path.exists('Roads')):
        os.mkdir('Roads')
    while str(number)+".road" in os.listdir('Roads'):
        number+=1
    file=open("Roads/"+str(number)+".road","wb")
    file.write(data)
    file.close()
road = Road()
buildButton=SquareButton(0,0,100,build)
destroyButton=SquareButton(dimensions[0]-100,0,100,destroy)
saveButton=SquareButton(int(round(dimensions[0]/2-50)),0,100,save,road)
while True:
    road.update(WINDOW)
    buildButton.update(WINDOW)
    destroyButton.update(WINDOW)
    if building:
        pygame.draw.circle(WINDOW,(0,128,0),pygame.mouse.get_pos(),5)
    elif destroying:
        pygame.draw.circle(WINDOW, (128, 0, 0), pygame.mouse.get_pos(), 5)
    if building or destroying:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
    if road.looped:
        saveButton.update(WINDOW)
    #print(building,destroying)
    pygame.display.update()
    WINDOW.fill((0,255,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
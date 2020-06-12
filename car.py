import pygame
from math import sin, cos, radians,atan2, hypot, pi

class Car(object):
    def __init__(self,pos,color,rotation=90,scale=1):
        self.pos=[]
        self.wheelRot=0
        self.speed=0
        self.framesStill=0
        self.testRot=False
        self.sensors=[]
        self.hardCoded=True
        self.rotation=rotation-90
        self.maxSteer=65
        self.camRot=0
        if color==(1,0,0):
            self.color=(0,0,0)
        else:
            self.color=color
        self.origDim=(10*scale,20*scale)
        self.center=list(pos)
        self.surface=pygame.Surface(self.origDim)
        #self.surface=pygame.Surface.convert(self.surface)
        self.surface.fill(self.color)
        self.alpha=pygame.Surface(self.origDim)
        self.origRot=pygame.Surface([self.origDim[0]*9/8+self.origDim[1]/3,self.origDim[1]])
        self.rotSurf=pygame.transform.rotate(self.surface,self.rotation)
        self.rotSurf.set_colorkey((1,0,0))
        self.noScaleSurface = self.surface.copy()
        #self.centerCar()
    def scaleOffset(self,point,zoom_, offset_, dimensions,rotation=0):
        rad = radians(rotation)
        # print(rad)
        noRot = [(point[z] + offset_[z] - dimensions[z] / 2) * zoom_ + dimensions[z] / 2 for z in
                 range(len(point))]
        noRot[0] -= dimensions[0] / 2
        noRot[1] -= dimensions[1] / 2
        noRot[1] = -noRot[1]
        newPoint = [0, 0]
        newPoint[0] = cos(atan2(noRot[1], noRot[0]) + rad) * hypot(noRot[0], noRot[1])
        newPoint[1] = sin(atan2(noRot[1], noRot[0]) + rad) * hypot(noRot[0], noRot[1])
        newPoint[0] += dimensions[0] / 2
        newPoint[1] = -newPoint[1]
        newPoint[1] += dimensions[1] / 2
        return newPoint
    def setSensors(self,num,trackSurf):
        self.sensors=[]
        for i in range(num):
            currentPos=list(self.center)
            distance=0
            end=False
            while not(end):
                intPos=[int(round(x)) for x in currentPos]
                if intPos[0]>0 and intPos[0]<trackSurf.get_width() and intPos[1]>0 and intPos[1]<trackSurf.get_height():
                    if trackSurf.get_at(intPos)==(255,255,255):
                        currentPos[0]+=cos((2*pi)/num*i+radians(-self.rotation))
                        currentPos[1]+=sin((2*pi)/num*i+radians(-self.rotation))
                    else:
                        end=True
                else:
                    end=True
                distance+=1
            self.sensors.append([distance,currentPos[::]])
    def drawSensors(self,surface,scale,offset,camRot=0,print_=True):
        for i in self.sensors:
            pygame.draw.line(surface,(255,255,255),self.scaleOffset(self.center,scale,offset,surface.get_size(),camRot),self.scaleOffset(i[1],scale,offset,surface.get_size(),camRot))
        if print_==True:
            print([i[0] for i in self.sensors])
    def drawPOV(self,surface,scale,offset,camRot=0,print_=True):
        for i in self.sensors:
            pygame.draw.circle(surface,(255,255,255),self.scaleOffset(i[1],scale,offset,surface.get_size(),camRot),1*scale)
        if print_==True:
            print([i[0] for i in self.sensors])
    def centerCar(self,surface,offsetPoint):
        self.pos = [offsetPoint[0] - surface.get_size()[0]/2, offsetPoint[1] - surface.get_size()[1]/2]
    def makeCarFrame(self,surface,scale,offset):
        self.dimensions=[int(round(i*scale)) for i in self.origDim]
        self.alpha=pygame.Surface(self.dimensions)
        self.alpha.set_colorkey(self.color)
        self.alpha.fill((1,0,0))
        self.surface=pygame.Surface(self.dimensions)
        self.surface.set_colorkey((1, 0, 0))
        self.surface.fill(self.color)
        pygame.draw.rect(self.surface,(1,0,0),pygame.Rect(0,0,int(round(self.dimensions[0]/4)),int(round(self.dimensions[0]/4))))
        pygame.draw.rect(self.surface, (1, 0, 0),pygame.Rect(self.dimensions[0]-int(round(self.dimensions[0] / 4)), 0, int(round(self.dimensions[0] / 4)), int(round(self.dimensions[0] / 4))))
        pygame.draw.circle(self.surface,self.color,(int(round(self.dimensions[0] / 4)),int(round(self.dimensions[0] / 4))),int(round(self.dimensions[0] / 4)))
        pygame.draw.circle(self.surface, self.color,
                           (self.dimensions[0]-int(round(self.dimensions[0] / 4)), int(round(self.dimensions[0] / 4))),
                           int(round(self.dimensions[0] / 4)))
        pygame.draw.rect(self.surface, (1, 0, 0),
                         pygame.Rect(0, self.dimensions[1]-int(round(self.dimensions[0] / 4)), int(round(self.dimensions[0] / 4)), int(round(self.dimensions[0] / 4))))
        pygame.draw.rect(self.surface, (1, 0, 0),
                         pygame.Rect(self.dimensions[0] - int(round(self.dimensions[0] / 4)), self.dimensions[1]-int(round(self.dimensions[0] / 4)),
                                     int(round(self.dimensions[0] / 4)), int(round(self.dimensions[0] / 4))))
        pygame.draw.circle(self.surface, self.color,
                           (int(round(self.dimensions[0] / 4)), self.dimensions[1]-int(round(self.dimensions[0] / 4))),
                           int(round(self.dimensions[0] / 4)))
        pygame.draw.circle(self.surface, self.color,
                           (
                           self.dimensions[0] - int(round(self.dimensions[0] / 4)), self.dimensions[1]-int(round(self.dimensions[0] / 4))),
                           int(round(self.dimensions[0] / 4)))
        self.alpha.blit(self.surface,(0,0))
        self.addHeadlights()
        self.addWindows()
        self.addWheels()
    def draw(self,surface,scale,offset,camRot=0):
        self.camRot=camRot
        self.makeCarFrame(surface, scale, offset)
        self.rotSurf = pygame.Surface(pygame.transform.rotate(self.surface, self.rotation+camRot).get_size())
        self.rotSurf.set_colorkey((1, 0, 0))
        self.surface = pygame.Surface.convert(self.surface)
        self.rotSurf.blit(pygame.transform.rotate(self.surface, self.rotation+camRot), (0, 0))
        self.surface = pygame.Surface.convert(self.surface)
        self.centerCar(self.rotSurf,self.scaleOffset(self.center, scale, offset, surface.get_size(), camRot))
        surface.blit(self.rotSurf,self.pos)
    def update(self,keys,trackSurf,numSensors=8):
        if keys[0]:
            if self.speed<10:
                self.speed+=0.3
        elif keys[1]:
            if self.speed>0:
                self.speed-=0.6
        if self.speed<0:
            self.speed=0
        if keys[2]:
            self.wheelRot=20
            if self.testRot==False:
                if self.speed<10:
                    self.rotation+=self.speed*2
                else:
                    self.rotation+=20
            else:
                self.rotation+=20
        if keys[3]:
            self.wheelRot=-20
            if self.testRot==False:
                if self.speed<10:
                    self.rotation-=self.speed*2
                else:
                    self.rotation-=20
            else:
                self.rotation-=20
        if not(keys[2]) and not(keys[3]):
            self.wheelRot=0
        self.center[0]-=sin(radians(-(self.rotation+180)))*self.speed
        self.center[1]+=cos(radians(-(self.rotation+180)))*self.speed
        self.setSensors(numSensors, trackSurf)
    def addHeadlights(self):
        pygame.draw.circle(self.surface, (255, 255, 0), (0, 0), int(round(self.dimensions[0] / 4)))
        pygame.draw.circle(self.surface, (255, 255, 0), (self.dimensions[0], 0), int(round(self.dimensions[0] / 4)))
        pygame.draw.circle(self.surface, (128, 0, 0), (0, self.dimensions[1]), int(round(self.dimensions[0] / 4)))
        pygame.draw.circle(self.surface, (128, 0, 0), (self.dimensions[0], self.dimensions[1]),
                           int(round(self.dimensions[0] / 4)))
        self.surface.blit(self.alpha, (0, 0))
    def addWindows(self):
        pygame.draw.rect(self.surface, (209, 240, 255),
                         pygame.Rect(int(round(self.dimensions[0] / 16)), int(round(self.dimensions[1] / 4)),
                                     self.dimensions[0] - int(round(self.dimensions[0] / 8)),
                                     int(round(self.dimensions[1] / 16))))
        pygame.draw.rect(self.surface, (209, 240, 255),
                         pygame.Rect(int(round(self.dimensions[0] / 16)), int(round(3*self.dimensions[1] / 4-self.dimensions[1]/8)),
                                     self.dimensions[0] - int(round(self.dimensions[0] / 8)),
                                     int(round(self.dimensions[1] / 16))))
        pygame.draw.line(self.surface, (0, 0, 0), (
        int(round(self.dimensions[0] / 16)), int(round(self.dimensions[1] / 4 + self.dimensions[1] / 16))), (
                         int(round(self.dimensions[0] / 16)),
                         int(round(3 * self.dimensions[1] / 4 - self.dimensions[1] / 8))))
        pygame.draw.line(self.surface, (0, 0, 0), (
        int(round(self.dimensions[0] / 16))+self.dimensions[0] - int(round(self.dimensions[0] / 8)), int(round(self.dimensions[1] / 4 + self.dimensions[1] / 16))), (
                         int(round(self.dimensions[0] / 16))+self.dimensions[0] - int(round(self.dimensions[0] / 8)),
                         int(round(3 * self.dimensions[1] / 4 - self.dimensions[1] / 8))))
        pygame.draw.line(self.surface,(0,0,0),(
        int(round(self.dimensions[0] / 16)), int(round(self.dimensions[1] / 4 + self.dimensions[1] / 16))),(0,int(round(self.dimensions[1] / 4))))
        pygame.draw.line(self.surface,(0,0,0),(int(round(self.dimensions[0] / 16)),int(round(3 * self.dimensions[1] / 4 - self.dimensions[1] / 8))),(0,int(round(3 * self.dimensions[1] / 4 - self.dimensions[1] / 8))+int(round(self.dimensions[1] / 16))))
        pygame.draw.line(self.surface, (0, 0, 0), (
            self.dimensions[0] -int(round(self.dimensions[0] / 16)), int(round(self.dimensions[1] / 4 + self.dimensions[1] / 16))),
                         (self.dimensions[0], int(round(self.dimensions[1] / 4))))
        pygame.draw.line(self.surface, (0, 0, 0), (
        self.dimensions[0]-int(round(self.dimensions[0] / 16)), int(round(3 * self.dimensions[1] / 4 - self.dimensions[1] / 8))), (self.dimensions[0], int(
            round(3 * self.dimensions[1] / 4 - self.dimensions[1] / 8)) + int(round(self.dimensions[1] / 16))))
    def addWheels(self):
        oldSurface=self.surface.copy()
        self.surface=pygame.Surface((int(round(self.dimensions[0]*9/8+self.dimensions[1] / 3)),self.dimensions[1]))
        self.surface.set_colorkey((1, 0, 0))
        wheel=pygame.Surface((int(round(self.dimensions[0] / 16)),
                                     int(round(self.dimensions[1] / 6))))
        wheel.fill((0,0,0))
        if not(wheel.get_size()[0]==0 or wheel.get_size()[1]==0):
            rotatedWheel=pygame.transform.rotate(wheel,self.wheelRot)
            self.surface.blit(rotatedWheel,(int(round(self.dimensions[0]/32))-rotatedWheel.get_width()/2+self.dimensions[1] / 6,int(round(self.dimensions[1]/8+self.dimensions[1]/12))-rotatedWheel.get_height()/2))
            self.surface.blit(rotatedWheel, (int(round(self.dimensions[0] / 32)) - rotatedWheel.get_width() / 2+self.dimensions[1] / 6+self.dimensions[0]+self.dimensions[0] / 16, int(
                round(self.dimensions[1] / 8 + self.dimensions[1] / 12)) - rotatedWheel.get_height() / 2))
            #back wheels
            pygame.draw.rect(self.surface, (0, 0, 0),
                             pygame.Rect(self.dimensions[1] / 6, int(round(7*self.dimensions[1] / 8-self.dimensions[1]/6)), int(round(self.dimensions[0] / 16)),
                                         int(round(self.dimensions[1] / 6))))
            pygame.draw.rect(self.surface, (0, 0, 0),
                             pygame.Rect(int(round(self.dimensions[0]*8.5/8+self.dimensions[1] / 6)), int(round(7 * self.dimensions[1] / 8 - self.dimensions[1] / 6)),
                                         int(round(self.dimensions[0] / 16)),
                                         int(round(self.dimensions[1] / 6))))
        self.surface.blit(oldSurface, (int(round(self.dimensions[0] / 16))+self.dimensions[1] / 6, 0))
    def reset(self,pos,rotation=90,scale=1):
        self.__init__(pos,self.color,rotation,scale)
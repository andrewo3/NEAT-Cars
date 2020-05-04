import pygame
from math import sin, cos, tan, radians

class Car(object):
    def __init__(self,pos,color,rotation=90,scale=1):
        self.pos=[]
        self.wheelRot=0
        self.speed=0
        self.hardCoded=True
        self.rotation=rotation-90
        self.maxSteer=65
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
        #self.centerCar()
    def centerCar(self,camRot):
        self.pos = [self.center[0] - (pygame.transform.rotate(self.origRot,self.rotation+camRot).get_size()[0])/2, self.center[1] - pygame.transform.rotate(self.origRot,self.rotation+camRot).get_size()[1]/2]
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
        self.makeCarFrame(surface, scale, offset)
        self.rotSurf = pygame.Surface(pygame.transform.rotate(self.surface, self.rotation+camRot).get_size())
        self.rotSurf.set_colorkey((1, 0, 0))
        self.surface = pygame.Surface.convert(self.surface)
        self.rotSurf.blit(pygame.transform.rotate(self.surface, self.rotation+camRot), (0, 0))
        self.surface = pygame.Surface.convert(self.surface)
        self.centerCar(camRot)
        surface.blit(self.rotSurf,
                     [(self.pos[i] + offset[i] - surface.get_size()[i] / 2) * scale + surface.get_size()[i] / 2 for i in
                      range(len(self.pos))])
    def update(self,keys):
        if keys[pygame.K_w]:
            if self.speed<10:
                self.speed+=0.3
        elif keys[pygame.K_s]:
            if self.speed>0:
                self.speed-=0.6
        if self.speed<0:
            self.speed=0
        if keys[pygame.K_a]:
            self.wheelRot=20
            self.rotation+=3*self.speed/2
        elif keys[pygame.K_d]:
            self.wheelRot=-20
            self.rotation-=3*self.speed/2
        else:
            self.wheelRot=0
        self.center[0]-=sin(radians(-(self.rotation+180)))*self.speed
        self.center[1]+=cos(radians(-(self.rotation+180)))*self.speed
        None
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
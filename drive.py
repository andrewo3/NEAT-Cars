import pygame, sys, pickle
from math import e,log, atan2, sin, cos, pi, floor, radians
from car import Car
from random import randint

dimensions=(640,360)
WINDOW = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Drive car lol")
road=4
roadFile=open('Roads/'+str(road)+'.road','rb')
byteList=b''
for i in roadFile.readlines():
    byteList+=i
trackDim=pickle.loads(byteList)[0]
segments=pickle.loads(byteList)[1]
start=pickle.loads(byteList)[2]
offset=[0,0]
def sigmoid(x,scale):
    return (e**x)/((e**x)+1)*scale+0.5
def bezierCurve(res,*pointlist):
    allPoints = [((1 - (i / res)) * ((1 - (i / res)) * pointlist[0][0] + (i / res) * pointlist[1][0]) + (i / res) * ((1 - (i / res)) * pointlist[1][0] + (i / res) * pointlist[2][0]),(1 - (i / res)) * ((1 - (i / res)) * pointlist[0][1] + (i / res) * pointlist[1][1]) + (i / res) * ((1 - (i / res)) * pointlist[1][1] + (i / res) * pointlist[2][1])) for i in range(res+1)]
    return allPoints
def bezFirstDer(res,*pointlist):
    allPoints = [tuple([2*(1-i/res)*(pointlist[1][x]-pointlist[0][x])+2*(i/res)*(pointlist[2][x]-pointlist[1][x]) for x in range(2)]) for i in range(res + 1)]
    return allPoints
allBezierPoints=[bezierCurve(100,*i) for i in segments]
lastMouse=False
zoom=-log(7,e)
#zoom=2.054
zoom=6
#offset=[130,4]
offset=[0,0]
sigmoidScale=4
derAng=[[atan2(x[0],x[1]) for x in bezFirstDer(100,*i)] for i in segments]
edge1=[]
edge2=[]
followCar=True
cameraRotation=0
trig={0:cos,1:lambda x: -sin(x)}
for i in range(len(derAng)):
    for x in range(len(derAng[i])):
        edge1.append([allBezierPoints[i][x][z]+trig[z](derAng[i][x]+pi)*20 for z in range(2)])
        edge2.append([allBezierPoints[i][x][z]-trig[z](derAng[i][x]+pi)*20 for z in range(2)])
def scaleOffset(point,zoom_,offset_,rotation=0):
    global sigmoidScale,dimensions
    rad=radians(rotation)
    print(rad)
    noRot=[(point[z]+offset_[z]-dimensions[z]/2)*sigmoid(zoom_,sigmoidScale)+dimensions[z]/2 for z in range(len(point))]
    '''noRot[0]-=dimensions[0]/2
    noRot[1]-=dimensions[1]/2
    noRot[0]=noRot[0]*cos(rad)+noRot[1]*sin(rad)
    noRot[1]=noRot[1]*cos(rad)-noRot[0]*sin(rad)
    noRot[0]+=dimensions[0]/2
    noRot[1]-=dimensions[1]/2
    noRot[1]=-noRot[1]'''
    return noRot
def onScreen(pos,leniance=0):
    global dimensions
    x=pos[0]
    y=pos[1]
    if x>=0-leniance and x<dimensions[0]+leniance and y>=0-leniance and y<dimensions[1]+leniance:
        return True
    else:
        return False
#print(atan2(*(bezFirstDer(100,*([i for i in segments if i[0]==start])[0])[0][::-1]))/(pi)*180)
redCar=Car(start,(255,0,0),rotation=atan2(*([bezFirstDer(100,*([i for i in segments if i[0]==start])[0])[0][x]*((-1)**x) for x in range(2)][::-1]))/(pi)*180,scale=trackDim[0]/640)
#cars=[Car([start[0]+floor(i/10)*15,start[1]+i%10*30],[randint(0,255) for i in range(3)],scale=trackDim[0]/640) for i in range(100)]
while True:
    rel=pygame.mouse.get_rel()
    if not(followCar):
        if pygame.mouse.get_pressed()[0]:
            offset[0]-=rel[0]
            offset[1]-=rel[1]
    else:
        cameraRotation+=1
        #zoom=6
        offset[0]=(offset[0]+(dimensions[0]/2-redCar.center[0]))/2
        offset[1]=(offset[1]+(dimensions[1]/2-redCar.center[1]))/2
    for i in allBezierPoints:
        for x in i:
            if onScreen(scaleOffset(x,zoom,offset,cameraRotation),20*trackDim[0]/640*sigmoid(zoom,sigmoidScale)):
                pygame.draw.circle(WINDOW,(128,128,128),scaleOffset(x,zoom,offset,cameraRotation),20*trackDim[0]/640*sigmoid(zoom,sigmoidScale))
    pygame.draw.lines(WINDOW,(255,255,255),False,[scaleOffset(i,zoom,offset,cameraRotation) for i in edge1],int(round(1*sigmoid(zoom,sigmoidScale))))
    pygame.draw.lines(WINDOW, (255,255,255),False,[scaleOffset(i, zoom, offset,cameraRotation) for i in edge2],int(round(1*sigmoid(zoom,sigmoidScale))))
    #pygame.draw.circle(WINDOW,(255,255,0),[(start[i]+offset[i]-dimensions[i]/2)*sigmoid(zoom,sigmoidScale)+dimensions[i]/2 for i in range(len(start))],10*trackDim[0]/640*sigmoid(zoom,sigmoidScale))
    redCar.update(pygame.key.get_pressed())
    if onScreen(scaleOffset(redCar.center,zoom,offset,cameraRotation),20):
        redCar.draw(WINDOW,sigmoid(zoom,sigmoidScale),offset,cameraRotation)
    '''for i in cars:
        i.update()
        if onScreen(i.pos,20):
            i.draw(WINDOW,sigmoid(zoom,sigmoidScale),offset)'''
    '''rotation=pygame.display.get_surface()
    rotation=pygame.transform.rotate(rotation,cameraRotation)
    WINDOW.fill((0,0,0))
    WINDOW.blit(rotation,(-(rotation.get_size()[0]-dimensions[0])/2,-(rotation.get_size()[1]-dimensions[1])/2))'''
    pygame.display.update()
    WINDOW.fill((0,255,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEWHEEL:
            zoom-=event.y
            if zoom<-6:
                zoom=-6
            elif zoom>6:
                zoom=6
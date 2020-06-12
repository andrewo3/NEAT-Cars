import pygame, sys, pickle, neat
from math import e,log, atan2, sin, cos, pi, radians, hypot
from car import Car
from random import randint
from time import time

dimensions=(640,360)
WINDOW = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Drive car lol")
saveAsGo=False
def sigmoid(x,scale):
    return (e**x)/((e**x)+1)*scale+0.5
def bezierCurve(res,*pointlist):
    allPoints = [((1 - (i / res)) * ((1 - (i / res)) * pointlist[0][0] + (i / res) * pointlist[1][0]) + (i / res) * ((1 - (i / res)) * pointlist[1][0] + (i / res) * pointlist[2][0]),(1 - (i / res)) * ((1 - (i / res)) * pointlist[0][1] + (i / res) * pointlist[1][1]) + (i / res) * ((1 - (i / res)) * pointlist[1][1] + (i / res) * pointlist[2][1])) for i in range(res+1)]
    return allPoints
def bezFirstDer(res,*pointlist):
    allPoints = [tuple([2*(1-i/res)*(pointlist[1][x]-pointlist[0][x])+2*(i/res)*(pointlist[2][x]-pointlist[1][x]) for x in range(2)]) for i in range(res + 1)]
    return allPoints
lastMouse=False
sigmoidScale = 4
#zoom=-6
#zoom=2.054
#zoom=6
#offset=[130,4]
def scaleOffset(point,zoom_,offset_,rotation=0):
    global sigmoidScale,dimensions
    rad=radians(rotation)
    #print(rad)
    noRot=[(point[z]+offset_[z]-dimensions[z]/2)*sigmoid(zoom_,sigmoidScale)+dimensions[z]/2 for z in range(len(point))]
    noRot[0]-=dimensions[0]/2
    noRot[1]-=dimensions[1]/2
    noRot[1]=-noRot[1]
    newPoint=[0,0]
    newPoint[0]=cos(atan2(noRot[1],noRot[0])+rad)*hypot(noRot[0],noRot[1])
    newPoint[1]=sin(atan2(noRot[1],noRot[0])+rad)*hypot(noRot[0],noRot[1])
    newPoint[0]+=dimensions[0]/2
    newPoint[1]=-newPoint[1]
    newPoint[1]+=dimensions[1]/2
    return newPoint
def onScreen(pos,leniance=0):
    global dimensions
    x=pos[0]
    y=pos[1]
    if x>=0-leniance and x<dimensions[0]+leniance and y>=0-leniance and y<dimensions[1]+leniance:
        return True
    else:
        return False
def fitness(genomes,config):
    global dimensions, sigmoidScale, saveAsGo
    display=True
    if saveAsGo:
        bestGenome=genomes[0][1]
    road = randint(0,12)
    roadFile = open('Roads/' + str(road) + '.road', 'rb')
    byteList = b''
    for i in roadFile.readlines():
        byteList += i
    trackDim = pickle.loads(byteList)[0]
    segments = pickle.loads(byteList)[1]
    start = pickle.loads(byteList)[2]
    allBezierPoints = [bezierCurve(100, *i) for i in segments]
    zoom = -log(7, e)
    offset = [0, 0]
    edge1 = []
    edge2 = []
    derAng = [[atan2(x[0], x[1]) for x in bezFirstDer(100, *i)] for i in segments]
    trig = {0: cos, 1: lambda x: -sin(x)}
    for i in range(len(derAng)):
        for x in range(len(derAng[i])):
            edge1.append([allBezierPoints[i][x][z] + trig[z](derAng[i][x] + pi) * 20 for z in range(2)])
            edge2.append([allBezierPoints[i][x][z] - trig[z](derAng[i][x] + pi) * 20 for z in range(2)])
    trackSurf=pygame.Surface(dimensions)
    trackSurf.fill((0,0,0))
    for i in allBezierPoints:
        for x in i:
            pygame.draw.circle(trackSurf, (255,255,255), x, 20 * trackDim[0] / 640)
    #testRot=[dimensions[0]/2,0]
    limitFps=pygame.time.Clock()
    running=True
    followCar = False
    cameraRotation = 0
    currentCar=0
    nets = []
    ge = []
    cars = []
    for id,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(start, [randint(0, 255) for a in range(3)], rotation=atan2(*(
        [bezFirstDer(100, *([i for i in segments if i[0] == start])[0])[0][x] * ((-1) ** x) for x in range(2)][
        ::-1])) / (pi) * 180, scale=trackDim[0] / 640))
        g.fitness=0
        ge.append(g)
    for car in cars:
        car.update([0,0,0,0], trackSurf, 8)
    frames=0
    while running:
        rel=pygame.mouse.get_rel()
        if display:
            if not(followCar):
                if pygame.mouse.get_pressed()[0]:
                    distance=hypot(rel[0],rel[1])
                    offset[0]-=cos(atan2(rel[1],rel[0])+radians(cameraRotation))*distance
                    offset[1]-=sin(atan2(rel[1],rel[0])+radians(cameraRotation))*distance
                if pygame.mouse.get_pressed()[1]:
                    cameraRotation+=rel[0]
            else:
                '''if pygame.mouse.get_pressed()[0]:
                    cameraRotation+=1'''
                cameraRotation=-cars[currentCar].rotation
                #zoom=6
                offset[0]=(dimensions[0]/2-cars[currentCar].center[0])
                offset[1]=(dimensions[1]/2-cars[currentCar].center[1])
                #offset[0]=(offset[0]+(dimensions[0]/2-car.center[0]))/2
                #offset[1]=(offset[1]+(dimensions[1]/2-car.center[1]))/2
            #draw track
            for i in allBezierPoints:
                for x in i:
                    if onScreen(scaleOffset(x,zoom,offset,cameraRotation),20*trackDim[0]/640*sigmoid(zoom,sigmoidScale)):
                        pygame.draw.circle(WINDOW,(128,128,128),scaleOffset(x,zoom,offset,cameraRotation),20*trackDim[0]/640*sigmoid(zoom,sigmoidScale))
        #pygame.draw.circle(WINDOW,(255,255,0),[(start[i]+offset[i]-dimensions[i]/2)*sigmoid(zoom,sigmoidScale)+dimensions[i]/2 for i in range(len(start))],10*trackDim[0]/640*sigmoid(zoom,sigmoidScale))
        #userInput
        '''allKeys = [pygame.key.get_pressed()[pygame.K_w]]
        allKeys.append(pygame.key.get_pressed()[pygame.K_s])
        allKeys.append(pygame.key.get_pressed()[pygame.K_a])
        allKeys.append(pygame.key.get_pressed()[pygame.K_d])'''
        for index,car in enumerate(cars):
            if saveAsGo:
                if ge[index].fitness>bestGenome.fitness:
                    bestGenome=ge[index]
            allKeys = []
            inputs=[i[0] for i in car.sensors]
            inputs.append(car.speed)
            output = nets[index].activate(inputs)
            for i in output:
                allKeys.append(i>0.5)
            if allKeys[0]==False:
                #print(car.framesStill)
                car.framesStill+=1
                ge[index].fitness -= 5
            else:
                car.framesStill=0
            lastPos=list(car.center)[::]
            car.update(allKeys,trackSurf,8)
            ge[index].fitness+=hypot(lastPos[0]-car.center[0],lastPos[1]-car.center[1])
            ge[index].fitness+=0.1
            if len(cars)>0:
                if ge[index].fitness>10000:
                    cars.pop(index)
                    nets.pop(index)
                    ge.pop(index)
            intCenter=[int(round(i)) for i in car.center]
            if intCenter[0]>0 and intCenter[0]<trackSurf.get_width() and intCenter[1]>0 and intCenter[1]<trackSurf.get_height():
                if trackSurf.get_at(intCenter)!=(255,255,255):
                    cars.pop(index)
                    nets.pop(index)
                    ge.pop(index)
                    #car.reset(start,rotation=atan2(*([bezFirstDer(100,*([i for i in segments if i[0]==start])[0])[0][x]*((-1)**x) for x in range(2)][::-1]))/(pi)*180,scale=trackDim[0]/640)
            else:
                cars.pop(index)
                nets.pop(index)
                ge.pop(index)
            if onScreen(scaleOffset(car.center, zoom, offset, cameraRotation), 20) and display:
                car.draw(WINDOW, sigmoid(zoom, sigmoidScale), offset, cameraRotation)
            if car.framesStill>=200:
                cars.pop(index)
                nets.pop(index)
                ge.pop(index)
        if len(cars)>0 and display:
            cars[currentCar].drawPOV(WINDOW, sigmoid(zoom, sigmoidScale), offset, cameraRotation,False)
        '''for i in cars:
            i.update()
            if onScreen(i.pos,20):
                i.draw(WINDOW,sigmoid(zoom,sigmoidScale),offset)'''
        frames+=1
        if display:
            pygame.display.update()
            #limitFps.tick(30)
            WINDOW.fill((0,255,0))
        for event in pygame.event.get():
            if event.type==pygame.MOUSEWHEEL and display:
                zoom-=event.y
                if zoom<-6:
                    zoom=-6
                elif zoom>6:
                    zoom=6
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c and display:
                    if followCar:
                        followCar=False
                    else:
                        followCar=True
            if event.type==pygame.QUIT:
                pygame.quit()
                running=False
                sys.exit()
        if len(cars)==0 or frames>=30*60:
            running=False
    if saveAsGo:
        NN = open('bestCar.nn', 'wb')
        NN.write(pickle.dumps(bestGenome))
        NN.close()
config=neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "NEATConfig.txt")
population = neat.Population(config)
population.add_reporter(neat.StdOutReporter(True))
stats=neat.StatisticsReporter()
population.add_reporter(stats)
winner=population.run(fitness,200)
NN=open('bestCar.nn','wb')
NN.write(pickle.dumps(winner))
NN.close()
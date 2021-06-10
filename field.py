import pygame
from vector import vector2D
import random as r
from perlin_noise import PerlinNoise

pygame.init()
key = pygame.key.get_pressed()

noise = PerlinNoise(octaves = 3, seed = 1)

fps = 40
fpsClock = pygame.time.Clock()

screen = None
scr_width = 1000
scr_height = 800
boid = []
flowfield = None
##################################################################
class Flowfield:
        def __init__(self):
                self.res = 75
                self.cols = int(scr_width / self.res) + 1
                self.rows = int(scr_height / self.res) + 1 
                self.flow = [[vector2D(0,0) for i in range(self.rows)]for j in range(self.cols)]
                self.k = 0
                self.size = 100
                
        def update(self):
                for i in range(self.cols):
                        for j in range(self.rows):
                                v = vector2D(0,0)
                                v.from_angle(self.res,noise([i/self.size,j/self.size,self.k/self.size])*360)
                                self.flow[i][j] = v
                self.k += 1      
        
                
        
        def show(self):
                for i in range(self.cols):
                        for j in range(self.rows):
                                pygame.draw.aaline(screen,(150,150,150),(i*self.res,j*self.res),(i*self.res + self.flow[i][j].x,j*self.res + self.flow[i][j].y))
                        
##################################################################
class Boid:
        def __init__(self):
                self.pos = vector2D(r.randint(0,scr_width), r.randint(0,scr_height))
                self.vel = vector2D(0,0)
                self.acc = vector2D(0,0)
                self.perc_r = 100 
                self.maxspeed = 10
                self.maxacc = 0.25
                self.angle = 0
                
        def edges(self):
                if self.pos.x >= scr_width:
                        self.pos.x = 0
                if self.pos.x < 0:
                        self.pos.x = scr_width
                if self.pos.y >= scr_height:
                        self.pos.y = 0
                if self.pos.y < 0:
                        self.pos.y = scr_height
                         
        
        def move_flow(self,stream):
                point_x = int(self.pos.x/stream.res)
                point_y = int(self.pos.y/stream.res) 
                desired = stream.flow[point_x][point_y]
                desired.set_mag(self.maxspeed)
                
                steering = vector2D(0,0)
                steering.subtract(desired,self.vel)
                steering.limit(self.maxacc)
                
                self.acc.add(steering)
                
                
        
        def update(self):
                self.vel.add(self.acc)
                self.pos.add(self.vel)

                
                self.acc.mult(0)
                
        def show(self):
                # to get circular boid use this
                #pygame.draw.circle(screen,(0,0,0),(self.pos.x,self.pos.y),5,0)
                
                # to get arrow boid use this
                w = 10
                h = 15
                body = pygame.Surface((w,h))
                body.fill((255,255,255))
                pygame.draw.polygon(body,(10,10,10),[(w/2,0),(0,h),(w/2,3/4*h),(w,h)],3)
                body2 = pygame.transform.rotate(body,self.vel.get_angle()) 
                new_rect = body2.get_rect(center = body.get_rect(center = (self.pos.x, self.pos.y)).center)
                
                screen.blit(body2, new_rect)
##################################################################
def setup():
        global screen, scr_width, scr_height
        global boid,flowfield
        screen = pygame.display.set_mode((scr_width,scr_height))
        for i in range(200):
                boid.append(Boid())
        flowfield = Flowfield()
        flowfield.update()
               
def draw():
        global boid,flowfield
        screen.fill((255,255,255))
        
        #flowfield.show()
        flowfield.update()
        for i in range(len(boid)):
                boid[i].move_flow(flowfield)
                boid[i].edges()
                boid[i].update()
                boid[i].show()
        
        
        pygame.display.flip()
###################################################################        
setup()
running = True
while running:
        # Quiting program when pygame window is closed
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                        running = False
        draw()
        pygame.display.update()
        fpsClock.tick(fps)
####################################################################

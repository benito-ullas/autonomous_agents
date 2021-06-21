import pygame
from vector import vector2D
import random as r
from perlin_noise import PerlinNoise

pygame.init()
key = pygame.key.get_pressed()

noise = PerlinNoise(octaves = 8, seed = 1)

fps = 30
fpsClock = pygame.time.Clock()

screen = None
scr_width = 800
scr_height = 600
boid = []
flowfield = None
p = None
##################################################################
class Flowfield:
        def __init__(self):
                self.res = 20
                self.cols = int(scr_width / self.res) + 1
                self.rows = int(scr_height / self.res) + 1 
                self.time_loop = 10
                self.flow = [[[vector2D(0,0)for p in range(self.time_loop)] for i in range(self.rows)]for j in range(self.cols)]
                self.k = 0
                self.size = 100
                
                
        def gen_flowfield(self):
                for i in range(self.cols):
                        for j in range(self.rows):
                                for p in range(self.time_loop):
                                        v = vector2D(0,0)
                                        v.from_angle(self.res,noise([i/self.size,j/self.size,p/self.size])*360)
                                        self.flow[i][j][p] = v
        def lookup(self,i,j,p):
                return self.flow[i][j][p]
                
        
        def show(self,p):
                for i in range(self.cols):
                        for j in range(self.rows):
                                        pygame.draw.aaline(screen,(150,150,150),(i*self.res,j*self.res),(i*self.res + self.flow[i][j][p].x,j*self.res + self.flow[i][j][p].y))
                                        
                        
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
                self.color = pygame.Color(51,51,51,0)
                self.color.hsva = (r.randint(0,125),100,100,100)
                
        def edges(self):
                if self.pos.x >= scr_width:
                        self.pos.x = 0
                if self.pos.x < 0:
                        self.pos.x = scr_width
                if self.pos.y >= scr_height:
                        self.pos.y = 0
                if self.pos.y < 0:
                        self.pos.y = scr_height
                         
        
        def move_flow(self,stream,p):
                point_x = int(self.pos.x/stream.res)
                point_y = int(self.pos.y/stream.res) 
                desired = stream.lookup(point_x,point_y,p)
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
                body = pygame.Surface((w,h), pygame.SRCALPHA)
                body.fill((0,0,0,0))
                pygame.draw.polygon(body,self.color,[(w/2,0),(0,h),(w/2,3/4*h),(w,h)],0)
                body2 = pygame.transform.rotate(body,self.vel.get_angle()) 
                new_rect = body2.get_rect(center = body.get_rect(center = (self.pos.x, self.pos.y)).center)
                
                screen.blit(body2, new_rect)
##################################################################
def setup():
        global screen, scr_width, scr_height
        global boid,flowfield, p
        screen = pygame.display.set_mode((scr_width,scr_height))
        
        for i in range(200):
                boid.append(Boid())
        flowfield = Flowfield()
        flowfield.gen_flowfield()
        p = 0
               
def draw():
        #print("draw")
        global boid,flowfield,p
        screen.fill((0,0,0))
        
        flowfield.show(p)
        
        for i in range(len(boid)):
                boid[i].move_flow(flowfield,p)
                boid[i].edges()
                boid[i].update()
                boid[i].show()
        p = p + 1
        p = p % flowfield.time_loop 
        
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

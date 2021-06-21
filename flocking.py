import pygame
from vector import vector2D
import random as r

pygame.init()
key = pygame.key.get_pressed()

fps = 80
fpsClock = pygame.time.Clock()

bgcolor = (51,51,51)
fgcolor = (255,255,255)

screen = None
scr_width = 800
scr_height = 600

boid = []
####################################################################
class Boid:
        def __init__(self):
                self.pos = vector2D(r.randint(0,scr_width),r.randint(0,scr_height))
                self.vel = vector2D(r.random()*2 -1,r.random()*2 -1)
                self.vel.set_mag(r.random()+0.5)
                self.acc = vector2D(0,0)
                self.maxacc = 0.1
                self.maxvel = 3.5
        
        def align(self,boid):
                perc_r = 50
                avg = vector2D(0,0)
                steering = vector2D(0,0)
                l = 0
                for i in boid:
                        if self.pos.dist(i.pos) <= perc_r and self != i:
                                avg.add(i.vel)
                                l += 1
                if l > 0:
                        avg.div(l)
                        avg.set_mag(self.maxvel)
                        steering.subtract(avg,self.vel)
                        steering.limit(self.maxacc)
                
                return steering          #####
                        
        def cohesion(self,boid):
                perc_r = 50
                avg = vector2D(0,0)
                steering = vector2D(0,0)
                l = 0
                for i in boid:
                        if self.pos.dist(i.pos) <= perc_r and self != i:
                                avg.add(i.pos)
                                l += 1
                if l > 0:
                        avg.div(l)
                        desired = vector2D(0,0)
                        desired.subtract(avg,self.pos)
                        desired.set_mag(self.maxvel)
                        steering.subtract(desired,self.vel)
                        steering.limit(self.maxacc)
                        
                return steering          ######
                
        def separation(self,boid):
                perc_r = 60
                diff = vector2D(0,0)
                desired = vector2D(0,0)
                steering = vector2D(0,0)
                l=0
                for i in boid:
                        if self.pos.dist(i.pos) <= perc_r and self != i:
                                diff.subtract(self.pos,i.pos)
                                diff.div(self.pos.dist(i.pos))
                                desired.add(diff)
                                l += 1
                if l>0:
                        desired.div(l)
                        desired.set_mag(self.maxvel)                
                        steering.subtract(desired,self.vel)
                        steering.limit(self.maxacc)
                                
                return steering          #######
                
        def behaviour(self,boid):
                a = vector2D(0,0)
                c = vector2D(0,0)
                s = vector2D(0,0)
                
                a = self.align(boid)
                c = self.cohesion(boid)
                s = self.separation(boid)
                
                a.mult(1.5)
                c.mult(1.2)
                s.mult(1.5)
                
                self.acc.add(a)
                self.acc.add(c)
                self.acc.add(s)
        
        def edges(self):
                if self.pos.x > scr_width:
                        self.pos.x = 0
                elif self.pos.x < 0:
                        self.pos.x = scr_width
                elif self.pos.y > scr_height:
                        self.pos.y = 0
                elif self.pos.y < 0:
                        self.pos.y = scr_height              
                        
        
        def update(self):
                self.vel.add(self.acc)
                self.vel.set_mag(self.maxvel)
                self.pos.add(self.vel)
                
                self.acc.mult(0)
                
        def show(self):
                # to get circular boid use this
                #pygame.draw.circle(screen,fgcolor,(self.pos.x,self.pos.y),5,0)
                
                # to get arrow boid use this
                w = 10
                h = 15
                body = pygame.Surface((w,h))
                body.fill(bgcolor)
                pygame.draw.polygon(body,fgcolor,[(w/2,0),(0,h),(w/2,3/4*h),(w,h)])
                body2 = pygame.transform.rotate(body,self.vel.get_angle()) 
                new_rect = body2.get_rect(center = body.get_rect(center = (self.pos.x, self.pos.y)).center)
                
                screen.blit(body2, new_rect)
                
##################################################################
def setup():
        global screen, scr_width, scr_height
        global boid
        screen = pygame.display.set_mode((scr_width,scr_height))
        for i in range(100):
                boid.append(Boid())
               
def draw():
        global boid
        screen.fill(bgcolor)
        
        
        for i in boid:
                i.behaviour(boid)
                i.edges()
                i.update()
                i.show()
        
        
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

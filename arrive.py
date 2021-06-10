import pygame
from vector import vector2D

pygame.init()
key = pygame.key.get_pressed()

fps = 60
fpsClock = pygame.time.Clock()

screen = None
scr_width = 800
scr_height = 600

boid = None
##################################################################
class Boid:
        def __init__(self):
                self.pos = vector2D(scr_width/2, scr_height/2)
                self.vel = vector2D(0,0)
                self.acc = vector2D(0,0)
                self.perc_r = 100 
                self.maxspeed = 5
                self.maxacc = 0.25
                self.angle = 0
        
        
                
        def arrive(self,target):
                desired = vector2D(0,0)
                desired.subtract(target,self.pos)
                if (desired.get_mag() > self.perc_r):
                        desired.set_mag(self.maxspeed)
                else:
                        m = desired.get_mag()/self.perc_r*self.maxspeed
                        desired.set_mag(m)
                
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
        global boid
        screen = pygame.display.set_mode((scr_width,scr_height))
        boid = Boid()
               
def draw():
        global boid
        screen.fill((255,255,255))
        
        
        boid.arrive(vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))
        boid.update()
        boid.show()
        
        
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

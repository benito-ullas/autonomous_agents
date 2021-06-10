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
        
        def seek(self,target):
                desired = vector2D(0,0)
                desired.subtract(target,self.pos)
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
                pygame.draw.circle(screen,(0,0,0),(self.pos.x,self.pos.y),5,0)
##################################################################
def setup():
        global screen, scr_width, scr_height
        global boid
        screen = pygame.display.set_mode((scr_width,scr_height))
        boid = Boid()
               
def draw():
        global boid
        screen.fill((255,255,255))
        
        boid.seek(vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))
        
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

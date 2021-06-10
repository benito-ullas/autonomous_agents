import math

class vector2D:
        def __init__(self,x,y):
                self.x = x
                self.y = y        
        
        def show_vector(self):
                return [self.x,self.y]
                
        def get_mag(self):
                mag = (self.x*self.x) + (self.y*self.y)
                return math.sqrt(mag)
                
        def get_angle(self):
                angle = math.degrees(math.atan(abs(self.y)/abs(self.x))) 
                if self.x >= 0 and self.y >=0 :
                        return 270 - angle        
                elif self.x < 0 and self.y >=0 :
                        return 90 + angle
                elif self.x >= 0 and self.y <0 :
                        return 270 + angle
                elif self.x < 0 and self.y <0 :
                        return 90 - angle
        
        def sub(self,v):
                # v should be a object of vector2D class
                self.x -= v.x
                self.y -= v.y
                
        def add(self,v):
                # v should be a object of vector2D class
                self.x += v.x
                self.y += v.y
                
        def mult(self, no):
                # no should a number
                self.x *= no
                self.y *= no
                
        def div(self, no):
                # no should be a number
                self.x /= no
                self.y /= no
                
        def set_mag(self, no):
                # no should be a number
                mag = self.get_mag()
                self.div(mag)
                self.mult(no)
                
        def subtract(self,v1,v2):
                self.x = v1.x - v2.x
                self.y = v1.y - v2.y
                
        def limit(self,no):
                mag = self.get_mag()
                if mag > no:
                        self.set_mag(no)
                        
        def from_angle(self,r,thetta):
                self.x = r * math.cos(math.radians(thetta))
                self.y = r*math.sin(math.radians(thetta))
        
        

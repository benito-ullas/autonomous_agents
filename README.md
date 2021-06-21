# AUTONOMOUS AGENTS
Series of python programs where the vehicle or boids make decision on their own and move through the screen.

Made by Benito Ullas.

Inspired from Daniel Shiffman from The Coding Train.

## Requirements
1. Python 3
2. Pygame
```pip
pip install pygame
```
3. Perlin Noise
```pip
pip install perlin-noise
```
## Different programs
1. seek.py

In this program the boid follows the mouse.

2. arrive.py

In this program the boid follows the mouse and slows down to stop on reaching the mouse.

3. field.py

In this program there is a flow field generated using perlin noise. The boids are like particle that are flowing through the flow field 

4. flocking.py

In this program the boids do flocking which is a comination of three behaviours.
Align - The boid align themselves to the average direction of their local flockmates
Cohesion - The boids moves into the average position of their local local flockmates.
Separation - To avoid over-crowding the boids separate themselves from their local flockmates. 

To get more information regarding flocking, [check this article](https://www.red3d.com/cwr/boids/)

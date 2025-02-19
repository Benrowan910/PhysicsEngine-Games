import math
import random
import pygame
from pygame.constants import *
from pygame.math import Vector2
from physics_objects import Circle, Polygon, Wall
from forces import *
import contact

pygame.init()
pygame.font.init()

# Fonts
font = pygame.font.SysFont('comicsansms', 20, False, False)
font2 = pygame.font.SysFont('comicsansms', 32, False, False)

# Colors
bonus_zone_color = (50,25,0)
Gray = (25,25,25)
# Variables
score = 0
balls_left = 3
plunger_speed = .2
plunger_acceleration = 0.1


plunger_points = [
    Vector2(0,0),
    Vector2(20,0),
    Vector2(20,500),
    Vector2(0,500)
]
plunger_points.reverse()

# Create window
width, height = 600, 800
window = pygame.display.set_mode([width, height])
center = Vector2(width/2, height/2)
diagonal = math.sqrt(width**2 + height**2)
print(window.get_height())
print(window.get_width())
# Clock object for timing
clock = pygame.time.Clock()
fps = 240
dt = 1/fps

min_plunger_height = window.get_height() - 60
max_plunger_height = window.get_height() - 500

# OBJECTS
particles = []
# pinball
pinball = Circle(pos = [window.get_width()-9, 200], radius =10, color = [255,255,0], mass = 1,static = False)
pinBall = [pinball]
# walls

top_points = [
    [-400,0],
    [400,0],
    [400,20],
    [-400,20]
]
top_points.reverse()

side_points = [
    [0,-800],
    [20,-800],
    [20,400],
    [0,400]
]
side_points.reverse()

side2_points = [
    [0,-150],
    [18,-150],
    [18,400],
    [0,400]
]
side2_points.reverse()

spinner_points = [
    [0,-50],
    [15, -50],
    [15,100],
    [0,100]
]

corner_wall_points = [
    [-70, -60],
    [-50,-60],
    [30,100],
    [10,100]
]

corner_wall_points.reverse()

corner_wall = Polygon(
    local_points = corner_wall_points,
    pos = (window.get_width()-10, 40),
    color = (155,75,155), mass = math.inf
)
spinner_points.reverse()
#border walls
top_wall = Polygon(
    local_points=top_points,
    pos=(400, 0),  # Position at the top of the screen
    color=(155, 75, 155), mass = math.inf
)

left_wall = Polygon(
    local_points= side_points,
    pos=(0, 400),  # Position at the left of the screen
    color=(155, 75, 155), mass = math.inf
)
right_wall = Polygon(
    local_points=side2_points,
    pos=(560, 400),  # Position at the right of the screen
    color=(155, 75, 155), mass = math.inf
)


#spinning walls
spinner = Polygon(local_points =spinner_points,pos = (window.get_width() /2, window.get_height()/2), color = (155,75,155), avel = 40, mass = math.inf)
belowSpin = Polygon(local_points = spinner_points,pos = (window.get_width()/2, window.get_height() - 200), color = (155,75,155), mass = math.inf)

walls= [top_wall, left_wall, right_wall, spinner, corner_wall, belowSpin]
# bumpers
polyBump = [
    [75,150],
    [125,150],
    [200,200],
    [0,200]
]


polyBump.reverse()

polyBumpRight = [
    [25,75],
    [75,75],
    [100,100],
    [0,100]
]
polyBumpRight.reverse()
trapBump1 = Polygon(local_points = polyBump, pos = (200,155), color = (255,100,100), mass = math.inf, angle = 90, bumper = True)
trapBump2 = Polygon(local_points = polyBump, pos = (200,455), color = (255,100,100), mass = math.inf, angle = 90, bumper = True)
trapBump3 = Polygon(local_points = polyBumpRight, pos = (window.get_width()-140,355), color = (255,100,100), mass = math.inf, angle = -90, bumper = True)
trapBump4 = Polygon(local_points = polyBumpRight, pos = (window.get_width()-140,655), color = (255,100,100), mass = math.inf, angle = -90, bumper = True)
topBump = Polygon(local_points = polyBump, pos = (window.get_width()/2, 200), color = (255,100,100), mass = math.inf, angle = 180, bumper = True)
trapBump5 = Polygon(local_points = polyBumpRight, pos = (window.get_width()-185,575), color = (255,100,100), mass = math.inf, angle = 90, bumper = True)
trapBump6 = Polygon(local_points = polyBumpRight, pos = (window.get_width()-400,675), color = (255,100,100), mass = math.inf, angle = -90, bumper = True)

bumper1 = Circle(pos = [window.get_width()-120, 400], radius =50, color = [0,255,0], mass = math.inf,static = True)
bumper2 = Circle(pos = [120, 400], radius =50, color = [0,255,0], mass = math.inf,static = True)
bumper3 = Circle(pos = [180, 600], radius =20, color = [0,255,0], mass = math.inf,static = True)
bumper4 = Circle(pos = [420, 600], radius =20, color = [0,255,0], mass = math.inf,static = True)
bumper5 = Circle(pos = [180, 200], radius =20, color = [0,255,0], mass = math.inf,static = True)
bumper6 = Circle(pos = [420, 200], radius =20, color = [0,255,0], mass = math.inf,static = True)

bumpers = [bumper1, bumper2, trapBump1,trapBump2,trapBump3,trapBump4, topBump, bumper3, bumper4, bumper5, bumper6, trapBump5, trapBump6]
# bonus zones
pentagonal_points = [
    [0,-50],
    [-47,-15],
    [-29,40],
    [29,40],
    [47,-15]
]

bonus_zone1 = Polygon(local_points = pentagonal_points, pos = (window.get_width() - 290, 200), color = bonus_zone_color, mass = math.inf)
bonus_zone2 = Polygon(local_points = pentagonal_points, pos = (window.get_width() - 290, 500), color = bonus_zone_color, mass = math.inf)

bonus_areas = [bonus_zone1, bonus_zone2]
# paddles
paddle_points = [
    [0,20],
    [-20,0],
    [0,-150],
    [20,0]
]
paddle_points.reverse()
left_paddle = Polygon(local_points = paddle_points, pos = (20,window.get_height()-20), color = (255,0,0), mass = math.inf)
left_paddle.angle = 90

right_paddle = Polygon(local_points = paddle_points, pos = (window.get_width()-40,window.get_height()-20), color = (255,0,0), mass = math.inf)
right_paddle.angle = -90
paddles = [left_paddle, right_paddle]
# plunger
plunger = Polygon(local_points = plunger_points, pos = (window.get_width()-20, window.get_height() -500), mass = math.inf)
plunger_velocity = 0
plunged = False

particles.append(plunger)
particles.extend(pinBall)
particles.append(top_wall)
particles.extend(walls)
particles.extend(paddles)
particles.extend(bumpers)
particles.extend(bonus_areas)

passed_bonus_zones = []

particles.extend(passed_bonus_zones)

paddleVel = 0
# Game loop
running = True
gameEnd = False
while running:
    pygame.display.update()
    clock.tick(fps)
    window.fill((0,0,0))

    # EVENTS
    while event := pygame.event.poll():
        if (event.type == QUIT
            or(event.type == KEYDOWN and event.key == K_ESCAPE)): 
            running = False
    
    # KEY STATE
    keys = pygame.key.get_pressed()
    # Plunger control
    if keys[pygame.K_DOWN]:
        plunger.pos.y += plunger_speed
        
    elif keys[pygame.K_SPACE] and plunged == False:
        plunger_velocity = 2
        plunged = True
        
    # Paddle controls
    # LEFT PADDLE
    if keys[pygame.K_LSHIFT]:
        paddleVel = -130.0

    if left_paddle.angle <= 10:
        left_paddle.angle = 10
        left_paddle.avel = 130.0
    if left_paddle.angle > 90:
        left_paddle.angle = 90
    if left_paddle.angle == 90:
        left_paddle.avel = paddleVel
    paddVel = 0

# RIGHT PADDLE
    if keys[pygame.K_RSHIFT]:
        paddleVel = 130.0

    if right_paddle.angle >= -10:
        right_paddle.angle = -10
        right_paddle.avel = -130
    if right_paddle.angle < -90:
        right_paddle.angle = -90
        right_paddle.avel = 0
    if right_paddle.angle == -90:
        right_paddle.avel = paddleVel

    paddleVel = 0
    
    if plunger.pos.y >= min_plunger_height:
        plunger.pos.y = min_plunger_height
    if plunger.pos.y <= max_plunger_height:
        plunger.pos.y = max_plunger_height
        plunged = False
        plunger_velocity = 0
        plunger.vel = Vector2(0,0)

    # PHYSICS
    # Clear force from all particles
    if gameEnd == False:
        for par in particles:
            par.clear_force()
    # Add forces
    if gameEnd == False:
        for par in particles:
            if par is pinball:
                gravity = Vector2(0,98.1)
                board_incline = math.radians(6.5)
                gravity.rotate_ip(board_incline)
                par.add_force(gravity)
            if par is plunger:
                par.vel += (Vector2(0,-plunger_velocity))
    # Update particles
    if gameEnd == False:
        for par in particles:
            par.update(dt)

    # Checking if pinball has fallen out of the game
        
    # CONTACTS
    contacts = []
    if gameEnd == False:
        for par in particles:
            if par is not pinball:
                c = contact.generate(pinball, par)
                if c.overlap > 0:
                    overlap = True
                    if par not in bonus_areas:
                        contacts.append(c)
                    elif par in bonus_areas and par not in passed_bonus_zones:
                        score += 5
                        
        for wall in  walls:
            c = contact.generate(pinball, wall, restitution = .3)
            if c.overlap > 0:
                overlap = True
                contacts.append(c)
        for pad in paddles:
            c = contact.generate(pinball, pad)
            if c.overlap > 0:
                overlap = True
                contacts.append(c)
        for bump in bonus_areas:
            c = contact.generate(pinball, bump)
            if c.overlap > 0:
                overlap = True
                passed_bonus_zones.append(bump)
                #bonus_areas.remove(bump)
        for schlump in bumpers:
            c = contact.generate(pinball,schlump, resolve = True, rebound = 100)
            if c.overlap > 0:
                overlap = True
                c.rebound = 100
        
        for c in contacts:
            c.resolve()
            print(c.contact_type)
            if c.contact_type == "CircleBumper":
                score += 1
        
    # GRAPHICS
    ## Clear window
    window.fill((0,0,0))
    ## Draw objects
    #if gameEnd == False:
    for par in particles + pinBall + bonus_areas + walls + passed_bonus_zones:
        if par in passed_bonus_zones: 
            par.color = Gray
        par.draw(window)


    ## Draw Text
    if gameEnd == False:
        text = font.render(f"Score: {score}", True,(255,0,0))
        window.blit(text, (window.get_width() /2 - 50, 30))
    else:
        text = font2.render(f"Final Score: {score}, Press Space to Exit", True, (255,255,255))
        window.blit(text, (window.get_width() /2 - 270, 330))
    
    text = font.render(f"Balls Remaining: {balls_left}", True, (255,0,0))
    window.blit(text, (window.get_width() /2 - 75, 60))
    
    if gameEnd == False:
        for bon in bonus_areas:
            if bon not in passed_bonus_zones:
                bon.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                if bon.color == (255,255,255):
                    bon.color = (0,0,0)
        

    pygame.display.flip()
    if gameEnd == False:
        for o in particles:
            if (o.pos - center).magnitude() > diagonal + pinball.radius:
            # Handle the pinball being off the screen (e.g., reset its position)
                pinball.pos = Vector2(window.get_width() - 9, 200)
                pinball.vel = Vector2(0,0)
                balls_left -=1
    if balls_left == 0 :
        gameEnd = True
    if gameEnd == True:
        if keys[pygame.K_SPACE]:
             running = False
            
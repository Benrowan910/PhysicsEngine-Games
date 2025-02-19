import pygame
from pygame.math import Vector2
from pygame.locals import *
from physics_objects import Circle, Wall, Polygon
import contact
from forces import Gravity
import itertools
import math

# initialize pygame and open window
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode(flags = FULLSCREEN)

# set timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# set objects
objects = []
lose = []

#walls
top_wall = Wall(point1= (0,0), point2 = (window.get_width(), 0), color = (255,0,255))
left_wall = Wall(point1 = (0,window.get_height()), point2 = (0, 0), color = (255,0,255))
right_wall = Wall(point1 = (window.get_width(), 0), point2 = (window.get_width(), window.get_height()), color = (255,0,255))

floor_points = [
    [0,0],
    [0,30],
    [window.get_width() - 200,30],
    [window.get_width() - 200,0]
]
short_floor_points = [
    [0,0],
    [0,30],
    [700,30],
    [700,0]
]
reduced_fric_points = [
    [0,0],
    [0,30],
    [250,30],
    [250,0]
]

trap_points = [
    [350,120],
    [200,0],
    [125,0],
    [125,120]
]

trap_points_two = [
    [450, 75],
    [175,0],
    [125,0],
    [0,75]
]

#floors
top_floor_reduced = Polygon(local_points = reduced_fric_points, color = (175, 175, 255), pos = (400,300), mass = math.inf)
top_floor_one = Polygon(local_points = floor_points, color = (255,255,255),pos = (-937,300), mass = math.inf)
top_floor_two = Polygon(local_points = short_floor_points, color = (255,255,255),pos = (651,300), mass = math.inf)
trap_one = Polygon(local_points= trap_points, color = (255,255,255), pos = (875, 200), mass = math.inf)
trap_two = Polygon(local_points= trap_points_two, color = (255,255,255), pos = (875, 545), mass = math.inf)

middle_floor = Polygon(local_points = floor_points, color = (255,255,255),pos = (200,600), mass = math.inf)

#barriers
barrier_points = [
    [0,0],
    [0,150],
    [25,150],
    [25,0]
]

barrier_points_two = [
    [0,0],
    [0,75],
    [25,75],
    [25,0]
]

death_point = [
    [0,0],
    [0,30],
    [window.get_width(), 30],
    [window.get_width(), 0]
]


barrierOne = Polygon(local_points = barrier_points, color = (255,255,255), pos = (175,150), mass = math.inf)
barrierTwo = Polygon(local_points = barrier_points, color = (255,255,255), pos = (175,-55), mass = math.inf)
barrierThree = Polygon(local_points = barrier_points_two, color = (255,255,255), pos = (325,225), mass = math.inf)
barrierFour = Polygon(local_points = barrier_points, color = (255,255,255), pos = (325,10), mass = math.inf)
death_barrier = Polygon(local_points = death_point, color = (255,0,0), pos = (0 ,window.get_height() - 30), mass = math.inf)

#floating platforms
floating_plat_points = [
    [0,0],
    [200,0],
    [200,25],
    [0,25],
]
floating_plat_points.reverse()
floating_end = [
    [0,0],
    [150,0],
    [150,25],
    [0,25]
]
floating_end.reverse()

floatingPlatOne = Polygon(local_points = floating_plat_points, color = (255,255,255), pos = (0, 900), mass = math.inf)
floatingPlatTwo = Polygon(local_points = floating_plat_points, color = (255,255,255), pos = (500, 900), mass = math.inf)
floatingPlatThree = Polygon(local_points = floating_plat_points, color = (255,255,255), pos = (1150, 120), mass = math.inf)
floatingPlatFour = Polygon(local_points = floating_end, color = (255,255,255), pos = (1190, 800), mass = math.inf)

#bouncing

bounce_points = [
    [150,25],
    [150,0],
    [0,0],
    [0,25],
]


bounce_pad_one = Polygon(local_points = bounce_points, color = (0,0,255), pos = (750, 900), mass = math.inf, static = True)
bounce_pad_two = Polygon(local_points = bounce_points, color = (0,0,255), pos = (1000, 850), mass = math.inf, static = True)

#win pad
win_point = [
    [150,500],
    [150,0],
    [0,0],
    [0,500]
]

win_pad = Polygon(local_points = win_point, color = (255,255,255), pos = (window.get_width() - 150, 750), mass = math.inf, static = True)

#spikes
spike_points = [
    [75,25],
    [38,0],
    [37,0],
    [0,25]
]

spikeOne = Polygon(local_points = spike_points, color = (255,0,0), pos = (650, 274), mass = math.inf)
spikeTwo = Polygon(local_points = spike_points, color = (255,0,0), pos = (1150, 545), mass = math.inf, angle = 16)
spikeThree = Polygon(local_points = spike_points, color = (255,0,0), pos = (750, 575), mass = math.inf)

spikeFour = Polygon(local_points = spike_points, color = (255,0,0), pos = (550, 575), mass = math.inf)
spikeFive = Polygon(local_points = spike_points, color = (255,0,0), pos = (350, 575), mass = math.inf)
spikeSix = Polygon(local_points = spike_points, color = (255,0,0), pos = (525, 357), mass = math.inf, angle = 180)
spikeSeven = Polygon(local_points = spike_points, color = (255,0,0), pos = (725, 357), mass = math.inf, angle = 180)



#bonus
bonus = Circle(pos = (1250, 90), radius = 10, color = [0,255,0], width = 0, static = True)
win_ball = Circle(pos = (window.get_width() - 50, 700), radius = 10, color = [0,255,0], width = 0, static = True)

#checkpoint
checkpoints = [
    [30,20],
    [15,0],
    [14,0],
    [0,20]
]

check1 = Polygon(local_points = checkpoints, color = (0,255,0), pos = (20,280), mass = math.inf, static = True, index = 1)
check2 = Polygon(local_points = checkpoints, color = (0,255,0), pos = (350,280), mass = math.inf, static = True, index = 2)
check3 = Polygon(local_points = checkpoints, color = (0,255,0), pos = (1000,180), mass = math.inf, static = True, index = 3)
check4 = Polygon(local_points = checkpoints, color = (0,255,0), pos = (1300,580), mass = math.inf, static = True, index = 4)
check5 = Polygon(local_points = checkpoints, color = (0,255,0), pos = (250,578), mass = math.inf, static = True, index = 5)

#initalize
checks = [check1, check2, check3, check4, check5]
die = [death_barrier, spikeOne, spikeTwo, spikeThree, spikeFour, spikeFive, spikeSix, spikeSeven]
bounce_pads = [bounce_pad_one, bounce_pad_two]
floatingPlat = [floatingPlatOne, floatingPlatTwo, floatingPlatThree, floatingPlatFour]
barriers = [barrierOne, barrierTwo, barrierThree, barrierFour]
walls = [top_wall, left_wall, right_wall, top_floor_one, top_floor_two, middle_floor, trap_one, trap_two]
reduced_floor = [top_floor_reduced]

circle = Circle(pos=(20,280), radius=17, mass=1, color=[0,0,255], width=0)
Circles = [circle]
slope_of_floor    = 0.25
coeff_of_friction = 0.3

objects.extend(Circles)
objects.append(win_pad)
objects.append(bonus)
objects.append(win_ball)
objects.extend(checks)

gravity_objects = objects.copy()

objects.extend(walls)
objects.extend(barriers)
objects.extend(floatingPlat)
objects.extend(bounce_pads)
objects.extend(die)
objects.extend(reduced_floor)

lose.extend(walls)
lose.extend(barriers)
lose.extend(floatingPlat)
lose.extend(bounce_pads)
lose.extend(die)
lose.extend(reduced_floor)
lose.append(win_pad)

# forces
gravity = Gravity(acc=[0,980], objects_list=gravity_objects)

charge_jump = False
jumping = False
jump_distance = 0
jump_velocity = 0

top = False
bottom = True

left = False
right = True

Lost = False
Win = False
game_end = False
current_checkpoint = (0,0)

chk1 = (30,20)
chk2 = (400,20)
chk3 = ()

lives = 5
bonus_reward = []
checkText = 0
# game loop
running = True
while running:
    jumping = False
    # update the display
    pygame.display.update()
    # delay for correct timing
    clock.tick(fps)
    # clear the screen
    window.fill([0,0,0])

    # EVENTS
    while event := pygame.event.poll():
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        # events for warp points
        if event.type == KEYDOWN and event.key == K_a:
            circle.avel = -420
        elif event.type == KEYUP and event.key == K_a:
            circle.avel = 0
        if event.type == KEYDOWN and event.key == K_d:
            circle.avel = 420
        elif event.type == KEYUP and event.key == K_d:
            circle.avel = 0
        if event.type == KEYDOWN and event.key == K_SPACE:
            charge_jump = True
            jumping = False
        elif event.type == KEYUP and event.key == K_SPACE:
            charge_jump = False
            jumping = True
        if event.type == KEYDOWN and event.key == K_1:
            circle.pos = check1.pos + (0,17)
            circle.vel = (0,0)
        if event.type == KEYDOWN and event.key == K_2:
            circle.pos = check2.pos + (0,17)
            circle.vel = (0,0)
        if event.type == KEYDOWN and event.key == K_3:
            circle.pos = check3.pos + (0,17)
            circle.vel = (0,0)
        if event.type == KEYDOWN and event.key == K_4:
            circle.pos = check4.pos + (0,17)
            circle.vel = (0,0)
        if event.type == KEYDOWN and event.key == K_5:
            circle.pos = check5.pos + (0,17)
            circle.vel = (0,0)
            
    

    # CONTROLS
    key = pygame.key.get_pressed()
    # movement

    
    if not key:
        circle.avel = 0
    # jumping
    print(dt)
    if charge_jump:
        jump_distance += dt
        if jump_distance >= 0.25:
            jump_distance = 0.25
    print(jump_distance)
    if jumping:
        jump_velocity = math.sqrt(jump_distance) * 1250
        jump_distance = 0

    # PHYSICS
    for o in objects:
        o.clear_force()
        
    #floating platforms
    if floatingPlatOne.pos.y >= 650 and bottom:
        floatingPlatOne.vel = (0,-60)
        if floatingPlatOne.pos.y <= 650:
            top = True            
            bottom = False
    if floatingPlatOne.pos.y <= 900 and top:
        floatingPlatOne.vel = (0,60)
        if floatingPlatOne.pos.y >= 900:
            top = False
            bottom = True
            
    if floatingPlatTwo.pos.x >= 200 and right:
        floatingPlatTwo.vel = (-90,0)
        if floatingPlatTwo.pos.x <= 200:
            left = True            
            right = False
    if floatingPlatTwo.pos.x <= 500 and left:
        floatingPlatTwo.vel = (+90,0)
        if floatingPlatTwo.pos.x >= 500:
            left = False
            right = True


    # forces
    gravity.apply()
    
    # update objects
    for o in objects:
        o.update(dt)

    # COLLISIONS
    
    for a, b in itertools.combinations(objects, 2):
        if jumping:
            c = contact.generate(a, b, resolve=True, restitution=0.2, friction=coeff_of_friction, rebound_speed = jump_velocity)
        elif not jumping and b in bounce_pads:
            c = contact.generate(a, b, resolve=True, restitution=0.2, friction=coeff_of_friction, rebound_speed = 500)
        elif not jumping and b in reduced_floor:
            c = contact.generate(a,b, resolve =True, restitution =.2, friction = 0.04)
        elif not jumping and b is win_ball:
            c = contact.generate(a,b, resolve = True, resitution = .2)
            if c.overlap >=0 :
                Win = True
                b.pos = (-100,-100)
        elif not jumping and b is bonus:
            c = contact.generate(a,b)
            if c.overlap >=0 :
                b.pos = (-100,-100)
                die.remove(spikeThree)
                objects.remove(spikeFour)
        elif not jumping and b in checks:
            c = contact.generate(a,b, resolve = False)

        else:
            c = contact.generate(a, b, resolve=True, restitution=0.2, friction=coeff_of_friction)
    for dead in die:
        c = contact.generate(circle, dead)
        if c.overlap >= 0:
            lives -=1
            circle.pos = (-100, -100)
            Lost = True
    for check in checks:
        c = contact.generate(circle,check)
        if c.overlap >= 0:
            current_checkpoint = check.pos + (0,17)
    
    for dead in die:
        if dead in bonus_reward:
            die.remove(dead)
    # GRAPHICS
    # draw objects
    if not Lost:
        for o in objects + Circles:
            o.draw(window)
    if Lost:
        for o in lose:
            o.draw(window)
            
    font = pygame.font.SysFont('comicsansms', 36, False, False)
    scoreboard = font.render(f"Lives:{lives}", True, (0,255,0))
    window.blit(scoreboard, (window.get_width() - 200, 20))
    
    if current_checkpoint+ (0,-17) == (20,280):
        checkText = 1
    if current_checkpoint+ (0,-17) == (350,280):
        checkText = 2
    if current_checkpoint+ (0,-17) == (1000,180):
        checkText = 3
    if current_checkpoint + (0,-17)== (1300,580):
        checkText = 4
    if current_checkpoint+ (0,-17) == (250,578):
        checkText = 5
    
    checkpointTell = font.render(f"Current Checkpoint{checkText}", True, (0,255,0))
    window.blit(checkpointTell, (window.get_width()/2, 20))
    if Lost:
        if lives >0:
            text = font.render("You died bruh", True,(255,0,0))
            text2 = font.render("Press L to Respawn", True,(255,0,0))

            window.blit(text, (window.get_width() /2 - 150, window.get_height()/2 - 30))
            window.blit(text2, (window.get_width() /2 - 250, window.get_height()/2 + 34))
            if key[K_l]:
                circle.pos = current_checkpoint
                circle.vel = (0,0)
                jump_velocity = 0
                Lost = False
        elif lives == 0:
            game_end = True
            lives = 0
    if Win:
        text = font.render("You did it!", True, (255,0,255))
        window.blit(text, (window.get_width() / 2 - 150, window.get_height()/2 - 30))
    if game_end == True:
        text = font.render("You have lost the game.", True, (255,0,0))
        window.blit(text,(window.get_width()/2 - 150,window.get_height()/2-30))

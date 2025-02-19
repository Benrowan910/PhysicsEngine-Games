import random
import pygame
from pygame.constants import *
from pygame.math import Vector2, Vector3
import math
from physics_objects import Circle  # copy in physics_objects.py from your previous project
from forces import *

# INITIALIZE PYGAME AND OPEN WINDOW
pygame.init()
window = pygame.display.set_mode(flags=FULLSCREEN)

# SETUP TIMING
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# SETUP OBJECTS
objects = [] 
gravity = []
pairList = []
num_objects = 15
vertical_placement = 50
GRAY = (70,70,70)
WHITE = (255,255,255)
current_color = GRAY

grabbed_circle = None

prev_mouse_pos = Vector2(0,0)

wind_velocity = Vector2(0, 0)

wind_speed_scale = 10.0

paused = False

for i in range(num_objects):
    circle = Circle(mass=1, pos=(window.get_width()/2, vertical_placement), radius=20, color = current_color)  
    vertical_placement += 50
    current_color = (random.randint(0,255),random.randint(0,255), random.randint(0,255) )
    objects.append(circle)
    
pairList = itertools.pairwise(objects)
# SETUP FORCES
for i in range(num_objects):
    gravity.append(Gravity(objects_list=[objects[i]], acc=(0,100)))
    #drag = Drag(objects_list =[objects[i]], drag_coefficient = .01, cross_sectional_area = .01, air_density = 1.225)
    
drag = Drag(objects_list= objects, wind_velocity=wind_velocity, drag_coefficient = .01, cross_sectional_area = .01, air_density = .001)

bonds = SpringForce(stiffness = 25, damping =5, natural_length = 10, pairs_list = list(itertools.pairwise(objects)))
repulsion = SpringRepulsion()


# game loop
running = True
clock.tick()
while running:
    # DISPLAY
    pygame.display.update()
    # TIMING
    clock.tick(fps)
    # BACKGROUND GRAPHICS
    window.fill([75,75,150])
 
    objects[0].vel = Vector2(0,0)
    objects[0].pos = (window.get_width()/2, 50)
 
    # EVENTS
    #prev_mouse_pos = Vector2(pygame.mouse.get_pos())

    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button ==1:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_LCTRL]:
                print ("yoink")
                for circle in objects:
                    if circle.contains_point(mouse_pos):
                        objects.remove(circle)
                        bonds.remove_bonds(circle)
                        break
            else:
                for circle in objects:
                    if circle.contains_point(mouse_pos):
                        grabbed_circle = circle
                        grabbed_circle.clear_force()
                        break
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if grabbed_circle:
                current_mouse_pos = Vector2(pygame.mouse.get_pos())
                mouse_velocity = (Vector2(current_mouse_pos - prev_mouse_pos)) /dt
                grabbed_circle.clear_force()
                grabbed_circle.vel = mouse_velocity
                grabbed_circle.update(dt)
                grabbed_circle = None
                #prev_mouse_pos = Vector2(pygame.mouse.get_pos())

        elif event.type == KEYDOWN and event.key == K_SPACE:
            if grabbed_circle:
                grabbed_circle.fixed = not grabbed_circle.fixed
                if grabbed_circle.fixed:
                    grabbed_circle.color = GRAY
                else: grabbed_circle.color = WHITE
        elif event.type == KEYDOWN and event.key == K_p:
            if paused:
                paused = False
            elif not paused:
                paused = True
    prev_mouse_pos = Vector2(pygame.mouse.get_pos())
    if pygame.mouse.get_pressed()[0] and grabbed_circle is not None:
        #current_mouse_pos = Vector2(pygame.mouse.get_pos())
        grabbed_circle.pos = Vector2(pygame.mouse.get_pos())
    # PHYSICS
    ## clear all forces from each object
    for circle in objects:
        circle.clear_force()
    ## apply all forces
    if not paused:
        for i in range(num_objects):
            if i != 0:
                gravity[i].apply()
        bonds.apply()
        drag.apply()
        repulsion.apply()
    
    ## update all objects
    for circle in objects:
        if not circle.fixed and paused == False:
            circle.update(dt)

    # STATE CHECKS
    ## Mouse state check for grabbing objects
    ## Key state check for changing wind velocity
    keys = pygame.key.get_pressed()
    
    # Adjust wind velocity using left and right arrow keys
    if keys[K_LEFT]:
        wind_velocity.x -= 1.0  # Adjust the wind speed increment as needed
    elif keys[K_RIGHT]:
        wind_velocity.x += 1.0  # Adjust the wind speed increment as needed

    # GRAPHICS
    ## draw all objects
    bonds.draw(window)
    for circle in objects:
        circle.draw(window)

    wind_speed_bar_length = abs(wind_velocity.x) * wind_speed_scale
    print(wind_speed_bar_length)
    wind_bar_start_x = window.get_width() //2
    if wind_velocity.x < 0:
        wind_bar_start_x -= wind_speed_bar_length
    
    pygame.draw.rect(window, (255, 0, 0), (wind_bar_start_x, 10, wind_speed_bar_length, 10))
    
    # Display the wind speed as text
    wind_speed_text = f"Wind Speed: {wind_velocity.x:.2f} m/s"  # Adjust units as needed
    font = pygame.font.Font(None, 36)
    text = font.render(wind_speed_text, True, (255, 255, 255))
    window.blit(text, (10, 10))

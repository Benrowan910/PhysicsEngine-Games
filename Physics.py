import pygame
from pygame.constants import *
from pygame.math import Vector2
import math
from physics_objects import *
from forces import *
import contact
from collections import defaultdict
from draw_objects import *

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
fps = 120
dt = 1/fps
font = pygame.font.SysFont(None, 24)
CELL_SIZE = 20
LocalRadius = 30
slider_width = 300
slider_height = 10
slider_x = 50
slider_y = 50
slider_min_value = 10
slider_max_value = LocalRadius

slider = Slider(slider_x, slider_y, slider_width, slider_height, slider_min_value, slider_max_value)


particleAmount = 50
particles = []

top_wall = Wall(point1= (0,0), point2 = (screen.get_width(), 0), color = (255,255,255))
bottom_wall = Wall(point1 = (screen.get_width(),screen.get_height()), point2 = (0, screen.get_height()), color = (255,255,255))
left_wall = Wall(point1 = (-10,screen.get_height()), point2 = (0, 0), color = (255,255,255))
right_wall = Wall(point1 = (screen.get_width(), 0), point2 = (screen.get_width(), screen.get_height()), color = (255,255,255))

walls = [top_wall, bottom_wall, left_wall, right_wall]

#function to initiate a cell index based on position
def get_cell_index(pos):
    """Convert a position into a grid cell index"""
    if math.isnan(pos.x) or math.isnan(pos.y):
        print(f"Warning: Invalid position detected: ({pos.x}, {pos.y})")
        return (0, 0)
    return (int(pos.x // CELL_SIZE), int(pos.y // CELL_SIZE))

#grid instantiation and updating the grid position based on particle position
grid = defaultdict(list)
def update_grid(particles):
    grid.clear()
    for particle in particles:
        cell = get_cell_index(particle.pos)
        grid[cell].append(particle)
        
NEIGHBOR_OFFSETS = [
    (0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (-1, -1), (1, -1), (-1, 1)
]

def check_collisions():
    for cell, cell_particles in grid.items():
        # Check with particles in the same cell and neighboring cells
        for dx, dy in NEIGHBOR_OFFSETS:
            neighbor_cell = (cell[0] + dx, cell[1] + dy)
            if neighbor_cell in grid:
                for i, p1 in enumerate(cell_particles):
                    for p2 in grid[neighbor_cell]:
                        if p1 == p2:
                            continue
                        ct = contact.generate(p1, p2, restitution=0.5, FrictionForce= 9.5)
                        if ct.overlap > 0:
                            ct.resolve()

def createParticles():
    """Function to create the particles that the program is going to be using"""
    spacing = LocalRadius * 2
    width = screen.get_width()
    height = screen.get_height()
    
    x = LocalRadius
    y = LocalRadius
    
    for i in range(particleAmount):
        particles.append(Circle(
            radius = LocalRadius,
            color = (0, 0, 255), 
            pos = Vector2(x, y),
            mass = 100
        ))
        
        x += spacing
        
        if x + LocalRadius > width:
            x = LocalRadius
            y += spacing
    
    #Instantiate the particles in the particle array
createParticles()

while running:
    #poll for any events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    slider.update(mouse_pos, mouse_pressed)
    
    for particle in particles:
        particle.radius = int(slider.value)
    
    #reset each frame with a background color
    screen.fill("purple")
    
    
    update_grid(particles)
    check_collisions()
    
    # # Cohesion force 
    # cohesion =CohesionForce(objects_list = particles, strength= 1.0, radius = 15)
    # cohesion.apply()  
     
    # # # Repulsion force to prevent particles from overlapping
    # spring_repulsion = SpringRepulsion(objects_list=particles, spring_constant=1000)
    # spring_repulsion.apply() 
    
    # viscosity = Viscosity(objects_list=particles, viscosity_coefficient = 1)
    # viscosity.apply()
    
    # pressure = PressureForce(objects_list=particles, pressure_strength = 100)
    # pressure.apply()
    
    # wall_interaction = WallInteraction(objects_list=particles, walls=walls, restitution=0.5)
    # wall_interaction.apply()

    #this is where we want to render everything else
    for particle in particles:
        
        gravity = Gravity (acc = (0, 2), objects_list = [particle])
        gravity.apply()
        

        particle.update(dt)
    
    #create gravity force

    for wall in walls:       
        for particle in particles:
            ct = contact.generate(particle, wall, restitution = .1, rebound_speed = 500)
            if ct.overlap > 0:
                ct.resolve()
                
    for wall in walls:
        wall.draw(screen)
        wall.update(dt)  
        
    for particle in particles:
        particle.draw(screen)
        
    slider.draw(screen)
    
        # Show the current particle size
    size_text = font.render(f"Particle Size: {int(slider.value)}", True, (255, 255, 255))
    screen.blit(size_text, (slider_x, slider_y + slider_height + 20))
        
        
    FPS_COUNTER = int(clock.get_fps())
    FPS_TEXT = font.render(f"FPS:{FPS_COUNTER}", True, (255,255,255))
    screen.blit(FPS_TEXT, (10,10))
    #flip the screen to display the work
    pygame.display.flip()
    
    #caps the frames to 60
    clock.tick(fps)
    
#quits the game as soon as the while loop is done.
pygame.quit()
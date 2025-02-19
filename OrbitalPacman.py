import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import random
import math
from physics_objects import Circle

#INITIALIZE PYGAME
pygame.init()
pygame.font.init()

#CREATE WINDOW
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
SIZE = 0.4*min(screen_height, screen_width)
window = pygame.display.set_mode([2*SIZE+1, 2*SIZE+1])

#TIMING
clock = pygame.time.Clock()
FPS = 60
clock.tick()
#ship initialization
ship = Circle(radius = SIZE/30, color= (100, 127, 255), pos = (SIZE/2, SIZE/2), vel= (0,0))

ship_mass = 1

#sun initialization
sun = Circle(radius = SIZE/10, color= (255,255,0), pos = (window.get_width()/2, window.get_height()/2), vel = (0,0))

#win/lose conditions
win = False
lose = False
ship_gone = False

#timer variables
start_time = pygame.time.get_ticks()
timer_font = pygame.font.SysFont('comicsansms', 36, False, False)

pause_start_time = 0
elapsed_time_ms = 0
has_paused = False

minutes = 0
seconds = 0

pause = False

M_sun = 1

G = (SIZE**3)/15

class Dot(Circle):
    def __init__(self, radius, color, sun_pos, orbit_radius):
        super().__init__(radius=radius, color=color)
        self.sun_pos = sun_pos
        self.orbit_radius = orbit_radius
        self.angle = random.uniform(0, 2 * math.pi)  # Random initial angle
        self.calculate_position()

    def calculate_position(self):
        x = self.sun_pos.x + self.orbit_radius * math.cos(self.angle)
        y = self.sun_pos.y + self.orbit_radius * math.sin(self.angle)
        self.pos = Vector2(x, y)

    def update(self, dt):
        # Update the angle based on orbital velocity
        orbital_speed = math.sqrt(G * M_sun *.01 / self.orbit_radius**2)
        self.angle += orbital_speed * dt
        self.calculate_position()

class Obstacle(Circle):
    def __init__(self, radius, color, position, velocity):
        super().__init__(radius = radius , color = color)
        self.position = position
        self.velocity = velocity
        self.angle = random.uniform(0, 2 * math.pi)
        self.calculate_position()
        
    def calculate_position(self):
        x = self.position.x + self.velocity * math.cos(self.angle)
        y = self.position.y + self.velocity * math.sin(self.angle)
        self.pos = Vector2(x, y)

    def update(self, dt):
        # Update the angle based on orbital velocity
        obstacle_speed = math.sqrt(G * M_sun *.001 / self.velocity**2)
        self.angle += obstacle_speed * dt
        self.calculate_position()
#function to reset the game
def reset_game():
    global ship, win, lose, ship_gone, G
    # Reset game states
    win = False
    lose = False
    ship_gone = False

    G = SIZE**3/15
    # Reinitialize ship
    ship = Circle(radius = SIZE/30, color= (100, 127, 255), pos = (SIZE/2, SIZE/2), vel= (0,0))
    # Reinitialize dots
    dots.clear()
    for i in range(number_of_dots):
        dot_radius = SIZE / 60
        dot_color = (255, 255, 255)
        min_orbit_radius = sun.radius * 2  # Adjust as needed
        max_orbit_radius = SIZE - dot_radius * 2  # Adjust as needed
        orbit_radius = random.uniform(min_orbit_radius, max_orbit_radius)
        dot = Dot(radius=dot_radius, color=dot_color, sun_pos=sun.pos, orbit_radius=orbit_radius)
        dots.append(dot)
    #Reinitialize obstacles
    obstacles.clear()
    for obstacle in range(num_obstacles):
        obstacle_radius = SIZE/40
        obstacle_color = (255,0,0)
        min_orbit_radius = sun.radius * 2
        max_orbit_radius = SIZE - dot_radius * 2
        obstacle_radius_max = random.uniform(min_orbit_radius, max_orbit_radius)
        obstacle = Obstacle(radius=obstacle_radius, color=obstacle_color, position= sun.pos, velocity=obstacle_radius_max)
        obstacles.append(obstacle)
        
#initialization of dots
dots = []
number_of_dots = 6
for i in range(number_of_dots):
    dot_radius = ship.radius / 2
    dot_color = (255,255,255)
    min_orbit_radius = sun.radius * 2
    max_orbit_radius = SIZE - dot_radius * 2
    orbit_radius = random.uniform(min_orbit_radius, max_orbit_radius)
    dot = Dot(radius = dot_radius, color = dot_color, sun_pos= sun.pos, orbit_radius= orbit_radius)
    dots.append(dot)
    
#initialization of obstacles
obstacles = []
num_obstacles = 3
for obstacle in range(num_obstacles):
    obstacle_radius = SIZE/40
    obstacle_color = (255,0,0)
    min_orbit_radius = sun.radius * 2
    max_orbit_radius = SIZE - dot_radius * 2
    obstacle_radius_max = random.uniform(min_orbit_radius, max_orbit_radius)
    obstacle = Obstacle(radius=obstacle_radius, color=obstacle_color, position= sun.pos, velocity=obstacle_radius_max)
    obstacles.append(obstacle)
#ship.mass = 900
#GAME LOOP
running = True
while running:
    keys = pygame.key.get_pressed()
        # EVENTS
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_p and not pause:  # Toggle pause state
                pause = True
                has_paused = True

            elif event.key == K_p and pause:  # Resume game
                pause = False
    # DISPLAY AND TIMING            
    pygame.display.update()
    dt = clock.tick(FPS) / 1000
    
    #Check to see if the game is paused           
    if not pause:  
        
        #gravity calculations for the ship
        if ship_gone == False:
            distance_to_sun = sun.pos - ship.pos
            r_hat = distance_to_sun.normalize()
            F_grav = ((G * M_sun * 7) / abs(distance_to_sun.length_squared())) * r_hat
            
            v_ship = math.sqrt(G * M_sun * ship.mass/ distance_to_sun.length())

            initial_velocity_direction = distance_to_sun.rotate(90).normalize()

            ship.vel = v_ship * initial_velocity_direction

        #settings the timer variables
        elapsed_time_ms += 15
        
        elapsed_seconds = elapsed_time_ms // 1000
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        timer_surface = timer_font.render(timer_text, True, (255,255,255))
        timer_rect = timer_surface.get_rect(topleft = (10,10))

        pause_notif = timer_font.render("Press P To Pause", True, (255,255,255))
        pause_rect = pause_notif.get_rect(topright = (window.get_width()-10, 10))
        
    #BACKGROUND GRAPHICS
        window.fill((0,0,0))
        
        # PHYSICS
        ## Clear force from all particles
        if ship_gone == False:
            ship.clear_force()
            for dot in dots:
                dot.clear_force()
            for obstacle in obstacles:
                obstacle.clear_force()
        
    #Add forces
    #Gravitational force
        if ship_gone == False:
            ship.add_force((F_grav))
            
        for dot in dots: 
            distance_to_sun_dot = sun.pos - dot.pos
            r_hat_dot = distance_to_sun_dot.normalize()
            F_grav_dot = ((G * M_sun * .1) / distance_to_sun_dot.length_squared()) * r_hat_dot
            dot.add_force(F_grav_dot)
            
        ### Thrust force
        if ship_gone == False:
            key = pygame.key.get_pressed()
            direction = Vector2(0,0)
            if key[K_UP]:
                direction += Vector2(0,-1)
                ship.add_force((0, -SIZE*12/3))
                print("up")
            if key[K_DOWN]:
                direction += Vector2(0,1)
                ship.add_force((0, SIZE*12/3))
                print("down")
            if key[K_LEFT]:
                direction += Vector2(-1, 0)
                ship.add_force((-SIZE*12/3,0))
                print("left")
            if key[K_RIGHT]:
                direction += Vector2(1,0)
                ship.add_force((SIZE*12/3,0))
                print("right")
            if direction != Vector2(0,0):
                direction.normalize()
            else:
                thrust_vector = Vector2(0,0)
                
            triangle_length = 20  # Adjust the size as needed
            triangle_tip = ship.pos + -direction * triangle_length
            triangle_base1 = ship.pos + -direction.rotate(90) * (triangle_length / 2)
            triangle_base2 = ship.pos + -direction.rotate(-90) * (triangle_length / 2)
    
            # Define the triangle points as a list of tuples
            triangle_points = [triangle_tip, triangle_base1, triangle_base2]
    
            # Draw the triangle on the screen
            pygame.draw.polygon(window, (255, 0, 0), triangle_points)

    #Update particles
        if ship_gone == False:
            ship.update(dt)
        for dot in dots:
            dot.update(dt)
        for obstacle in obstacles:
            obstacle.update(dt)
        
    #line calculations
        r = distance_to_sun.length()
        theta = math.atan2(distance_to_sun.y,distance_to_sun.x)
        
    #check to see if hit SUn and Obstacle
        if ship_gone == False:
            if ship.pos.distance_to(sun.pos) < ship.radius + sun.radius:
                lose = True
            for obstacle in obstacles:
                if ship.pos.distance_to(obstacle.pos) < ship.radius + obstacle.radius:
                    lose = True
                    obstacles.remove(obstacle)
            
    #GAME ELEMENTS
    #Dot collection
        for dot in dots:
            if ship_gone == False:
                if ship.pos.distance_to(dot.pos) < ship.radius + dot.radius:
                    G+=10
                    dots.remove(dot)
        if len(dots) == 0:
            win = True
    #Winning
        if win: 
            font = pygame.font.SysFont('comicsansms', 36, False, False)
            text = font.render("You won! Press SpaceBar To Restart", True, (255, 255, 255))
            text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 1.25))
            window.blit(text, text_rect)
            elapsed_time_ms = 0
    #Losing    
        if lose:
            # Display "You lost!" at the center of the screen
            font = pygame.font.SysFont('comicsansms', 36, False, False)
            text = font.render("You lost! Press SpaceBar To Restart", True, (255, 255, 255))
            text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 1.25))
            window.blit(text, text_rect)
            ship = None
            ship_gone = True
            elapsed_time_ms=0
    #Reset Game
        if win or lose:
            if keys[K_SPACE]:
                reset_game()
    #GRAPHICS
        window.blit(timer_surface,timer_rect)
        window.blit(pause_notif, pause_rect)
        sun.draw(window)
        if ship_gone == False:
            ship.draw(window)
        for dot in dots:
            dot.draw(window)
        for obstacle in obstacles:
            obstacle.draw(window)
        if ship_gone == False:
            if (
            ship.pos.x < 0 or ship.pos.x > window.get_width() or
            ship.pos.y < 0 or ship.pos.y > window.get_height()
            ):
                angle_off = math.asin(ship.radius/r)
            
                point1_angle = theta-angle_off
                point2_angle = theta+angle_off
            
                point1_x = sun.pos.x - r * math.cos(point1_angle)
                point1_y = sun.pos.y - r * math.sin(point1_angle)

                point2_x = sun.pos.x - r * math.cos(point2_angle)
                point2_y = sun.pos.y - r * math.sin(point2_angle)

                # Draw the lines on the screen
                pygame.draw.line(window, (255, 255, 255), sun.pos, (point1_x, point1_y), 2)
                pygame.draw.line(window, (255, 255, 255), sun.pos, (point2_x, point2_y), 2)
    else:
        font = pygame.font.SysFont('comicsansms', 36, False, False)
        text = font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 1.50))
        window.blit(text, text_rect)
        pause_start_time = elapsed_time_ms
        
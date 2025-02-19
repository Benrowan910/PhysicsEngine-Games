import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import random
import math

from physics_objects import Circle, Wall, Polygon, UniformPolygon, UniformCircle
import itertools
import contact

# initialize pygame and open window
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode([width, height])

# set timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()
spawn_timer = 0
spawn_interval = 2

# Objects
objects = []
bombs = []
# Walls for ground and invisible boundaries: left, right, and top
ground = Wall(point1=[0,height], point2=[width,height], color=(0,190,0), width = 100)
ground.normal = -ground.normal
# shooter
shooter_points = [
    [0,-90],
    [50,-25],
    [-50,-25]
]
shooter_points.reverse()
shooter = Polygon(mass = 1, local_points = shooter_points, color = (150,0,175), pos = (width/2, height - 25))
# bullets
bullet_size = 5
bullet_speed = 200
shot_rate = 10
shot_timer = 0
bullets = []
# shapes
local_shmuck = [
    [-15,-15],
    [15,-15],
    [15,15],
    [-15,15]
]

local_triangle = [
    [-15,-15],
    [15,-15],
    [0,15]
]
local_rhombus = [
    [0, -15],
    [15, 0],
    [0, 15],
    [-15, 0]
]
local_rectangle = [
    [-10, -15],
    [10, -15],
    [10, 15],
    [-10, 15]
]
local_pentagon = [
    [0, -15],
    [13.76, -5],
    [8.66, 11.18],
    [-8.66, 11.18],
    [-13.76, -5]
]

local_triangle.reverse()
local_rectangle.reverse()
local_pentagon.reverse()
local_rhombus.reverse()
local_shmuck.reverse()
shapes_library = [
    local_triangle, local_shmuck, local_rectangle, local_rhombus, local_pentagon
]
# bombs

# Functions
stage = 1
stage_chose = 1
indScore = 0

def spawn(): # spawns a new shape
    i = random.randint(0, stage_chose- 1)
    current_points = shapes_library[i]
    
    global indScore
    indScore = i + 1
    
    return UniformPolygon(density = 1, local_points = current_points, color =( 255,255,255),pos = Vector2(random.uniform(50, width-50), 10), vel = Vector2(random.uniform(-10,10), random.uniform(50,100)),
                          avel = random.uniform(-10,10))

def spawn_bomb(): # spawns a bomb
    return Circle(mass = 10000, color = (255,0,0), radius = 20, pos = Vector2(random.uniform(50,width-50), 10), vel = (0,100))
# Set up lives and score
lives = 3
life_lost = False
lives_out = False
life_timer = 0
life_shoot_point =[
    [0,-40],
    [20,-10],
    [-20,-10]
]
life_shoot = Polygon(mass = 1, local_points = life_shoot_point, color = (255,255,255), pos = (width-30, height))
score = 0
max_score = 0
font = pygame.font.SysFont('comicsansms', 18, False, False)
overFont = pygame.font.SysFont('comicsansms',48, False, False)

game_over = False
running = True
dead = False
paused = False
bomb_count = 0
bomb_timer = 0
bomb_yes = False

explode = False
explosion_blast = None
explosion_timer = 0
SHOOTER_RESPAWN_EVENT = pygame.USEREVENT+1

while running:
    # game loop
    red_value = 20*stage
    spawn_interval = 4 / 1- (stage_chose ** .303)
    # EVENT loop
    for event in pygame.event.get():
        # Quitting game
        if (event.type == pygame.QUIT 
            or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE)):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            shooter.vel.x = -200
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            shooter.vel.x = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            shooter.vel.x = 200
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            shooter.vel.x = 0
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     if shot_timer <=0:
        #         bullet = UniformCircle(density = 1, radius = bullet_size, pos = shooter.pos + (0,-100), vel = (0,-bullet_speed))
        #         bullets.append(bullet)
        #         shot_timer = shot_rate
        # Use USEREVENT to start a new shooter after a delay of 2 seconds 
        if event.type == SHOOTER_RESPAWN_EVENT:
            pygame.time.set_timer(SHOOTER_RESPAWN_EVENT,0)
            objects.clear()
            bullets.clear()
            bombs.clear()
            if not lives_out:
                lives -=1
            life_lost = False
            shooter.pos = [width/2, height-25]
            if paused:
                shooter.pos = [-500,-500]
            shooter.vel = Vector2(0,0)
            shooter.avel = 0
            
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            if shot_timer <=0:
                bullet = UniformCircle(density = 2, radius = bullet_size, pos = Vector2(shooter.pos + (0,-100)), vel = (0,-bullet_speed))
                bullets.append(bullet)
                shot_timer = shot_rate

    if not paused:
        if score > max_score:
            max_score = score
        # PHYSICS
        for obj in objects:
            obj.clear_force()
        spawn_timer += dt
        
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            objects.append(spawn())
            bomb_count +=1
        
        if shot_timer >0:
            shot_timer -=1
        
        if bomb_count == 10:
            bombs.append(spawn_bomb())
            bomb_count = 0
        # update all objects
        shooter.update(dt)
        for obj in objects:
            obj.update(dt)
        for bullet in bullets:
            bullet.update(dt)
        for bomb in bombs:
            bomb.update(dt)
        ground.update(dt)
        # keep shooter on screen
        shooter.pos.x = max(shooter.pos.x,0)
        shooter.pos.x = min(shooter.pos.x,width)
        # collisions between bullets and polygons and polygons with each other
        for obj in objects:
            for bullet in bullets:
                c = contact.generate(bullet,obj,resolve = True, restitution = 1)
                if c.overlap >= 0:
                    bullets.remove(bullet)
                    
        for a,b in itertools.combinations(objects,2):
            c = contact.generate(a,b, resolve = True, restitution = 1)
        # check bullets hitting ground or going off screen
        for bullet in bullets:
            if bullet.pos.y < 0 or bullet.pos.y > height or bullet.pos.x < 0 or bullet.pos.x > width:
                bullets.remove(bullet)
        # check polygons hitting ground or going off screen or hitting shooter
        for obj in objects:
            if obj.pos.y < 0 or obj.pos.y > height or obj.pos.x < 0 or obj.pos.x > width:
                objects.remove(obj)
                if not lives_out or not life_lost:
                    score += indScore
        for obj in objects:
            c = contact.generate(obj, ground)
            if c.overlap > 0:
                objects.remove(obj)
                if lives_out == False or life_lost== False:
                    print("YORKKKK")
                    score -= indScore
        
        for obj in objects:
            c = contact.generate(obj, shooter, resolve = True)
            if c.overlap > 0:
                objects.remove(obj)
                life_lost = True
                shooter.pos = [-150,-150]
                shooter.vel = Vector2(0,0)
                pygame.time.set_timer(SHOOTER_RESPAWN_EVENT,2000)

        # check bombs hitting ground or going off screen or hitting shooter
        for bomb in bombs:
            c = contact.generate(bomb, ground, resolve = True)
            if c.overlap > 0:
                pygame.time.set_timer(SHOOTER_RESPAWN_EVENT,2000)
                bombs.clear()
                shooter.pos = [-150,-150]
                shooter.vel = Vector2(0,0)

                bomb_yes = True
            for bullet in bullets:
                c = contact.generate(bomb, bullet, resolve = True)
                if c.overlap > 0:
                    exp_pos = bomb.pos
                    bullets.remove(bullet)
                    bombs.remove(bomb)
                    explode = True
            if bomb.pos.y < 0 or bomb.pos.y > height or bomb.pos.x < 0 or bomb.pos.x > width:
                bombs.remove(bomb)
            for object in objects:
                c = contact.generate(bomb, object, resolve = True, restitution = 1)
            
            c = contact.generate(bomb, shooter)
            if c.overlap > 0:
                pygame.time.set_timer(SHOOTER_RESPAWN_EVENT,2000)
                bombs.clear()
                shooter.pos = [-150,-150]
                shooter.vel = Vector2(0,0)
        
        #bomb hitting ground or player
        if bomb_yes == True:
            if bomb_timer <=.1:
                bomb_timer += dt
                screen.fill((255,0,0))
            elif bomb_timer >.1:
                screen.fill((0,0,0))
                bomb_timer = 0
                bomb_yes = False
                
        #explosion event upon bomb shoot
        if explode == True:
            explosion_blast = Circle(color = (175,175,10), pos = exp_pos, radius = 30)
            explosion_blast.draw(screen)
            
            explosion_timer += dt
            if explosion_timer >= .25:
                explosion_blast.radius = 50
            if explosion_timer >= .4:
                explosion_blast.radius = 65
            if explosion_timer >= .55:
                explosion_blast.radius = 80
            if explosion_timer >.65:
                explosion_blast.pos = Vector2(-300,-500)
                explosion_blast = None
                explosion_timer = 0
                explode = False  
                
            for obj in objects:
                if explosion_blast is not None:
                    c = contact.generate(explosion_blast, obj, resolve = True)
                    if c.overlap > 0:
                        objects.remove(obj)
                        score += stage + indScore
                    

        # Stages and scoring
        if max_score >= 10:
            stage = 2
            stage_chose = 2
        if max_score >= 20:
            stage = 3
            stage_chose = 3
        if max_score >= 30:
            stage = 4
            stage_chose = 4
        if max_score >= 40:
            stage = 5
            stage_chose = 5
        if max_score >= 50:
            stage = 6
        if max_score >= 60:
            stage = 7
        if max_score >= 70:
            stage = 8
        if max_score >= 80:
            stage = 9
        if max_score >= 90:
            stage = 10
            
    if lives <0:
        lives_out = True
        lives = 0
                
            
    # DRAW section
    # clear the screen
    if bomb_yes == False:
        screen.fill((red_value,0,0))
    # draw objects
    shooter.draw(screen)
    ground.draw(screen)
    for obj in objects:
        obj.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for bomb in bombs:
        bomb.draw(screen)  
    if explosion_blast:
        explosion_blast.draw(screen)
        explosion_blast.update(dt)
    # display running score in the corners
    scoreboard = font.render(f"Score:{score}", True, (0, 255,0))
    screen.blit(scoreboard, (screen.get_width() - 100, 18))
    
    live_remain = font.render(f"X{lives}", True, (255,255,255))
    screen.blit(live_remain, (screen.get_width()-100, screen.get_height()-36))
    life_shoot.draw(screen)
    
    stage_disp = font.render(f"Stage: {stage}", True, (red_value,0,0))
    screen.blit(stage_disp, (10, height - 40))
    # display game over
    if lives_out:
        shooter.pos = [-150,-150]
        paused = True
        screen.fill((0,0,0))
        game_over = overFont.render("GAME OVER", True, (255,0,0))
        final_score = overFont.render(f"Your Max Score Was: {max_score}!", True, (255,0,0))
        screen.blit(game_over, (screen.get_width()/2,screen.get_height()/2 ))
        screen.blit(final_score, (screen.get_width()/2 - 200,screen.get_height()/2 + 50 ))

    # update the display
    pygame.display.update()
    clock.tick(fps)

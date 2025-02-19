import pygame
from pygame.math import Vector2
from pygame.locals import *
import random
from physics_objects import Circle, Wall
from forces import *
import contact

# Initialize pygame and open window
pygame.init()
window = pygame.display.set_mode(flags=FULLSCREEN)
bg_color = (0, 190, 0)

# Timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# Stages
PLACING_BALL = 0
AIMING_THROW = 1
CHARGING_THROW = 2
BALLS_ROLLING = 3
DISPLAY_ROUND_RESULT = 4
GAME_END = 5

game_stage = AIMING_THROW

charging_time = 0
aim_direction = 0


turns = 0

current_ball = None

pallino_placement = True

player_turn = 0
player_scores = [0,0]
balls_thrown = [0,0]
scoring_balls = []

# Set objects
#Gray Circle
gray_circle = Circle(radius = 200, pos = (window.get_width()-200, window.get_height()-200), color = (75,75,75))
gray_circle.draw(window)

#Pallino
pallino = Circle(radius = 10, color = (255,255,255),pos = (window.get_width()-200, window.get_height()-200), mass = .5)

#objects list and appending
objects = []
objects.append(gray_circle)

balls = []
    
top_wall = Wall(point1= (0,0), point2 = (window.get_width(), 0), color = (255,255,255))
bottom_wall = Wall(point1 = (window.get_width(),window.get_height()), point2 = (0, window.get_height()), color = (255,255,255), width = 10)
left_wall = Wall(point1 = (0,window.get_height()), point2 = (0, 0), color = (255,255,255))
right_wall = Wall(point1 = (window.get_width(), 0), point2 = (window.get_width(), window.get_height()), color = (255,255,255), width = 10)

walls = [top_wall, bottom_wall, left_wall, right_wall]

objects.extend(walls)
objects.extend(balls)

current_ball = pallino
# Set forces
mu = .3
g = 98
restitution_ball_ball = .5
restitution_ball_wall = 0.3
restitution_pallino_ball = 0.1
restitution_pallino_wall = .5

## friction
friction_force = FrictionForce(mu, g)

# Fonts
font = pygame.font.SysFont('comicsansms', 36, False, False)
# game loop
game_end = False
while not game_end:
    pallino_stopped = pallino.vel.length() < mu * g * dt

    #print(turns)
    pygame.display.update()
    dt = clock.tick(fps) / 1000
    window.fill(bg_color)
    
    # EVENT loop
    while event := pygame.event.poll():
        # Quitting game
        if (event.type == QUIT 
            or (event.type == KEYDOWN
                and event.key == K_ESCAPE)):
            game_end = True
        # Placing a new ball in the gray area
        if game_stage == PLACING_BALL:
            if event.type == MOUSEBUTTONDOWN:
                click_pos = Vector2(event.pos)
                if turns < 8 and pallino_placement == False:
                    if gray_circle.contains_point(click_pos):
                        if player_turn == 1 and pallino_stopped:
                            blue_ball = Circle(radius = 21, color = (0,0,255), mass = .910)
                            balls.append(blue_ball)
                            objects.append(blue_ball)
                            balls[turns].pos = click_pos
                            current_ball = balls[turns]
                            balls_thrown[0] +=1

                            game_stage = AIMING_THROW
                            
                        elif player_turn == 2 and pallino_stopped:
                            yellow_ball = Circle(radius = 21, color = (255,255,0), mass = .910)
                            balls.append(yellow_ball)
                            objects.append(yellow_ball)
                            balls[turns].pos = click_pos
                            current_ball = balls[turns]
                            balls_thrown[1] +=1

                            game_stage = AIMING_THROW
        if game_stage == AIMING_THROW:
            #event.type = None
            if current_ball:
                mouse_pos = Vector2(pygame.mouse.get_pos())
                #aim_direction = (mouse_pos - current_ball.pos).normalize()
                
                pygame.draw.line(window, (255,255,255), current_ball.pos, mouse_pos, 2)
                
            if event.type == MOUSEBUTTONDOWN:
                charge_start_time = pygame.time.get_ticks()
                game_stage = CHARGING_THROW
                
                
                    
        # Charging a ball for a throw
        if game_stage == CHARGING_THROW:
            if current_ball:
                mouse_pos = Vector2(pygame.mouse.get_pos())
                pygame.draw.line(window, (255,0,0), current_ball.pos, mouse_pos)
                
            if event.type == MOUSEBUTTONUP and event.button == 1:
                release_time = pygame.time.get_ticks()
                charge_duration = (release_time - charge_start_time) /1000.0
                max_velocity = 325
                initial_velocity = min(charge_duration * max_velocity, max_velocity)
                if mouse_pos != current_ball.pos:
                    direction = (mouse_pos - current_ball.pos).normalize()
                    current_ball.vel = direction * initial_velocity
                game_stage = BALLS_ROLLING
        # Releasing the ball to roll           

        # Going forward after the round ends
    # GAME
    # Check for balls rolling slow enough to stop
    if game_stage == BALLS_ROLLING:
        if pallino_placement == True:
            game_stage = DISPLAY_ROUND_RESULT
        all_balls_stopped = None
        for ball in balls:
            all_balls_stopped = all(ball.vel.length() < mu * g * dt for ball in balls)
        if all_balls_stopped and pallino_stopped:
            balls.sort(key=lambda x: (x.pos - pallino.pos).magnitude())
            for ball in balls:
                ball.vel = Vector2(0,0) 
            closest_ball_distance = (balls[0].pos - pallino.pos).magnitude()
            scoring_balls = [ball for ball in balls if (ball.pos - pallino.pos).magnitude() <= closest_ball_distance]
            game_stage = DISPLAY_ROUND_RESULT
            
    if turns == 7 and game_stage == DISPLAY_ROUND_RESULT:
        game_stage = GAME_END
    #Display Round Result
    if game_stage == DISPLAY_ROUND_RESULT:
        for ball in scoring_balls:
            if ball.color == (255,255,0):
                player_scores[1] += 1
                if balls_thrown[0] <4:
                    player_turn = 1
                elif balls_thrown[0] >=4:
                    player_turn = 2
            if ball.color == (0,0,255):
                player_scores[0] +=1
                if balls_thrown[1] < 4:
                    player_turn = 2
                elif balls_thrown[1] >= 4:
                    player_turn = 1
        
        if pallino_placement == True:
            pallino_placement = False
            player_turn = 1
            current_ball = None
            game_stage = PLACING_BALL
        elif turns < 8 and pallino_placement == False:
            turns +=1
            if turns >= 8:
                game_stage == GAME_END
            game_stage = PLACING_BALL
    # Check if all balls have been thrown and have stopped
    # Start new turn if all balls are stopped

    # PHYSICS
    # clear all forces
    for obj in objects+balls+walls:
        obj.clear_force()
    pallino.clear_force()
    # apply all forces
    for ball in balls:
        friction_force.apply(ball)
    friction_force.apply(pallino)
    # update all objects
    for obj in objects+balls+walls:
        obj.update(dt)
    pallino.update(dt)
    # process collisions
    if game_stage == BALLS_ROLLING:

        for ball in balls:
            for other_ball in balls:
                if ball != other_ball:
                    ct = contact.generate(ball, other_ball, restitution = restitution_ball_ball)
                    if ct.overlap > 0:
                        ct.resolve()

            for wall in walls:
                ct = contact.generate(ball, wall, restitution = restitution_ball_wall)
                if ct.overlap > 0:
                    ct.resolve()

            ct = contact.generate(pallino, ball, restitution = restitution_pallino_ball)
            if ct.overlap > 0:
                ct.resolve()

    for wall in walls:
        ct = contact.generate(pallino, wall, restitution = restitution_pallino_wall)
        if ct.overlap > 0:
            ct.resolve() 
                

    # DRAW
    # draw objects
    for obj in objects + balls + walls:
        obj.draw(window)
        pallino.draw(window)
    # draw aiming line
    if game_stage == AIMING_THROW:
        pygame.draw.line(window, (255, 255, 255), current_ball.pos, mouse_pos, 2)
    elif game_stage == CHARGING_THROW:
        pygame.draw.line(window, (255, 0, 0), current_ball.pos, mouse_pos, 2)

    # highlight balls
    for ball in balls:
        if ball in scoring_balls and pallino_stopped and all_balls_stopped:
            pygame.draw.circle(window, center = ball.pos, color = (255,255,255), radius = ball.radius + 5)
            ball.draw(window)
            if ball.color == (255,255,0):
                text = font.render("PLAYER 2 SCOREDDDDDD!!!!!!!", True, (255,255,255))
                window.blit(text, (window.get_width()/3, window.get_height()/2))
            if ball.color == (0,0,255):
                text = font.render("PLAYER 1 SCOREDDDDDD!!!!!!!", True, (255,255,255))
                window.blit(text, (window.get_width()/3, window.get_height()/2))                
    # Draw messages on screen
    if player_turn == 0:
        text = font.render(f"Pallino is being placed...", True, (255,255,255))
    else:
        text = font.render(f"Player {player_turn} Turn", True, (255,255,255))
    window.blit(text, (window.get_width()/2, 10))
    
    if pallino_stopped == False:
        text = font.render("Pallino on the move...", True, (255,0,255))
        window.blit(text, (window.get_width()/2, 50))
    
    message = f"Player 1 has scored {player_scores[0]} points!"
    text = font.render(message, True, (255,0,0))
    window.blit(text, (window.get_width()/20, window.get_height() - 100))
    
    message = f"Player 2 has scored {player_scores[1]} points!"
    text = font.render(message, True, (255,0,0))
    window.blit(text, (window.get_width()/2, window.get_height() -100))
        
    if game_stage == GAME_END:
        keys = pygame.key.get_pressed()
        font = pygame.font.SysFont('timesnewroman', 50, False, False)
        text = font.render("Game Over! Press Space to Exit", True, (255,0,0))
        window.blit(text, (window.get_width()/3.5, window.get_height()/1.5))
        if keys[K_SPACE]:
            game_end = True

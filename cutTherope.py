import random
from numpy import cross
import pygame
from pygame.constants import *
from pygame.math import Vector2, Vector3
import math
from physics_objects import *  # copy in physics_objects.py from your previous project
from forces import *
import contact

# INITIALIZE PYGAME AND OPEN WINDOW
pygame.init()
window = pygame.display.set_mode([800, 600])

# SETUP TIMING
fps = 120
dt = 1/fps
clock = pygame.time.Clock()

fail_counter = 0
level = 0
max_level = 0

candy = Circle(radius = 12, color = (175, 70, 40), pos = Vector2(window.get_width()/2, 150), mass = 3)
om_nom = Circle(radius = 21, color = (0,175,55), fixed = True, pos = Vector2(window.get_width()/2,479))
bubble = Circle(radius = 18, color = (24,18,140), pos = Vector2(window.get_width()/2-150, window.get_height()/2))

anchors = []

#All of the anchor points for ropes
anchor_one = Circle(pos = (window.get_width()/2, 100), radius = 20, color = (175,175,175), static = True)
anchor_two = Circle(pos = (window.get_width()/2 - 200, 100), radius = 20, color = (175,175,175), static = True)
anchor_three = Circle(pos = (window.get_width()/2 + 200, 100), radius = 20, color = (175,175,175), static = True)

anchors_one = [anchor_one, anchor_two, anchor_three]

anchor_four = Circle(pos = (window.get_width() - 50, window.get_height() - 500), radius = 20, color = (175,175,175), static = True)
anchor_five = Circle(pos = (window.get_width()/2 + 100, window.get_height() - 500), radius = 20, color = (175,175,175), static = True)
anchor_six = Circle(pos = (window.get_width()/2 - 300, window.get_height() - 400), radius = 20, color = (175,175,175), static = True)
anchor_seven = Circle(pos = (window.get_width()/2 - 10, window.get_height()-450), radius = 20, color =(175,175,175), static = True)
anchors_two = [anchor_four, anchor_five, anchor_six, anchor_seven]

#additive bonds
bonds_addition_points = []

bond_addition = Circle(pos = Vector2(130, window.get_height() - 150), radius = 45, color = (52, 27, 200), static = True, width = 2, mass = math.inf)
bond_addition1 = Circle(pos = (window.get_width()/2 - 170, window.get_height() - 250), radius = 45, color = (52, 27, 200), static = True, width = 2, mass = math.inf)
bond_addition2 = Circle(pos = (window.get_width()/2 - 60, window.get_height() - 330), radius = 45, color = (52, 27, 200), static = True, width = 2, mass = math.inf)
bond_addition3 = Circle(pos = (window.get_width()/2 + 60, window.get_height() - 420), radius = 45, color = (52, 27, 200), static = True, width = 2, mass = math.inf)
bond_addition4 = Circle(pos = Vector2(window.get_width()/2 - 270, window.get_height()/2 - 150), radius = 45, color = (52,27,200), static = True, width = 2, mass = math.inf)
bond_addition5 = Circle(pos = Vector2(window.get_width()/2 - 140, window.get_height()/2 - 200), radius = 45, color = (52,27,200), static = True, width = 2, mass = math.inf)

bondoidsThree = [bond_addition, bond_addition1, bond_addition2, bond_addition3, bond_addition4,bond_addition5]

bond_addition6 = Circle(pos = Vector2(window.get_width() - 255, window.get_height()/2 + 90), radius = 55, color = (52,27,200), static = True, width = 2, mass = math.inf)
bond_addition7 = Circle(pos = Vector2(window.get_width()/2, window.get_height()/2 + -220), radius = 40, color = (52,27,200), static = True, width = 2, mass = math.inf)
bond_addition8 = Circle(pos = Vector2(window.get_width()/2 - 150, window.get_height()/2 + -170), radius = 40, color = (52,27,200), static = True, width = 2, mass = math.inf)
bond_addition9 = Circle(pos = Vector2(window.get_width()/2 - 350, window.get_height()/2 + -170), radius = 40, color = (52,27,200), static = True, width = 2, mass = math.inf)

bondoidsFour = [bond_addition6, bond_addition7, bond_addition8, bond_addition9]

anchor_eight = Circle(pos = (130, window.get_height() -150), radius = 20, color = (175,175,175), static = True)
anchor_nine = Circle(pos = (window.get_width()/2 - 170, window.get_height() -250), radius = 20, color = (175,175,175), static = True)
anchor_ten = Circle(pos = (window.get_width()/2 - 60, window.get_height() -330), radius = 20, color = (175,175,175), static = True)
anchor_eleven = Circle(pos = (window.get_width()/2 + 60, window.get_height() -420), radius = 20, color = (175,175,175), static = True)
anchor_twelve = Circle(pos = Vector2(window.get_width()/2 - 270, window.get_height()/2 - 150), radius = 20, color = (175,175,175), static = True)
anchor_thirteen = Circle(pos = Vector2(window.get_width()/2 - 140, window.get_height()/2 - 200), radius = 20, color = (175,175,175), static = True)

anchors_three = [anchor_eight, anchor_nine, anchor_ten, anchor_eleven, anchor_twelve, anchor_thirteen]



anchor_fourteen = Circle(pos = Vector2(window.get_width() - 100, window.get_height()/2), radius = 20, color = (175,175,175), static = True)
anchors_four = [anchor_fourteen]

anchor_fifteen = Circle(pos = Vector2(window.get_width() - 255, window.get_height()/2 + 90), radius = 20, color = (175,175,175), static = True)
anchor_sixteen = Circle(pos = Vector2(window.get_width()/2 , window.get_height()/2 + -220), radius = 20, color = (175,175,175), static = True)
anchor_seventeen = Circle(pos = Vector2(window.get_width()/2 - 150, window.get_height()/2 + -170), radius = 20, color = (175,175,175), static = True, width = 2)
anchor_eighteen = Circle(pos = Vector2(window.get_width()/2 - 350, window.get_height()/2 + -170), radius = 20, color = (175,175,175), static = True, width = 2)


anchors_additive_four = [anchor_fifteen, anchor_sixteen, anchor_seventeen, anchor_eighteen]

#whoopie
big_whoop = Circle(pos = Vector2(window.get_width() - 50, window.get_height()/2 + 150), radius = 17, color = (255, 200, 210), static = True)
big_whoop2 = Circle(pos = Vector2(window.get_width()/2 + 60, window.get_height()/2 - 160), radius = 17, color = (255,200,210), static = True)
big_whoop3 = Circle(pos = Vector2(window.get_width()/2 - 40, window.get_height()/2 - 120), radius = 17, color = (255,200,210), static = True)
big_whoop4 = Circle(pos = Vector2(window.get_width()/2 - 245, window.get_height()/2 - 145), radius = 17, color = (255,200,210), static = True)
whoopie = [big_whoop,big_whoop2, big_whoop3,big_whoop4]


#gravity pointsp
gravity = []

plat_points = [
    [0,0],
    [0,25],
    [100,25],
    [100,0]
]

player_platform = Polygon(local_points = plat_points, pos = (window.get_width()/2,500), static = True)

hard_objects = [player_platform]

bubble_trap = False

y_true = False

snipped = False
time = 0
snip_point = Vector2(0,0)

#collecting the little yellow circles
bonus_score = 0
bonusOne = Circle(pos = Vector2(window.get_width()/2 - 250, window.get_height()/2 + 15), radius = 5, color = (255,255,0), static = True)
bonusTwo = Circle(pos = Vector2(window.get_width()/2 + 250, window.get_height()/2 + 15), radius = 5, color = (255,255,0), static = True)
bonOneList = [bonusOne, bonusTwo]

bonusThree =  Circle(pos = Vector2(window.get_width()/2 - 100, window.get_height()/2), radius = 5, color = (255,255,0), static = True)
bonusFour = Circle(pos = Vector2(window.get_width()/2 + 170, window.get_height()/2 - 47), radius = 5, color = (255,255,0), static = True)
bonTwoList = [bonusThree, bonusFour]

bonusFive = Circle(pos = Vector2(window.get_width()/2 - 270, window.get_height()/2 - 55), radius = 5, color= (255,255,0,), static = True)
bonusSix = Circle(pos = Vector2(window.get_width()/2 - 130, window.get_height()/2 - 75), radius = 5, color = (255,255,0), static = True)
bonThreeList = [bonusFive, bonusSix]

bonusSeven = Circle(pos = Vector2(window.get_width()/2 + 20, window.get_height()/2), radius = 5, color = (255,255,0), static = True)
bonusEight = Circle(pos = Vector2(window.get_width()/2 - 100, window.get_height()/2 - 199), radius = 5, color = (255,255,0), static = True)
bonFourList = [bonusSeven, bonusEight]

bonus_items = []

overlap= None

#cutting tools
clicked = False
cutting_sphere = None

#menu variable
menu = True

#tutorial Variables
tutorial = True
bubble_tutorial = False
draw_tutorial = False
whoopie_tutorial = False
game_win = False

running = True
level_pos = (0,0)
bonds = None
repulsion = None
click_line = None

clock.tick()
while running:
    # DISPLAY
    pygame.display.update()
    # TIMING
    clock.tick(fps)
    # BACKGROUND GRAPHICS
    window.fill([187,142,81])
    mouse_pos = Vector2(pygame.mouse.get_pos())
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        if event.type == MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        elif event.type == MOUSEBUTTONDOWN and clicked == True:
            clicked = False
        if event.type == KEYDOWN and event.key == K_p and menu == True:
            menu = False
            tutorial = True
        if event.type == KEYDOWN and event.key == K_k and tutorial == True:
            tutorial = False
            level = 1
        if event.type == KEYDOWN and event.key == K_k and bubble_tutorial == True:
            bubble_tutorial = False
            level = 2
            level_pos = Vector2(window.get_width() - 100, window.get_height()-150)
            candy.pos = level_pos
        if event.type == KEYDOWN and event.key == K_k and draw_tutorial == True:
            draw_tutorial = False
            bubble_trap = False
            level = 3
            level_pos = Vector2(75, window.get_height() - 60)
            candy.pos = level_pos
            bubble.pos = level_pos
        if event.type == KEYDOWN and event.key == K_k and whoopie_tutorial == True:
            whoopie_tutorial = False
            bubble_trap = False
            level = 4
            level_pos = Vector2(window.get_width() - 65, window.get_height()- 60)
            candy.pos = level_pos
            bubble.pos = Vector2(window.get_width()/2, window.get_height()/2 + 155)
    if level > 0 and tutorial == False:
        if clicked == True:
            cutting_sphere = Circle(pos = mouse_pos, radius = 15, color = (175,0,0))
        if clicked == False:
            cutting_sphere = None
            
    if fail_counter != 3 and game_win == False:
        #clear forces
        candy.clear_force()
        om_nom.clear_force()  
        for obj in anchors:
            obj.clear_force()
            
        #gravity
        if bubble_trap == False and level !=0:
            gravity = Gravity (acc = (0,100), objects_list = [candy])
            gravity.apply()
        elif bubble_trap == True and level != 0:
            gravity = Gravity (acc = (0,-10), objects_list = [candy])
            gravity.apply()
        
        #candy_om_nom collision
        c = contact.generate(candy, om_nom)
        if c.overlap > 0:
            if level == 1:
                max_level = 1
                bubble_tutorial = True
            if level == 2:
                max_level = 2
                draw_tutorial = True
            if level == 3:
                max_level = 3
                whoopie_tutorial = True
            if level == 4:
                max_level = 4
                game_win = True
            bonds = None
            anchors = []
            clicked = False
            level = 0
            bubble_trap = False
            candy.vel = Vector2(0,0)
            cutting_sphere = None
            bonus_items = []
            bonds_addition_points = []
            
            
        #Candy_bubble_collision
        c = contact.generate(candy, bubble)
        if c.overlap > 0 and level != 1:
            bubble.pos = candy.pos
            bubble_trap = True
    #different levels
    if level == 1 and fail_counter != 3:
        anchors = anchors_one
        bonus_items = bonOneList
        level_pos = (window.get_width()/2-100,150)
        player_platform.pos = (window.get_width()/2 - 50,500)
        for obj in anchors:
            bonds = SpringForce(stiffness = 20, damping = 15, natural_length = 200, pairs_list = [[obj, candy]])
            bonds.apply()
            bonds.draw(window)
            repulsion = SpringRepulsion(objects_list = [[obj,candy]])
            repulsion.apply()
            
            if mouse_pos and cutting_sphere:
                r = cutting_sphere.pos - bonds.start_pos
                y_rad = cutting_sphere.pos.y
                if r.dot(bonds.normal) > 0:
                    if bonds.start_pos.y < bonds.end_pos.y:
                        if y_rad > bonds.start_pos.y and y_rad < bonds.end_pos.y:
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()                            
                if clicked == True:
                    if overlap and overlap > 0 and y_true == True:
                        bonds.remove_bonds(obj)
                        anchors_one.remove(obj)
                        overlap = 0
                        snipped = True
                        snip_point = cutting_sphere.pos
            
    #--------------------------------------------------------------------------   
    if level == 2 and fail_counter != 3:
        anchors = anchors_two
        player_platform.pos = Vector2(150,100)
        bonus_items = bonTwoList
        level_pos =  Vector2(window.get_width() - 100, window.get_height()-150)
        om_nom.pos = player_platform.pos + Vector2(50, -21)

        for obj in anchors:
            bonds = SpringForce(stiffness = 20, damping = 15, natural_length = 200, pairs_list = [[obj, candy]])
            bonds.apply()
            bonds.draw(window)
            repulsion = SpringRepulsion(objects_list = [[obj,candy]])
            repulsion.apply()
            if mouse_pos and cutting_sphere:
                r = cutting_sphere.pos - bonds.start_pos
                if r.dot(bonds.normal)>0:
                    if bonds.start_pos.y < bonds.end_pos.y:
                        y_rad = cutting_sphere.pos.y
                        if (y_rad > bonds.start_pos.y and y_rad < bonds.end_pos.y):
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()                            
                    if bonds.end_pos.y < bonds.start_pos.y:
                        y_rad = cutting_sphere.pos.y
                        if (y_rad > bonds.end_pos.y and y_rad < bonds.start_pos.y):
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()
                if clicked == True:
                    if overlap and overlap > 0 and y_true == True:
                        bonds.remove_bonds(obj)
                        anchors_two.remove(obj)
                        overlap = 0
                        snipped = True
                        snip_point = cutting_sphere.pos
 
        #-------------------------------------------------------------------
    if level == 3 and fail_counter != 3:
        #anchors = anchors_three
        player_platform.pos = Vector2(window.get_width()/2, 100)
        om_nom.pos = player_platform.pos + Vector2(50,-21)
        bonus_items = bonThreeList
        bonds_addition_points = bondoidsThree
        bonds = None
        level_pos = Vector2(75, window.get_height() - 60)
        for i, obj in enumerate((bonds_addition_points)):
            c = contact.generate(obj, bubble, resolve = True, restitution = 1)
            if c.overlap > 0:
                anchors.append(anchors_three[i])
        for obj in anchors:
            bonds = SpringForce(stiffness = 20, damping = 15, natural_length = 100, pairs_list = [[obj, candy]])
            bonds.apply()
            bonds.draw(window)
            repulsion = SpringRepulsion(objects_list = [[obj,candy]])
            repulsion.apply()
            if mouse_pos and cutting_sphere and bonds:
                r = cutting_sphere.pos - bonds.start_pos
                if r.dot(bonds.normal)>0:
                    if bonds.start_pos.y < bonds.end_pos.y:
                        y_rad = cutting_sphere.pos.y
                        if (y_rad > bonds.start_pos.y and y_rad < bonds.end_pos.y):
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()       
                    if bonds.end_pos.y < bonds.start_pos.y:
                        y_rad = cutting_sphere.pos.y
                        if (y_rad > bonds.end_pos.y and y_rad < bonds.start_pos.y):
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()
                if clicked == True:
                    if overlap and overlap > 0 and y_true == True:
                        bonds.remove_bonds(obj)
                        anchors.remove(obj)
                        overlap = 0
                        snipped = True
                        snip_point = cutting_sphere.pos
    #-----------------------------------------------------------------------------------------------------------------
    if level == 4 and fail_counter < 3:
        player_platform.pos = Vector2(0, window.get_height()/2)
        om_nom.pos = player_platform.pos + Vector2(50,-21)
        bonds = None
        bonus_items = bonFourList
        bonds_addition_points = bondoidsFour
        level_pos = Vector2(window.get_width() - 65, window.get_height()- 60)

        anchors = anchors_four
        for i, obj in enumerate((bonds_addition_points)):
            c = contact.generate(obj, candy, resolve = True, restitution = 1)
            if c.overlap > 0:
                anchors.append(anchors_additive_four[i])
        
        for obj in anchors:
            bonds = SpringForce(stiffness = 20, damping = 15, natural_length = 150, pairs_list = [[obj,candy]])
            bonds.apply()
            bonds.draw(window)
            repulsion = SpringRepulsion(objects_list = [[obj,candy]])
            repulsion.apply()
            if mouse_pos and cutting_sphere and bonds:
                r = cutting_sphere.pos - bonds.start_pos
                if r.dot(bonds.normal)>0:
                    if bonds.start_pos.y < bonds.end_pos.y:
                        y_rad = cutting_sphere.pos.y
                        if (y_rad > bonds.start_pos.y and y_rad < bonds.end_pos.y):
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()
                    if bonds.end_pos.y < bonds.start_pos.y:
                        y_rad = cutting_sphere.pos.y
                        if (y_rad > bonds.end_pos.y and y_rad < bonds.start_pos.y):
                            y_true = True
                            overlap = cutting_sphere.radius - r.dot(bonds.normal)
                            bonds.normal = bonds.normal.normalize()
                if clicked == True:
                    if overlap and overlap > 0 and y_true == True:
                        bonds.remove_bonds(obj)
                        anchors.remove(obj)
                        overlap = 0
                        snipped = True
                        snip_point = cutting_sphere.pos

    #------------------------------------------------------------------------------------------------------------------------
    if fail_counter != 3 and game_win == False:
        if bubble_trap == False:
            for obj in hard_objects:
                c = contact.generate(candy, obj,resolve = True)
            
        for obj in whoopie:
            if level == 4:
                obj.draw(window)
                obj.update(dt)
                obj.color = (255,200,210)
                keys = pygame.key.get_pressed()
                directional_vector = candy.pos - obj.pos
                if abs(candy.pos.x - obj.pos.x) < 95 and abs(candy.pos.y - obj.pos.y) < 95:
                    obj.color = (180,120,100)
                    if obj.contains_point(mouse_pos) and keys[K_SPACE]:
                        candy.vel += directional_vector.normalize() * 10
        
        for bon in bonus_items:
            c = contact.generate(candy, bon)
            bon.draw(window)
            bon.update(dt)
            if c.overlap > 0:
                bonus_score += 1
                bonus_items.remove(bon)
                
        #draw Objects
        if level != 0:
            player_platform.draw(window)
            om_nom.draw(window)
            if level != 1:
                bubble.draw(window)
            if level != 2 and level != 1:
                for obj in bonds_addition_points:
                    obj.draw(window)
            candy.draw(window)
            for obj in anchors:
                obj.draw(window)
        
        #update objects
        if cutting_sphere:
            cutting_sphere.draw(window)
            cutting_sphere.update(dt)
        candy.update(dt)
        om_nom.update(dt)
        if level != 1:
            bubble.update(dt)
        player_platform.update(dt)
        for belt in bonds_addition_points:
            belt.update(dt)
        for obj in anchors:
            obj.update(dt)

    #Fail Check:
    if candy.pos.y < 0 or candy.pos.y > window.get_height() or candy.pos.x < 0 or candy.pos.x > window.get_width():
            fail_counter += 1
            candy.pos = (level_pos)
            candy.vel = Vector2(0,0)
            press_spot = None
            if level == 1:
                anchors_one = [anchor_one, anchor_two, anchor_three]
            elif level == 2:
                bubble.pos = Vector2(window.get_width()/2-150, window.get_height()/2)
                anchors_two = [anchor_four, anchor_five, anchor_six, anchor_seven]
            elif level == 3:
                bubble.pos = level_pos
                anchors_three = [anchor_eight, anchor_nine, anchor_ten, anchor_eleven, anchor_twelve, anchor_thirteen]
            elif level == 4:
                anchors_four = [anchor_fourteen]
                bubble.pos = Vector2(window.get_width()/2, window.get_height()/2 + 155)

            if bubble_trap == True:
                bubble_trap = False
            
            if fail_counter == 1:
                fail_counter = 1
            if fail_counter == 2:
                fail_counter = 2
            if fail_counter >= 3:
                fail_counter = 3
                
                
                
    bigFont = pygame.font.SysFont('comicsansms', 36, True, True)
    smallFont = pygame.font.SysFont('comicsansms', 16, True, True)
    mediumFont = pygame.font.SysFont('comicsansms', 24, True, True)
    #check if lost
    if fail_counter == 3:
        end_of_game = bigFont.render(f"Game Over, Press Escape to Exit", True, (255,0,0))
        window.blit(end_of_game, (window.get_width()/2 - 280, window.get_height()/2))
        tiny_tip = mediumFont.render(f"You made it to level: {max_level}", True, (255,0,0))
        window.blit(tiny_tip, (window.get_width()/2 - 140, window.get_height()/2 + 50))
        bonus_text = smallFont.render(f"You got: {bonus_score} Extra Points", True, (255,0,0))
        window.blit(bonus_text, (window.get_width()/2 - 90, window.get_height()/2 + 100))
    
    if menu == True:
        tutorial = False
        oh_my_god = Circle(pos = Vector2(window.get_width()/2, window.get_height()), radius = 250, color = (0,175,0))
        eyeOne = Circle(pos = Vector2(window.get_width()/2 - 100, window.get_height() - 150), radius = 30, color = (255,255,255))
        eyeTwo = Circle(pos = Vector2(window.get_width()/2 + 100, window.get_height()-150), radius = 30, color = (255,255,255))
        pupilOne = Circle(pos = eyeOne.pos, radius = 15, color = (0,0,0))
        pupilTwo = Circle(pos = eyeTwo.pos, radius = 15, color = (0,0,0))
        
        tri_arrow = Polygon(local_points = [[0,0], [50, 25], [50, -25]], pos = Vector2(window.get_width()/2 + 200, window.get_height() - 200), angle = -65)
        tri_arrow.draw(window)
        tri_rect = Polygon(local_points = plat_points, pos = Vector2(window.get_width()/2 + 210, window.get_height() - 250), angle = -65)
        tri_rect.draw(window)
        
        oh_my_god.draw(window)
        eyeOne.draw(window)
        eyeTwo.draw(window)
        pupilOne.draw(window)
        pupilTwo.draw(window)
        
        cut_the_rope = bigFont.render(f"Cut The Rope!", True, (255,255,255))
        window.blit(cut_the_rope, (window.get_width()/2 - 130, window.get_height()/2 - 150))
        
        continue_text = smallFont.render(f"Press p to start", True, (255,255,255))
        window.blit(continue_text, (window.get_width()/2 - 75, window.get_height()/2 - 100))
        
        does_he_know = smallFont.render(f"he doesn't know physics", True, (255,255,255))
        window.blit(does_he_know, (window.get_width()/2 + 190, window.get_height() - 360))
        
    #The tutorial UI
    if tutorial == True:
        tutorial_mesg = mediumFont.render("To play, press the mouse in order to form the cut", True, (255,255,255))
        tutorial_mesg_two = mediumFont.render("Try to make the cuts necessary to get the candy to Om-Nom!", True, (255,255,255))
        window.blit(tutorial_mesg, (window.get_width()/2 - 325, 200))
        window.blit(tutorial_mesg_two, (window.get_width()/2 - 375, 300))
        tell_end = mediumFont.render("Press K to begin the game", True, (255,255,255))
        window.blit(tell_end, (window.get_width()/2 - 150, 400))
        
    #The tutorial bubble UI
    if bubble_tutorial == True:
        tutorial_mesg = mediumFont.render("Congrats you passed level 1!", True, (255,255,255))
        tutorial_mesg_two = mediumFont.render("Some bubbles have begun to appear...", True, (255,255,255))
        window.blit(tutorial_mesg, (window.get_width()/2 - 200, 200))
        window.blit(tutorial_mesg_two, (window.get_width()/2 - 250, 300))
        tell_end = mediumFont.render("Press K to continue", True, (255,255,255))
        window.blit(tell_end, (window.get_width()/2 - 150, 400))

    #tutorial for bond_additions
    if draw_tutorial == True:
        tutorial_mesg = mediumFont.render("You passed level 2!", True, (255,255,255))
        tutorial_mesg_two = mediumFont.render("Hey, can you grab rope from there?", True, (255,255,255))
        window.blit(tutorial_mesg, (window.get_width()/2 - 175, 200))
        window.blit(tutorial_mesg_two, (window.get_width()/2 - 250, 300))
        tell_end = mediumFont.render("Press K to continue", True, (255,255,255))
        window.blit(tell_end, (window.get_width()/2-150, 400))
    
    #tutorial for the whoopie cushion
    if whoopie_tutorial == True:
        tutorial_mesg = mediumFont.render("You passed level 3!", True, (255,255,255))
        tutorial_mesg_two = mediumFont.render("Press space on the cushion to push the candy!", True, (255,255,255))
        window.blit(tutorial_mesg, (window.get_width()/2 - 175, 200))
        window.blit(tutorial_mesg_two, (window.get_width()/2 - 270, 300))
        tell_end = mediumFont.render("Press K to continue", True, (255,255,255))
        window.blit(tell_end, (window.get_width()/2-150, 400))
        
    #win screen
    if game_win == True:
        end_of_game = bigFont.render(f"You Won!, Press Escape to Exit", True, (0,255,0))
        window.blit(end_of_game, (window.get_width()/2 - 280, window.get_height()/2))
        tiny_tip = mediumFont.render(f"You made it to level: {max_level}", True, (0,255,0))
        window.blit(tiny_tip, (window.get_width()/2 - 140, window.get_height()/2 + 50))
        bonus_text = smallFont.render(f"You got: {bonus_score} Extra Points", True, (0,255,0))
        fail_count = smallFont.render(f"You failed: {fail_counter} Times", True, (255,0,0))
        window.blit(bonus_text, (window.get_width()/2 - 90, window.get_height()/2 + 100))
        window.blit(fail_count, (window.get_width()/2 -90, window.get_height()/2 + 82))
        
    #draw little snipped notification
    if snipped == True:
        time += dt
        if time < .5:
            snippy = smallFont.render(f"Snip!", True, (12,210,54))
            window.blit(snippy, (snip_point + Vector2(15,0)))
        elif time > .5:
            time = 0
            snipped = False
            
    #draw everything that stays the entire time
    if tutorial == True or bubble_tutorial == True:
        level_counter = smallFont.render(f"Level:Tutorial", True, (255,255,255))
    elif menu == True:
        level_counter = smallFont.render(f"Level:Menu!", True, (255,255,255))
    elif game_win == True:
        level_counter = smallFont.render("Level: Win!" , True, (0,255,0))
    else:
        level_counter = smallFont.render(f"Level:{level}", True, (255,255,255))
        
    fail_text = smallFont.render(f"You have Failed: {fail_counter} times", True, (255,0,0))
    score_text = smallFont.render(f"You earned: {bonus_score} extra points!", True, (0,255,0))

    pygame.draw.line(window, color= (255,0,0), start_pos = Vector2(0,50), end_pos = Vector2(220,50), width = 1)
    pygame.draw.line(window,color = (255,0,0), start_pos = Vector2(220,0), end_pos = Vector2(220,50), width = 1)
    window.blit(fail_text, (10, 10))
    
    pygame.draw.line(window, color = (255,255,255), start_pos = Vector2(window.get_width(), 50), end_pos = Vector2(window.get_width()-130, 50), width = 1)
    pygame.draw.line(window, color = (255,255,255), start_pos = Vector2(window.get_width() - 130, 0), end_pos = Vector2(window.get_width()-130, 50), width = 1)
    window.blit(level_counter, (window.get_width()-115, 10))
    
    pygame.draw.line(window,color = (0,255,0), start_pos = Vector2(window.get_width()/2 - 115, 0), end_pos = Vector2(window.get_width()/2 - 115, 50), width = 1)
    pygame.draw.line(window,color = (0,255,0), start_pos = Vector2(window.get_width()/2 + 115, 0), end_pos = Vector2(window.get_width()/2 + 115, 50), width = 1)
    pygame.draw.line(window,color = (0,255,0), start_pos = Vector2(window.get_width()/2 - 115, 50), end_pos = Vector2(window.get_width()/2 + 115, 50), width = 1)
    window.blit(score_text, (window.get_width()/2-110, 10))
    
    # update the display
    #pygame.display.update()
    #clock.tick(fps)
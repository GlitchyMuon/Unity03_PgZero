# code pour changer où la fenêtre du jeu apparaît en l'initialisant.
# doit impérativement être mis avant l'import pgzrun !!!
x = 400
y = 280
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import pgzrun
from pgzhelper import *
# pgzhelper.py needs to be in the same folder as the project it needs to be imported in 
#from GIFImage_ext import *
from random import randint
from random import choice
from os import listdir
from os.path import isfile
from pathlib import Path
import pygame

#folder = Path(__file__).parent
#Path(folder, "images", "all_bricks")   #est le nom du chemin du dossier
#Path(folder, "images", "all_bricks", brick_file)   #ne fonctionne pas, il va metttre ses dossiers dans la librairie pgzero !


WIDTH = 800
HEIGHT = 600
bricks_screen_limit_y = 210

menu_visible = True
did_we_click = False
pause = False
is_win = False

menu_bg = Actor("daysky")
menu_bg.scale = 0.28
menu_bg.pos = [WIDTH/2, HEIGHT/2]

menu_img = Actor("airship")
menu_img.scale = 0.7
menu_img.pos = [WIDTH/2, HEIGHT/2]


game_bg = Actor("sunriseparallax")
game_bg.scale = 0.30
game_bg.pos = [WIDTH/2, HEIGHT/2]

game_easteregg = Actor("floatingisle_frame0_resized")
game_easteregg.scale = 0.2
game_easteregg.images =["floatingisle_frame0_resized", "floatingisle_frame1_resized", "floatingisle_frame2_resized", "floatingisle_frame3_resized", "floatingisle_frame4_resized", "floatingisle_frame5_resized"]
game_easteregg.pos= [randint(20, WIDTH-20), randint(20, bricks_screen_limit_y-50)] #20 cause at 0 crops the image
game_easteregg.fps= 6

game_over_img = Actor("flowerpetals")   #rosepetals
game_over_img.pos = [WIDTH/2-5, HEIGHT/2+66]

win_wind_fx = Actor("euclidean_vector_fx")
win_wind_fx.scale = 0.20
win_wind_fx.pos = [WIDTH/2, HEIGHT/2+200]

# win_lightfx = Actor("blue_sky_light") #only appears right bottom
# win_lightfx.scale = 0.5
# win_wind_fx.pos = [0, 0]

score = 0

all_bricks = []
speed_bricks = []
brick_width = 30
brick_height = 100
brick_names = []


for brick_file in listdir(r'images/all_bricks'):    #Path(folder, "images", "all_bricks")    #(r'images/all_bricks')    #works only if the correct main folder is open ! otherwise would need : from pathlib import Path   
        if isfile(r'images/all_bricks/' + brick_file ):       #(r'images/all_bricks/' + brick_file)
            brick_names.append(brick_file)

for y in range(0, 7 * brick_width, 30):
    # 100 est le pas, car la brique fait 100 de largeur, sinon elles se superposent
    for x in range(0, 8 * brick_height, 100):
        # autre façon : for y in range(10)       for x in range(0, 8, 1)/range(8)       brick.pos = [x * 100, y * 30]
        name = choice(brick_names)
        brick = Actor('all_bricks/' + name, anchor=["left", "top"])
        brick.pos = [x, y]
        all_bricks.append(brick)
        if name == "brick_colourful100x30.png":
            speed_bricks.append(brick)


player = Actor("airship_s")
player.pos = [WIDTH/2, 575]
player_width = 150
player_height = 40

ball = Actor("ball")
ball.pos = [WIDTH/2, 500]
ball.speed = [randint(1, 3), randint(-3, -1)]
ball.velocity = 1.5

ball_is_moving = False
ball_is_displayed = True
ball_in_cloud = False

cloud = Actor("cloud", anchor=["center", "bottom"])
cloud_width = 182
cloud_height = 32
cloud.pos = [randint(cloud_width//2, WIDTH-cloud_width//2), 
             randint(bricks_screen_limit_y+cloud_height//2+10, 
            player.top-30)]      #range((randint(0,WIDTH-192), randint(0, WIDTH-192)))       #WIDTH= 182 HEIGHT= 32    #226 -> 210 end of bricks : 16= half of 32   #36 -> 20 is half of zeppelin. 16 = half of cloud
cloud.speed = [randint(-1, 1)*50, randint(-1, 1)*50]
saved_cloud_pos = None
cloud_pos_ranges = [-11, -8, -5, 5, 8, 11]
cloud_speed_options = [-2, -1, 1, 2]





def update_menu():
    if not music.is_playing('into_the_ruins'):
        music.play_once('into_the_ruins')
        music.set_volume(0.5)
        music.get_volume()

def update_game(dt):
    global score, saved_cloud_pos, ball_is_moving, ball_is_displayed, ball_in_cloud, is_win, pause

    # print(is_win)
    game_easteregg.animate()
    
    if pause:
        return
    
    is_win = True
    for brick in all_bricks:
        if brick.colliderect(game_easteregg):
            is_win = False
    
    if is_win:
        return
    
    if did_we_click == True:
        if ball_is_moving:  #this way, the ball won't be constantly moving even when collide with cloud. it will iterate once
            new_x = ball.pos[0] + ball.speed[0] * ball.velocity
            new_y = ball.pos[1] + ball.speed[1] * ball.velocity
            # pas * car sinon 400 * 3 quand ball_speed = [3, -3]
            ball.pos = [new_x, new_y]
        
        if not ball_in_cloud:
            new_cloud_x = cloud.pos[0] + cloud.speed[0] * dt
            new_cloud_y = cloud.pos[1] + cloud.speed[1] * dt
            cloud.pos = [new_cloud_x, new_cloud_y]
        
    if cloud.right >= WIDTH:
        invert_horizontal_speed(cloud)
    if cloud.left <= 0:
        invert_horizontal_speed(cloud)
    if cloud.top <= 210:
        invert_vertical_speed(cloud)
    if cloud.bottom >= player.top-30:
        invert_vertical_speed(cloud)


    if ball.right >= WIDTH:
        invert_horizontal_speed(ball)
    if ball.left <= 0:
        invert_horizontal_speed(ball)
    if ball.top <= 0:
        invert_vertical_speed(ball)

    if ball.colliderect(player):
        invert_vertical_speed(ball)

    for brick in all_bricks:
        if ball.colliderect(brick):
            all_bricks.remove(brick)
            if brick in speed_bricks:
                speed_bricks.remove(brick)
                if ball.speed[0] > 0 and ball.speed[1] > 0:
                    ball.speed[0] += 0.5
                    ball.speed[1] += 0.5
                else:
                    ball.speed[0] -= 0.5
                    ball.speed[1] -= 0.5    
            score = score + 100
            invert_vertical_speed(ball)

    if not ball_in_cloud and ball.colliderect(cloud):
        saved_cloud_pos = cloud.pos
        ball_is_displayed = False
        ball_in_cloud = True
        ball_trajectory_recalc()
        clock.schedule(cloud_move_around, 0.25) #0.25 #1/60 si on veut qu'il shake qu'une fois
        clock.schedule(setback_cloud_pos, 0.7)

    if ball_in_cloud and not ball.colliderect(cloud):
        ball_in_cloud = False
    
    if ball.bottom > HEIGHT:
        music.fadeout(2)
        music.play_once('angel_eyes')
        return
 


def update(dt):
    global score, saved_cloud_pos, ball_is_moving, ball_is_displayed

    if menu_visible == True:
        update_menu()
    else:
        update_game(dt)

    
def draw():
    global menu_visible
    if menu_visible == True:
        draw_menu()
    
    else:
        draw_game()

def draw_menu():
    screen.clear()
    menu_bg.draw()
    menu_img.draw()

    screen.draw.text(f"ESC : Exit Fullscreen\nEnter : Start game\nPause : Spacebar",
                     (10, 15), color="sandybrown", shadow=(1,2), scolor="sienna", fontsize=16, fontname="bookosbi")
    
    screen.draw.text("Press enter to start", center=(WIDTH/2, HEIGHT/2+200), color="sandybrown", owidth=0.25, ocolor="sienna", fontsize=37, fontname="bookos")


def draw_game():
    global all_bricks, brick_file, brick_height, brick_width, brick_names, ball_is_displayed, is_win

    screen.clear()
    game_bg.draw()    
    game_easteregg.draw()
    
    for brick in all_bricks:
        brick.draw()

    player.draw()

    if ball_is_displayed == True:
        ball.draw()

    cloud.draw()
    

    screen.draw.text(str(score), (25, 230),
                        color=(255, 255, 255), gcolor="lightseagreen", fontsize=45)
    

    if ball.bottom > HEIGHT+10:
        screen.clear()
        screen.draw.text("Sadly, you lost...\n\nThe castle in the sky might never be discovered ...", center=[WIDTH/2, HEIGHT/2], color="firebrick",
                         gcolor="papayawhip", owidth=0.25, ocolor="peachpuff", fontsize=35, fontname="mtcorsva")
        game_over_img.draw() 
                
    if is_win:
        win_wind_fx.draw()
        screen.draw.text("Magnificent !\nYou discovered...\nTHE legendary Castle in the Sky", center=[WIDTH/2, HEIGHT/2], color="powderblue", gcolor="lightskyblue",
                         owidth=0.25, ocolor="lightcyan", fontsize=35, fontname="mtcorsva")


# ---------------------Def Fonctions------------------------


def on_mouse_move(pos):  # pos -> mouse position
    # player.x = pos[0] mouse can only move on vertical axis and y axis stays at player.pos[1]
    player.pos = [pos[0], player.pos[1]]
    if player.right >= WIDTH:
        player.x = WIDTH - 75   # not player.pos[0] because it's a tuple
    if player.left <= 0:
        player.x = 75

def on_mouse_down(pos, button):
    global did_we_click, ball_is_moving
    if button == mouse.LEFT and not did_we_click:   #same as #did_we_click == False
        did_we_click = True
        ball_is_moving = True

def on_key_down(key):
    global menu_visible, pause
    if key == keys.RETURN and menu_visible == True:     #RETURN = Enter key
        menu_visible = False

    if key == keys.SPACE:
        pause = not pause
        
    if key == keys.ESCAPE:
        exit()

def on_music_end():
    music.queue('angel_eyes')


def invert_horizontal_speed(obj):
    obj.speed[0] = obj.speed[0] * -1

def invert_vertical_speed(obj):
    obj.speed[1] = obj.speed[1] * -1
    
def cloud_move_around():
    global saved_cloud_pos
    new_cloud_x = saved_cloud_pos[0] + choice(cloud_pos_ranges)   #not cloud.pos[0] but saved_cloud_pos[0]
    new_cloud_y = saved_cloud_pos[1] #+ choice(cloud_pos_ranges)
    cloud.pos = [new_cloud_x, new_cloud_y]

def setback_cloud_pos():
    global saved_cloud_pos
    clock.unschedule(cloud_move_around)
    cloud.pos = saved_cloud_pos #not the other way around, cos we want the cloud.pos to be the saved_cloud_pos

def set_ball_is_moving_true_delay():
    global ball_is_moving, ball_is_displayed
    ball_is_moving = True
    ball_is_displayed = True

def ball_trajectory_recalc():
    global ball_is_moving, cloud_speed_options
    ball_is_moving = False
    clock.schedule(set_ball_is_moving_true_delay, 1.5)
    ball.speed[0] = choice(cloud_speed_options)
    #not sure about code below, maybe randint ?
    # new_x = ball.pos[0] + ball.speed[0] * ball.velocity
    # new_y = ball.pos[1] + ball.speed[1] * ball.velocity
    # ball.pos = 


# a hidden object between bricks and background, revealed, makes the player win


# LAST LINE HERE
pgzrun.go()

import pgzrun

WIDTH = 800
HEIGHT = 600

all_bricks = []

for y in range(7):
    for x in range(8):
        brick = Actor("brick", anchor=["left", "top"])
        brick.pos = [x * 100, y * 30]
        all_bricks.append(brick)

player = Actor("player")
player.pos = [WIDTH/2, 550]

ball = Actor("ball")
ball.pos = [WIDTH/2, 500]
ball_speed = [3, -3]

def on_mouse_move(pos):
    # player.x = pos[0]
    player.pos = [pos[0], player.pos[1]]

def invert_horizontal_speed():
    ball_speed[0] = ball_speed[0] * -1

def invert_vertical_speed():
    ball_speed[1] = ball_speed[1] * -1

def update():
    new_x = ball.pos[0] + ball_speed[0]
    new_y = ball.pos[1] + ball_speed[1]
    ball.pos = [new_x, new_y]

    if ball.right > WIDTH or ball.left < 0:
        invert_horizontal_speed()
    
    if ball.top < 0:
        invert_vertical_speed()

    if ball.colliderect(player):
        invert_vertical_speed()

    for brick in all_bricks:
        if ball.colliderect(brick):
            all_bricks.remove(brick)
            invert_vertical_speed()


def draw():
    screen.clear()
    for brick in all_bricks:
        brick.draw()
    
    player.draw()
    ball.draw()
    

# DERNIERE LIGNE ONLY
pgzrun.go()

import pgzrun 
# from pygame import pgzero     when automatic switch to python 3.10

WIDTH = 920
HEIGHT = 400
center = [460, 200]

def update():
    global center
    center[0] = center[0] + 1
    

def draw():
    screen.clear()
    #screen.draw.circle(center, 50, "greenyellow")
    screen.fill((128, 50, 75))
    screen.draw.filled_circle(center, 200, "lightsalmon")
    screen.draw.filled_circle(center, 30, "palevioletred")
    screen.draw.filled_circle(center, 10, "mediumvioletred")




# DERNIERE LIGNE ONLY
pgzrun.go()

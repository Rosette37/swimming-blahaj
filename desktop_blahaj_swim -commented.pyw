import pygame
import win32api
import win32con
import win32gui
import os
from random import randint
import mouse

dir_name = os.path.dirname(__file__)

pygame.init()

#getting the size of the main monitor
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)
screen_size = (screen_width, screen_height)

screen = pygame.display.set_mode(screen_size, pygame.NOFRAME)
running = True
clock = pygame.time.Clock()
tick = 0
fuchsia = (255, 0, 128)  # Transparency color
hajsprite = pygame.image.load(dir_name + r"\sprites\sprite.png")
hajdrawnsprite = hajsprite
hajtrueposition = pygame.math.Vector2(screen_width / 2, screen_height / 2)
hajposition = pygame.math.Vector2(hajtrueposition.x, hajtrueposition.y)
hajtangle = pygame.Rect(hajposition, (44, 21))
mouseposition = pygame.math.Vector2(mouse.get_position())
targetposition = pygame.math.Vector2(screen_width / 2, screen_height / 2)
targetchange = randint(4, 12)
offtickmark = 1
hajbobintensity = 1

# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

# set window to always on top
win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #move haj towards target vector
    hajtrueposition.update(hajtrueposition.move_towards(targetposition, 1.5))

        
    #haj bobbing

    #makes a range from 0-30 when tick is 0 - 30 and from 29 - 1 when tick is 31 - 59
    if tick < 30:
        heightrange = tick
    else:
        heightrange = 60 - tick

    #the fraction that the heightrange will be multiplied by to convert the range to 0-1,
    #modified to be larger depending on hajbobintensity
    fraction = 1/(15 / hajbobintensity)

    #makes halfarc a range smaller range
    halfarc = heightrange * fraction

    #offtickmark changes between -1 and 1 every second, thereby flipping the arc each second
    positionoffset = halfarc * offtickmark
    
    hajposition.update(hajtrueposition.x, hajtrueposition.y + positionoffset)
    hajtangle.update((hajposition.x - 22, hajposition.y - 10.5), (44, 21))


    #updating mouse position
    mouseposition.update(mouse.get_position())

    #drawing the background
    screen.fill(fuchsia)  # Transparent background

    #drawing haj
    hajdrawnsprite = hajsprite
    if hajtrueposition.distance_to(targetposition) > 1:
        hajdrawnsprite = pygame.transform.flip(hajdrawnsprite, (targetposition.x < hajtrueposition.x), False)
        hajbobintensity = 3
    else:
        hajdrawnsprite = pygame.transform.flip(hajdrawnsprite, (mouseposition.x < hajtrueposition.x), False)
        hajbobintensity = 1
    screen.blit(hajdrawnsprite, hajtangle)

    pygame.display.update()
    clock.tick(60)
    #increment ticks
    tick += 1
    #reset ticks from 60 to 0
    if tick == 60:
        tick = 0
        #offtickmark changes from 1 to -1 every second
        offtickmark *= -1
        #deincrements target change timer if haj is at target
        if hajtrueposition.distance_to(targetposition) < 1:
            targetchange -= 1
        #sets new target vector
        if targetchange == 0:
            targetchange = randint(4, 12)
            targetx = 1000000
            while abs(targetx - hajtrueposition.x) > screen_width / 4:
                targetx = randint(30, screen_width - 30)
            targety = 1000000
            while abs(targety - hajtrueposition.y) > screen_height / 2:
                targety = randint(30, screen_height - 30)
            targetposition.update(targetx, targety)
            
pygame.quit()

import pygame
from pygame.locals import *
import random
from draw_text import draw_text
from menu import menu
from scores import save_score

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('El aviador')

# define font 
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images
bg = pygame.image.load('./images/bg2.png')
ground_img = pygame.image.load('./images/ground.png')
button_img = pygame.image.load('./images/button.png')

def reset_game():
    pipe_group.empty()
    aviator.rect.x = 100
    aviator.rect.y = int(screen_height / 2)
    score = 0
    return score

selected_option = menu(screen_width, screen, clock, fps, bg)

if selected_option == "scores":
    print("Aquí podrías mostrar los puntajes altos.")
    pygame.quit()
    exit()
elif selected_option == "play":
    flying = False
    game_over = False

class Plane(pygame.sprite.Sprite) :
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./images/plane.png')
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:

            #gravity
            self.vel += 0.5
            if self.vel > 8: 
                self.vel = 8

            if self.rect.bottom < 768 :
                self.rect.y += int(self.vel)

            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #rotate the plane
            self.image = pygame.transform.rotate(self.original_image, self.vel * -2)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./images/pipe.png')
        self.rect = self.image.get_rect()

        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed

        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

plane_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

aviator = Plane(100, int(screen_height / 2))
plane_group.add(aviator)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True

while run :
    clock.tick(fps)

    #draw backgorund
    screen.blit(bg, (0,0))

    plane_group.draw(screen)
    plane_group.update()
    pipe_group.draw(screen)
    
    #Draw the ground
    screen.blit(ground_img, (ground_scroll, 768))

    #check the score
    if len(pipe_group) > 0 :
        if plane_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and plane_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False :
            pass_pipe = True
        
        if pass_pipe == True:
            if plane_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
     
    draw_text(screen, str(score), font, white, int(screen_width/2), 20)

    #look for collision
    if pygame.sprite.groupcollide(plane_group, pipe_group, False, False) or aviator.rect.y < 0:
        game_over = True

    # chech if plane has hit the ground
    if aviator.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_heigh = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height/2) + pipe_heigh, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_heigh, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll the gorund 
        ground_scroll -= scroll_speed
        if abs(ground_scroll)> 35 : 
            ground_scroll = 0
        
        pipe_group.update()

    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            save_score(score) 
            menu(screen_width, screen, clock, fps, bg) 
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
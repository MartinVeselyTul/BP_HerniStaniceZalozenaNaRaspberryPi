import pygame, os, sys
from pygame.locals import *
from tkinter import *

from src.walls import Walls
from src.snake import Snake
from src.apple import *
from src.constants import *

import grove_controls

class App:
    clock = pygame.time.Clock()  # for timing and snake's speed
    
    start = False
    game_over = False
    seconds = 3  # seconds before start
    walls_list = Walls.createList(Walls(), CELL_SIZE)
    player_name = "testujem"

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # center the window
        self.screen = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.hero = Snake(image)  # the snake
        self.apple = Apple(CELL_SIZE)  # an apple
 

    def print_text(self, font, text, color, textpos=None):
        font = pygame.font.SysFont(font[0], font[1])
        text = font.render(text, 1, color)
        if textpos is None:
            textpos = text.get_rect(centerx=W/2, centery=H/2)
        self.screen.blit(text, textpos)

    
    def draw_text(self):
        text = "Apples:{} Points: {} Lives: {} ".format(self.apple.count, self.hero.points, "O " * self.hero.lives)
        #App.print_text(self, SCORE_FONT, text, TURQUOISE, (10, 10))
        App.print_text(self, SCORE_FONT, text, (240,240,240), (10, 10))

    def draw_walls(self):
        for wall in self.walls_list:
            #pygame.draw.rect(self.screen, pygame.Color("blue"), wall, 0)
            pygame.draw.rect(self.screen, pygame.Color(102,0,102), wall, 0)

        
    def countdown(self):
        global start
        
        pygame.time.wait(1000)
        #self.screen.fill(BLACK)
        self.screen.fill((40,40,40))
        #self.print_text(LARGE_FONT, "{}".format(self.seconds), BLUE)
        self.print_text(LARGE_FONT, "{}".format(self.seconds), (100,100,100))
        self.seconds -= 1
        pygame.display.flip()


    def ate_apple(self):
        head = self.hero.body[0]
        head_rect = pygame.Rect((head[0] * CELL_SIZE, head[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        return head_rect.colliderect(self.apple.rect)
        
def main():
    Application = App()
    Application.hero.draw(Application.screen)  # drawing snake
    Application.apple.draw(Application.screen)  # drawing apple
    Application.draw_walls()  # drawing walls
    Application.draw_text()  # showing walls

    while Application.seconds >= 0:
        Application.countdown()  # countdown before game start
    Application.start = True

    app_paused = False

    while True:  # main loop
        joystick = grove_controls.Joystick_controller(0)
        joystick.joystick_handle(None)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not Application.game_over:
                    Application.write_file()  # write result (name, apples, points) to the file
                    break
            elif event.type == KEYDOWN:  # if key pressed we change snake's direction
                if event.key == pygame.K_q:
                    Application.game_over = True
                if event.key == pygame.K_p:
                    app_paused = not app_paused
                if not app_paused:
                    Application.hero.set_direction(event.key)
            elif event.type == KEYUP:
                Application.hero.speed = 10

        if not app_paused:
            Application.screen.fill(BLACK)  # fill the screen black
            Application.draw_walls()  # drawing walls
            Application.draw_text()  # drawing text
            Application.hero.draw(Application.screen)  # drawing snake
            Application.apple.draw(Application.screen)  # drawing apple

            if not Application.game_over:
                Application.hero.move()  # snake's moving

                if Application.ate_apple():  # check if the apple was eaten
                    Application.hero.points += Application.apple.size  # add points to snake
                    Application.apple.set_random_xy()  # change apple position
                    Apple.count += 1  # count apples
                else:
                    Application.hero.body.pop()  # delete the ending tile of the snake

            if Application.hero.hit_walls(App.walls_list):  # check if snake hits the walls or itself
                Application.apple.set_random_xy()
                if Application.hero.lives <= 0:
                    Application.game_over = True
                    Application.print_text(LARGE_FONT, "GAME OVER", RED)

            Application.clock.tick(Application.hero.speed)  # FPS
            #clock.tick(5)  # FPS

            pygame.display.flip()  # update the screen
        
        if Application.game_over:
            pygame.time.wait(1500)
            break
        
    #zapis do databaze

    Apple.count = 0
    pygame.quit()
    pygame.display.quit()
    return Application.hero.points

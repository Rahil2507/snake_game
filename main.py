import pygame
from pygame.locals import *
import time
import random

SIZE = 40
breadth = 1000
height = 560

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/appled.jpg').convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,(breadth//40)-1)*SIZE
        self.y = random.randint(1,(height//40)-1)*SIZE



class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/block.jpg').convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]
        

    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_right(self):
        self.direction = 'right'
    def move_left(self):
        self.direction = 'left'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'up':
            self.y[0] -= SIZE            
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def out(self):
        if self.x[0] == -40 or self.x[0] == breadth or self.y[0] == -40 or self.y[0] == height:
            return True

    def cross(self):
        if self.x[0] == breadth and self.direction == 'right':
            self.x[0] = 0
        elif self.x[0] == 0 - SIZE  and self.direction == 'left':
            self.x[0] = breadth
        if self.y[0] == height  and self.direction == 'down' :
            self.y[0] = 0
        elif self.y[0] == 0 -SIZE  and self.direction == 'up':
            self.y[0] = height

class Game:
    def __init__(self):
            pygame.init()
            pygame.display.set_caption("Snake & Apple")

            pygame.mixer.init()
            self.play_background_music()

            self.surface = pygame.display.set_mode((breadth,height))
            self.snake = Snake(self.surface)
            self.snake.draw()
            self.apple = Apple(self.surface)
            self.apple.draw()
            self.speed_list = [0.5,0.25,0.225,0.2,0.175,0.15,0.125,0.1,0.075,0.05,0.03]
            self.iteration = 0
            self.speed_level = 1
            self.speed = self.speed_list[self.speed_level]

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()


    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.speed_level = 1
        self.speed = self.speed_list[self.speed_level]
        self.iteration = 0
 
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load('resources/desert.jpg')
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.apple.move()
            self.snake.increase_length()
            self.iteration += 1
            if self.speed_level < 10 and self.iteration%2 == 0:
                self.speed_level += 1
                self.speed = self.speed_list[self.speed_level]
            print(self.speed,self.iteration,self.speed_level)

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-1}",True,(255,255,255))
        self.surface.blit(score, (850,10))
        font_small = pygame.font.SysFont('arial', 20)
        level = font_small.render(f"Level: {self.speed_level}",True,(255,255,255))
        self.surface.blit(level, (920,530))


 
    def show_game_over(self):
        self.play_sound('crash')
        self.render_background()
        font = pygame.font.SysFont('arial', 25)
        line1 = font.render(f"Game over.  Your score is: {self.snake.length-1}", True, (255,255,255))
        self.surface.blit(line1,(370,200))
        line2 = font.render(f"To play again press ENTER, To exit press ESCAPE.", True, (255,255,255))
        self.surface.blit(line2,(260,300 ))
        pygame.mixer.music.pause() 
        
        pygame.display.flip()
    

    def run(self):
        running = True
        pause = True

        while running:
            # boundry out_feature
            '''
            if self.snake.out():
                pause = True
                self.show_game_over()
                self.reset()
            '''

            # boundary cross_feature
            self.snake.cross()

    

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        quit()               
                    if event.key == K_c:
                        self.cheat()
                        pause = True
                    # for inside the cheat_mode
                    if event.key == K_1:
                        self.cheat_level(1)
                        pause = False
                    if event.key == K_2:
                        self.cheat_level(2)
                        pause = False
                    if event.key == K_3:
                        self.cheat_level(3)
                        pause = False
                    if event.key == K_4:
                        self.cheat_level(4)
                        pause = False
                    if event.key == K_5:
                        self.cheat_level(5)
                        pause = False

                    if event.key == K_ESCAPE:
                        running = False   
                                  
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        if event.key == K_m:
                            self.interface()
                            self.reset()
                            pause = True
                        if event.key == K_r:
                            self.reset()
                            self.snake.move_up()
                        if event.key == K_UP and self.snake.direction != 'down':
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != 'up':
                            self.snake.move_down()
                        if event.key == K_LEFT and self.snake.direction != 'right':
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != 'left':
                            self.snake.move_right()
                    
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(self.speed)

    def interface(self):
        self.render_background()
        font = pygame.font.SysFont('times new roman', 50)
        line1 = font.render(f"Snake & Apple", True, (255,255,255))
        self.surface.blit(line1,(345,100))
        font_small = pygame.font.SysFont('arial',20)
        line2 = font_small.render(f"Press ENTER to start", True, (255,255,255))
        self.surface.blit(line2,(420,340))
        line3 = font_small.render(f"Press Q to quit", True, (255,255,255))
        self.surface.blit(line3,(445,370))
        line4 = font_small.render(f"Press C to enter CHEAT MODE", True, (255,255,255))
        self.surface.blit(line4,(380,400))
        pygame.display.flip()

    def cheat(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Enter level to advance", True, (255,255,255))
        self.surface.blit(line1,(350,150))
        line2 = font.render(f"(1-9)", True, (255,255,255))
        self.surface.blit(line2,(450,180))
        pygame.display.flip()
        
    def cheat_level(self,level):
        self.speed_level = level
        self.snake.length = level
        self.speed = self.speed_list[level]





if __name__ == '__main__':

    game = Game()
    game.interface()
    game.run()

    
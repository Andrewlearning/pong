#coding:utf-8
# pong version 3
# 2017 10. 30
# i think that the most important is how can let pong bounce
# when it touch the wall and front size of the paddles



from uagame import Window
import pygame
from pygame.locals import *
import time
import math

#在 pong move 设置小球与屏幕边缘。木板的碰撞速度变化，内边弹，外边穿
#在pong collide 里设置当小球碰到边缘时，game update里的 scoreboard +1 ，当score board =11是，xx = False


def main():
    #create window
    #make the game run
    #clean the window
    window = Window('pong', 500, 400)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.clear()


class Pong:
    # give pong different element
    def __init__(self,window,r,v,c,p):
        self.window = window
        self.r = r
        self.v = v
        self.c = pygame.Color(c)
        self.p = p


    def move(self,rect1,rect2):
        size = self.window.get_surface().get_size()
        #rect1 = pygame.Rect(self.window, 'white', [350, 50, 20, 300], 0)
        for index in range(len(self.p)):
            self.p[index] = self.p[index] + self.v[index]
            if self.p[index] > size[index] - self.r or self.p[index] -self.r < 0:
                self.v[index] = -1*self.v[index]


            #ball touch the front side of the front size
            elif rect1.rect.collidepoint(self.p[0],self.p[1]) and self.v[0] < 0:
                self.v[index] = -1 * self.v[index]
            elif rect2.rect.collidepoint(self.p[0], self.p[1]) and self.v[0] > 0:
                self.v[index] = -1 * self.v[index]
                #注意不能直接用pygame.Rect.coillidepoint(),要先定义一个identifier = pygame.Rect()才能使用


    # it is the method about the score
    # 不能直接Game.score1 = ... 要先在原函数的别的地方，先identifier先才
    def touch_edge(self,game):
        size = self.window.get_surface().get_size()
        if self.p[0] > size[0] - self.r:
            game.score1 = game.score1 + 1
        elif self.p[0] -self.r < 0:
            game.score2 = game.score2 + 1
                #Game.score2 = Game.score2 + 1
        if game.score1 > 10 or game.score2 > 10:
            game.continue_game = False

    #draw the pong
    def draw(self):
        pygame.draw.circle(self.window.get_surface(),self.c , self.p , self.r )



class Rect:
    # set all the data about the rect
    def __init__(self, window , c , p):
        self.window = window
        self.c = pygame.Color(c)
        #self.p = p
        self.rect = pygame.Rect(p[0], p[1], p[2], p[3])

        #self.rect.move_ip(p[2],p[3])

    def draw(self):
        pygame.draw.rect(self.window.get_surface(), self.c , self.rect)




class Game:
    def __init__(self,window):
       #其实也只是用来放各个物体的参数
       #px,py
       self.window = window
       size = self.window.get_surface().get_size()
       x1 = 0.25 * size[0] - 5
       x2 = 0.75 * size[0] - 5
       y1 = 0.5 * size[1] - 20
       y2 = 0.5 * size[1] - 20
      # px = int(0.5 *size[0])
      # py = int(0.5 *size[1])
       self.pause_time = 0.01
       self.close_clicked = False  # 在line79作为游戏update循环的判断标志，在line95可以停止游戏循环
       self.continue_game = True  # 在83作为游戏update判断标志
       self.pong = Pong(self.window, 10, [10l, 5], 'white', [50, 50])
       self.rect1 = Rect(self.window, 'white', [x1, y1 ,10, 50])
       self.rect2 = Rect(self.window, 'white', [x2, y2 ,10, 50])
       # 第一个参数x,第二个参数y,第三个参数宽，第四个参数高
       self.score1 = 0
       self.score2 = 0
       self.score_size = 64

    # the most important part of the game
    def play(self):
        while not self.close_clicked:
            #play frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time)


    # button contral center, get all the user behaviors
    def handle_event(self):

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True

        #make the paddle can move #????rect
        keys_currently_pressed = pygame.key.get_pressed()
        if keys_currently_pressed[K_q] and self.rect1.rect[1] > 0 and self.continue_game:
            self.rect1.rect.move_ip(0 ,-10)
        if pygame.key.get_pressed()[K_a] and self.rect1.rect[1] < 350 and self.continue_game:
            self.rect1.rect.move_ip(0 , 10)

        if keys_currently_pressed[K_p] and self.rect2.rect[1] > 0 and self.continue_game:
            self.rect2.rect.move_ip(0 ,-10)
        if pygame.key.get_pressed()[K_l] and self.rect2.rect[1] < 350 and self.continue_game:
            self.rect2.rect.move_ip(0 , 10)



    #make the pong's data can be update
    def update(self):
        self.pong.move(self.rect1,self.rect2)
        self.pong.touch_edge(self) #不用打Game,因为self jiushi Game)


    # draw all the objects about the game can be move
    def draw(self):
        self.window.clear()
        size = self.window.get_surface().get_size()
        #不同CLASS做前缀，引用的函数都是自身class里定义的函数。
        self.pong.draw()
        self.rect1.draw()
        self.rect2.draw()
        self.window.set_font_size(self.score_size)
        self.window.draw_string(str(self.score1) , 0, 0 )
        self.window.draw_string(str(self.score2) , 450, 0 )
        self.window.update()

    def decide_continue(self):
        pass

main()
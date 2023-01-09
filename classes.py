import pygame
import random
from constants import *


class Paddle() :
    def __init__(self, pos, size, color) :
        self.pos = pos
        self.size = size
        self.color = color

        self.speed = PADDLE_SPEED

        self.state = "Stop" # states are Up, Down, Stop


    def update(self, dt) :
        # update position from current state
        if self.state == "Up" :
            self.pos.y -= self.speed * dt
        elif self.state == "Down" :
            self.pos.y += self.speed * dt

        # check boundaries
        if self.pos.y < 0 :
            self.pos.y = 0
        if self.pos.y + self.size.y > HEIGHT :
            self.pos.y = HEIGHT - self.size.y


    def draw(self, window) :
        pygame.draw.rect(
            window, 
            self.color, 
            pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y), 
            0
        )


class Ball() :
    def __init__(self, pos, size, color) :
        self.pos = pos
        self.size = size
        self.color = color

        self.speed = BALL_SPEED

        self.direction = self.getRandomDirection()


    def update(self, paddle, dt) :
        # update position
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

        # check boundaries
        # x
        if self.isOutsideBoundaryMax(self.pos.x + self.size.x, WIDTH) :
            self.pos.x = WIDTH - self.size.y
            self.direction.x = -self.direction.x

        # y
        if self.isOutsideBoundaryMin(self.pos.y) : 
            self.pos.y = 0
            self.direction.y = -self.direction.y

        if self.isOutsideBoundaryMax(self.pos.y + self.size.y, HEIGHT) :
            self.pos.y = HEIGHT - self.size.y
            self.direction.y = -self.direction.y

        # paddle  
        if (self.pos.x <= paddle.pos.x + paddle.size.x and self.pos.x > paddle.pos.x and
            self.isYAlignedWithPaddle(paddle)) :
            self.pos.x = paddle.pos.x + paddle.size.x
            self.direction.x = -self.direction.x


    def isXAlignedWithPaddle(self, paddle):
        if (self.pos.x <= paddle.pos.x + paddle.size.x and
            self.pos.x + self.size.y > paddle.pos.x ) :
            return True
        else : 
            return False


    def isYAlignedWithPaddle(self, paddle):
        if (self.pos.y + self.size.y >= paddle.pos.y and
            self.pos.y < paddle.pos.y + paddle.size.y) :
            return True
        else :
            return False


    def isOutsideBoundaryMin(self, coordinate) :
        if coordinate < 0 :
            return True
        else :
            return False


    def isOutsideBoundaryMax(self, coordinate, screen_size_coordinate) :
        if coordinate > screen_size_coordinate :
            return True
        else :
            return False

    def getRandomDirection(self) :
        goes_right = random.getrandbits(1);
        goes_up = random.getrandbits(1);
        
        x_options = [1, -1]
        y_options = [1, -1]

        return pygame.Vector2(x_options[goes_right], y_options[goes_up])


    def draw(self, window) :
        pygame.draw.rect(
            window,
            self.color,
            pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y),
            0
        )
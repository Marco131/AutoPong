import pygame as pg


# engine constants
SCREEN = WIDTH, HEIGHT = (1600, 900)
COLORS = {
    "white": (255, 255, 255),
    "black": (21, 21, 21),
    "gray": (100, 100, 100)
}


# game constants
TIMESTEP = 250
NB_RANDOM_RUNS = 20

PADDLE_SPEED = 500
PADDLE_INITIAL_POS = pg.Vector2(100, 375)
PADDLE_SIZE = pg.Vector2(15, 150)

BALL_SPEED = 700
BALL_INITIAL_POS = pg.Vector2(790, 440)
BALL_SIZE = pg.Vector2(20, 20)

MAX_BALL_PADDLE_DISTANCE = HEIGHT - PADDLE_SIZE.y/2 - BALL_SIZE.y/2

K = 10
TEXT_MARGIN = 10

GRAPH_LABELS = {'x': 'Runs', 'y': 'Success pourcentage'}


# learner constants
DEFAULT_REWARD = 0.5
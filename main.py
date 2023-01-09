import pygame as pg
import plotly.express as px
import math
import random
import numpy as np

from constants import *
from classes import Paddle, Ball
from learner import Agent, State, Policy


# Initialization
pg.init()
window = pg.display.set_mode(SCREEN, pg.NOFRAME)

font = pg.font.Font("content\coolvetica_rg.ttf", 30)
clock = pg.time.Clock()

# game objects
paddle = Paddle(PADDLE_INITIAL_POS, PADDLE_SIZE, COLORS["white"])
ball = Ball(BALL_INITIAL_POS, BALL_SIZE, COLORS["white"])

# learner objects
agent = Agent()


# Functions
def resetEnvironment() :
    paddle.pos = pg.Vector2(100, 375)
    paddle.state = "State"

    ball.pos = pg.Vector2(790, 440)
    ball.direction = ball.getRandomDirection()

    return False;


def VerticalDistanceBallPaddle() :
    paddle_center_y = paddle.pos.y + paddle.size.y / 2
    ball_center_y = ball.pos.y + ball.size.y / 2

    distance = abs(paddle_center_y - ball_center_y)

    return distance


# Variables
is_running = True
time_counter = 0
rnd_runs_cpt = 0
learner_actions_state = ""

runs_cpt = 0
paddle_hits = []
success_percentage = 0;
graph_values = []

has_updated = False
has_failed_run = False

past_states = []


# Game loop
while is_running :
    dt = clock.tick(60)
    time_counter += dt

    window.fill(COLORS["black"])

    # Events
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            is_running = False

        if event.type == pg.KEYDOWN :
            if event.key == pg.K_ESCAPE :
                is_running = False


    if time_counter >= TIMESTEP :
        # take random action
        if runs_cpt < NB_RANDOM_RUNS :
            rndInt = random.randint(0, 2)
            if rndInt == 0 :
                paddle.state = "Up"
            elif rndInt == 1 :
                paddle.state = "Down"   
            else :
                paddle.state = "Stop"

            learner_actions_state = "Random"
        else : # take chosen action
            nextMovement = ball.direction * BALL_SPEED * dt/1000
            paddle.state = agent.takeAction(State(paddle.pos.y, ball.pos + nextMovement, ball.direction)) # next ball pos
            learner_actions_state = "Chosen"

        past_states.append(State(paddle.pos.y, pg.Vector2(ball.pos), pg.Vector2(ball.direction)))

        time_counter = 0


    # if true update states
    if ball.isXAlignedWithPaddle(paddle) and has_failed_run == False :
        verticalDistance = VerticalDistanceBallPaddle()
        signal = 1 - verticalDistance / MAX_BALL_PADDLE_DISTANCE
        if ball.isYAlignedWithPaddle(paddle) :
            reward_signal = 1 - 0.5 * (verticalDistance / (PADDLE_SIZE.y/2))
            agent.policy.updateStates(past_states, reward_signal)
            paddle_hits.append(1)
        else :
            reward_signal = 0.5 - 0.5 * (verticalDistance / MAX_BALL_PADDLE_DISTANCE)
            agent.policy.updateStates(past_states, reward_signal)
            has_failed_run = True
            paddle_hits.append(0)
        
        past_states = []

        runs_cpt += 1
        graph_values.append(success_percentage)

    # if the ball goes outide the screen to the left, reset the game
    if ball.isOutsideBoundaryMin(ball.pos.x) :
        has_failed_run = resetEnvironment()

    # Text
    learner_state_txt = font.render("Actions : " + learner_actions_state, True, COLORS["gray"]);
    if runs_cpt > 0:
        divider = K
        if len(paddle_hits) >= 10 :
            K = len(paddle_hits)

        success_percentage = round(sum(paddle_hits[-K:]) / K * 100)
    else :
        success_percentage = 0

    success_percentage_txt = font.render("Last 10 : " + str(success_percentage) + "%", True, COLORS["gray"])
    
    window.blit(learner_state_txt, 
        (WIDTH - learner_state_txt.get_width() - TEXT_MARGIN, 0)
    )
    window.blit(success_percentage_txt,
        (WIDTH - success_percentage_txt.get_width() - TEXT_MARGIN,
        learner_state_txt.get_height() + TEXT_MARGIN)
    )

    # Update
    paddle.update(dt/1000)
    ball.update(paddle, dt/1000)

    # Draw
    paddle.draw(window)
    ball.draw(window)

    pg.display.update()


pg.quit()

# draw graph    
fig = px.line(x=list(range(1, len(graph_values) + 1)), y=graph_values, labels=GRAPH_LABELS)
fig.write_html("fig.html", auto_open=True)
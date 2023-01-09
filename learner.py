import pygame
import math
import random
from constants import *
# todo add comments

# reward signal: 
#   good -> ball rebounds on the paddle [0.5 - 1]
#   bad -> ball is past paddle to the left [0 - 0.5[


class Agent:
    def __init__(self) :
        self.actions = ["Up", "Down", "Stop"]
        self.policy = Policy()


    # take action
    # for the current state take account of the next pos of the ball
    def takeAction(self, currentState) :
        # try all possible future states currentState, the chose the one that as the most reward
        rewards = self.tryNextStates(currentState)

        # find best reward
        if len(rewards) > 0 :
            best_rewarded_action = "Stop" # default
            rewards_list = list(rewards)[1:]
            for key in rewards_list :
                if rewards[key] > rewards[best_rewarded_action] :
                    best_rewarded_action = key

            if rewards[best_rewarded_action] > 0:
                return best_rewarded_action
            else:
                return self.getRandomAction()
        else : 
            return False


    def tryNextStates(self, currentState) :
        rewards = {}
        future_state = State(currentState.paddle_y, currentState.ball_pos, currentState.ball_direction)

        # try stop
        rewards["Stop"] = self.tryFutureState(future_state)

        # try up
        future_state.paddle_y -= 0.5 * PADDLE_SPEED
        rewards["Up"] = self.tryFutureState(future_state)

        # try down
        future_state.paddle_y = currentState.paddle_y
        future_state.paddle_y += 0.5 * PADDLE_SPEED
        rewards["Down"] = self.tryFutureState(future_state)

        return rewards


    def tryFutureState(self, future_state) :
        closest_state = self.policy.findClosestState(future_state)
        if(type(closest_state) != bool) :
            return closest_state.reward
        else : 
            return 0

    def getRandomAction(self) :
        rndInt = random.randint(0, 2)
        return self.actions[rndInt]


class State :
    def __init__(self, paddle_y, ball_pos, ball_direction):
        self.paddle_y = paddle_y
        self.ball_pos = ball_pos
        self.reward = 0 # between 0 and 1
        self.ball_direction = ball_direction
    
    def __eq__(self, other) :
        return (self.paddle_y == other.paddle_y 
            and self.ball_pos == other.ball_pos 
            and self.ball_direction.x == other.ball_direction.x
            and self.ball_direction.y == other.ball_direction.y)

    # more the importance is high, less the new reward affects the previous one
    def updateReward(self, new_reward, reward_importance) :
        self.reward = (self.reward * reward_importance + new_reward) / (reward_importance + 1)

    def roundToTen(self) :
        self.paddle_y = round(self.paddle_y, -1)
        ball_x = round(self.ball_pos.x, -1)
        ball_y = round(self.ball_pos.y, -1)

        self.ball_pos = pg.Vector2(ball_x, ball_y)

    def difference(self, state) :
        difference = abs(self.paddle_y - state.paddle_y)

        ball_x_diff = self.ball_pos.x - state.ball_pos.x
        ball_y_diff = self.ball_pos.y - state.ball_pos.y
        difference += math.sqrt(math.pow(ball_x_diff, 2) + math.pow(ball_y_diff, 2))

        return difference



class Policy:
    def __init__(self) :
        self.past_states = []


    # states order starts from the moment the paddle is hit, then the states before 
    # reward signal nb between 0 and 1
    def updateStates(self, states, reward_signal) :
        cpt = 1
        # for each state passed by parameter
        for state in states : 
            state.roundToTen()

            # check if already exists in list
            for past_state in self.past_states :    
                if past_state == state :
                    # if it does update reward
                    past_state.updateReward(reward_signal, cpt)
                    break
            else :
                # if not add it
                state.reward = DEFAULT_REWARD
                self.past_states.append(state)
                state.updateReward(reward_signal, cpt)

            cpt += 1


    # future improvement take account of multiple states 
    def findClosestState(self, state) :
        # select only same direction
        same_direction_past_state = [
            past_state for past_state in self.past_states
            if past_state.ball_direction.x == state.ball_direction.x and past_state.ball_direction.y == state.ball_direction.y
        ]

        if len(same_direction_past_state) != 0 :
            closest_state = same_direction_past_state[0]
            closest_state_diff = closest_state.difference(state)

            for past_state in same_direction_past_state[1:] :
                past_state_diff = past_state.difference(state)
                if past_state_diff < closest_state_diff:
                    closest_state = past_state
                    closest_state_diff = past_state_diff
            
            return closest_state
        
        return False
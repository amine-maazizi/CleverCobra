import torch
import random
import numpy as np
from collections import deque

from utils import *


from game import Game
from model import Linear_QNet, QTrainer
from plot import plot




class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # controls randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft() if exceeds max_memory
        self.model = Linear_QNet(8, 256, 3)  
        self.trainer = QTrainer(self.model, alpha=ALPHA, gamma=self.gamma)
    
    def get_state(self, game):
        snake = game.snake
        x, y = snake.body[0].rect.topleft
        xa, ya = game.apple.rect.topleft
        
        dir_l = (snake.dirname == Direction.LEFT)
        dir_r = (snake.dirname == Direction.RIGHT)
        dir_u = (snake.dirname == Direction.UP)
        dir_d = (snake.dirname == Direction.DOWN)
        
        # len(state) == 8 
        state = [
            # Mpve direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location
            xa < x,  # food is left
            xa > x,  # food is right
            ya < y,  # food is up
            ya > y,  # food is down
        ]

        return np.array(state, dtype= int)  # to convert bools to int

    def remeber(self, state, action, reward, next_state, gameover):
        self.memory.append(
            (state, action, reward, next_state, gameover)
        )

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            batch_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            batch_sample = self.memory
        states, actions, rewards, next_states, gameovers = zip(*batch_sample)
        self.trainer.train_step(states, actions, rewards, next_states, gameovers)

    def train_short_memory(self, state, action, reward, next_state, gameover):
        self.trainer.train_step(state, action, reward, next_state, gameover)

    def get_action(self, state):
        # Tradeoff exploration/exploitation (random move)
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if (random.randint(0, 200) < self.epsilon):
            idx = random.randint(0, 2)
            final_move[idx] = 1
        else:
            state_0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_0)
            idx = torch.argmax(prediction).item()
            final_move[idx] = 1
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []  # average scores
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    
    while True:
        # get old state
        old_state = agent.get_state(game)
        
        # get move
        final_move = agent.get_action(old_state)
        
        # perform move and get new state
        reward, gameover, score = game.play_step(final_move)
        new_state = agent.get_state(game)
        
        # train short memory
        agent.train_short_memory(old_state, final_move, reward, new_state, gameover)
        
        # remeber
        agent.remeber(old_state, final_move, reward, new_state, gameover)
        
        if gameover:
            # train long memory (replay memory) + plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                agent.model.save()
            
            print(f'Game: {agent.n_games}, Score: {score}, Record: {record}')
            game.gui.set_gen(agent.n_games)
            game.gui.set_score(score)
            game.gui.set_record(record)
            
            plot_scores.append(score)
            total_score += score
            plot_mean_scores.append(total_score / agent.n_games)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
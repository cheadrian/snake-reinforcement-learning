import pygame, sys, time, random, gymnasium
from gymnasium import Env, spaces
from gymnasium.spaces import Box
import numpy as np
import cv2
import os

class Snake(Env):
    def __init__(self, env_config):
        super(Snake, self).__init__()
        self.id = random.randint(0, 999999)
        
        # Experiment 1 / 2 / 3 / 4
        #self.observation_shape = (84, 84, 3)
        # Experiment 5
        # self.observation_shape = (42, 42, 3)
        # Experiment 6
        self.observation_shape = (10, 10, 3)
        self.observation_space = spaces.Box(low = 0, 
                                            high = 255,
                                            shape = self.observation_shape,
                                            dtype = np.uint8)
    
        self.action_space = spaces.Discrete(5,)
        os.environ["SDL_VIDEODRIVER"] = "dummy" # might be removed

        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        else:
            print('[+] Game successfully initialised')
        
        self.frame_size_x = 400
        self.frame_size_y = 400
        
        # Game variables
        self.box_size = 40 #40x40 
        self.snake_pos_h = 5 * self.box_size
        self.border = 3
        self.score = 0
                
        self.canvas_pg = pygame.Color(0, 0, 0)
        bug_1_pg = pygame.Color(30, 30, 255)
        bug_2_pg = pygame.Color(245, 30, 30)
        bug_3_pg = pygame.Color(37, 145, 229)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.snake_yellow = pygame.Color(255, 255, 70)
        
        self.bugs_arr = [bug_1_pg, bug_2_pg, bug_3_pg]
        
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y), flags=pygame.HIDDEN)
        
        self.grid_x, self.grid_y = self.frame_size_x//self.box_size, self.frame_size_y//self.box_size
       
        self.food_pos = [random.randrange(1, self.grid_x) * self.box_size, random.randrange(1, self.grid_y) * self.box_size]
        self.food_spawn = True
        self.random_bug = self.bugs_arr[random.randrange(0,len(self.bugs_arr))]
        
    def show_score(self, color, size):
        score_font = pygame.font.Font(pygame.font.get_default_font(), size)
        score_surface = score_font.render(str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x/self.box_size-8, 10)
        self.game_window.blit(score_surface, score_rect)
    
    def do_action(self, change_to):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 3 and self.direction != 'DOWN':
            self.direction = 'UP'
        if change_to == 2 and self.direction != 'UP':
            self.direction = 'DOWN'
        if change_to == 1 and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if change_to == 0 and self.direction != 'LEFT':
            self.direction = 'RIGHT'
    
        # Moving the snake
        if self.direction == 'UP':
            self.snake_pos[1] -= self.box_size
        if self.direction == 'DOWN':
            self.snake_pos[1] += self.box_size
        if self.direction == 'LEFT':
            self.snake_pos[0] -= self.box_size
        if self.direction == 'RIGHT':
            self.snake_pos[0] += self.box_size
    
        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            #print(self.score)
            self.food_spawn = False
        else:
            self.snake_body.pop()
               
        # Spawning food on the screen
        if not self.food_spawn:
            self.random_bug = self.bugs_arr[random.randrange(0,len(self.bugs_arr))]
            self.food_pos = [random.randrange(1, self.grid_x) * self.box_size, random.randrange(1, self.grid_y) * self.box_size]
            while self.food_pos in self.snake_body:
                f_pos_x = random.randrange(1, self.grid_x)
                f_pos_y = random.randrange(1, self.grid_y)
                self.food_pos = [f_pos_x * self.box_size,f_pos_y  * self.box_size]
    
        self.food_spawn = True
        
        # GFX
        self.game_window.fill(self.canvas_pg)
        for i,pos in enumerate(self.snake_body):
            if i == 0:
                color = self.green
            else:
                color = self.snake_yellow
            pygame.draw.rect(self.game_window, color, pygame.Rect(pos[0], pos[1], self.box_size, self.box_size))
        
        # FOOD
        pygame.draw.rect(self.game_window, self.random_bug, pygame.Rect(self.food_pos[0], self.food_pos[1], self.box_size, self.box_size))
    
        # Game Over conditions
        # Getting out of bounds
        done = False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-self.box_size:
            done = True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-self.box_size:
            done = True
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                done = True
    
        #self.show_score(self.snake_yellow, 20)
        pygame.display.update()
        view = pygame.surfarray.array3d(self.game_window)
        view = view.transpose([1, 0, 2])
        view = cv2.cvtColor(view, cv2.COLOR_BGR2RGB)
        #cv2_imshow(view)
        return view, done              
        
    def reset(self, seed=None, options=None):
        # Might need to implement the new "seed", "options" args: https://gymnasium.farama.org/api/env/#gymnasium.Env.reset
        # Reset the Snake position
        self.snake_pos = [self.box_size, self.snake_pos_h]
        self.snake_body = [[self.box_size, self.snake_pos_h], [self.box_size-self.box_size, self.snake_pos_h], [self.box_size-(2*self.box_size), self.snake_pos_h]]
        
        self.direction = 'RIGHT'
        self.change_to = 0
        
        canvas, done = self.do_action(0)
        self.score = 0
        self.last_score = 0

        obs = cv2.resize(canvas, (self.observation_shape[0], self.observation_shape[1]))
        # Might need to implement "info" dict
        return obs, {}
                   
    def step(self, action):
        assert self.action_space.contains(action), "Invalid Action"
        canvas, terminated = self.do_action(action)
        
        # Reward every step with X
        # Experiment 1 / 2 / 3 / 4
        # reward = 0.1
        # Experiment 5
        # reward = 0.001
        # Experiment 6
        reward = 0.0

        if(terminated):
            # If Snake hit the wall, decrease reward
            # Experiment 1 / 2
            # reward -= 1.1
            # Experiment 3 / 4
            # reward -= 5.1
            # Experiment 5 / 6
            reward -= 1.0
            
        if(self.score > self.last_score):
            # If score increase, add reward
            # Experiment 1 / 2 / 3 / 4
            # reward += 0.9
            # Experiment 5 / 6
            reward += 1.0
            self.last_score = self.score
        
        
        obs = cv2.resize(canvas, (self.observation_shape[0], self.observation_shape[1]))
        # Don't use premature episode ending, yet: https://gymnasium.farama.org/api/env/#gymnasium.Env.step
        truncated = False
        # Note, done is now "terminated"
        return obs, reward, terminated, truncated, {"score": self.score}
        
    def close(self):
        cv2.destroyAllWindows()
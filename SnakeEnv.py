import pygame, sys, time, random, gymnasium
from gymnasium import Env, spaces
from gymnasium.spaces import Box
import numpy as np
import cv2
import os

# You can use canvas_type_*.png from 1 to 4
canvas_path = os.path.abspath("snake_assets/canvas_type_1.png")
bug1_path = os.path.abspath("snake_assets/bug_1.png")
bug2_path = os.path.abspath("snake_assets/bug_2.png")
bug3_path = os.path.abspath("snake_assets/bug_3.png")
bug4_path = os.path.abspath("snake_assets/bug_4.png")
bug5_path = os.path.abspath("snake_assets/bug_boss.png")

class Snake(Env):
    def __init__(self, env_config):
        super(Snake, self).__init__()
        self.id = random.randint(0, 999999)
        #self.observation_shape = (168, 168, 3)
        self.observation_shape = (224, 224, 3)
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
                
        self.canvas_pg = pygame.image.load(canvas_path)
        bug_1_pg = pygame.transform.scale(pygame.image.load(bug1_path), (20, 20))
        bug_2_pg = pygame.transform.scale(pygame.image.load(bug2_path), (20, 20))
        bug_3_pg = pygame.transform.scale(pygame.image.load(bug3_path), (20, 20))
        bug_4_pg = pygame.transform.scale(pygame.image.load(bug4_path), (20, 20))
        bug_5_pg = pygame.transform.scale(pygame.image.load(bug5_path), (20, 20))
        
        self.bugs_arr = [bug_1_pg, bug_2_pg, bug_3_pg, bug_4_pg, bug_5_pg]
        
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y), flags=pygame.HIDDEN)
        
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.snake_yellow = pygame.Color(246, 211, 73)
        
        # Game variables
        self.box_size = 20 #20x20 
        self.snake_pos_h = 10 * self.box_size
        self.border = 1

        self.grid_x, self.grid_y = self.frame_size_x//self.box_size, self.frame_size_y//self.box_size
        self.food_pos = [random.randrange(1, self.grid_x) * self.box_size, random.randrange(1, self.grid_y) * self.box_size]
        
        self.food_spawn = True
        self.random_bug = self.bugs_arr[random.randrange(0,len(self.bugs_arr))]
        
        
    def show_score(self, color, size):
        score_font = pygame.font.Font(pygame.font.get_default_font(), size)
        score_surface = score_font.render(str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.grid_x - 8, 10)
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
        self.game_window.blit(self.canvas_pg, (0,0))
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.white, pygame.Rect(pos[0]-self.border, pos[1]-self.border, self.box_size+2*self.border, self.box_size+2*self.border))
            pygame.draw.rect(self.game_window, self.snake_yellow, pygame.Rect(pos[0]+self.border, pos[1]+self.border, self.box_size-2*self.border, self.box_size-2*self.border))
        
        self.game_window.blit(self.random_bug, (self.food_pos[0], self.food_pos[1]))
    
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
    
        self.show_score(self.snake_yellow, 20)
        pygame.display.update()
        view = pygame.surfarray.array3d(self.game_window)
        view = view.transpose([1, 0, 2])
        view = cv2.cvtColor(view, cv2.COLOR_BGR2RGB)
        #cv2_imshow(view)
        return view, done              
        
    def reset(self, seed=None, options=None):
        # Might need to implement the new "seed", "options" args: https://gymnasium.farama.org/api/env/#gymnasium.Env.reset
        # Reset the fuel consumed
        self.snake_pos = [60, self.snake_pos_h]
        self.snake_body = [[60, self.snake_pos_h], [60-self.box_size, self.snake_pos_h], [60-(2*self.box_size), self.snake_pos_h]]
        
        self.direction = 'RIGHT'
        self.change_to = 0
        
        self.score = 0
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
        reward = 0.0001

        if(terminated):
            # If Snake hit the wall, decrease reward
            reward -= 1.0
            
        if(self.score > self.last_score):
            # If score increase, add reward
            reward += 1.0
            self.last_score = self.score
        
        
        obs = cv2.resize(canvas, (self.observation_shape[0], self.observation_shape[1]))
        # Don't use premature episode ending, yet: https://gymnasium.farama.org/api/env/#gymnasium.Env.step
        truncated = False
        # Note, done is now "terminated"
        return obs, reward, terminated, truncated, {"score": self.score}
    
    def close(self):
        cv2.destroyAllWindows()
from SnakeEnv import Snake
import numpy as np
import os
import cv2

import ray
from ray.rllib.algorithms import ppo
from ray.air.config import RunConfig, ScalingConfig, CheckpointConfig
from ray.air.checkpoint import Checkpoint
from ray.train.rl import RLTrainer, RLCheckpoint, RLPredictor
from ray import tune, air
from ray.tune.registry import register_env
   
os.environ['RAY_DISABLE_MEMORY_MONITOR'] = '1'
ray.init(include_dashboard=False, ignore_reinit_error=True)

# Replace to your checkpoint path
checkpoint_path = "ray_checkpoints/checkpoint_000055"
USE_CHECKPOINT = True

def snake_env_creator(env_config):
    return Snake(env_config)

register_env("snake", snake_env_creator)

checkpoint = RLCheckpoint(local_path = checkpoint_path)
predictor =  RLPredictor.from_checkpoint(checkpoint=checkpoint)

env = Snake("")
rewards = []
num_episodes=10
for i in range(num_episodes):
    obs, _ = env.reset()
    reward = 0.0
    done = False
    while not done:
      action = predictor.predict(np.array([obs]))
      obs, r, done, _, _ = env.step(action[0])
      cv2.imshow("Snake", obs)
      cv2.waitKey(1)
      reward += r
    print(reward)
    rewards.append(reward)
print(rewards)
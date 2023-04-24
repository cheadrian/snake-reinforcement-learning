import numpy as np
import os
import cv2

print("1. Start non-asset, simple variant.")
print("2. Start the asset variant.")
simple = input()
checkpoint_path = ""
# Replace to your checkpoint path
if simple == "1":
    checkpoint_path = "ray_checkpoints/no_assets_10x10_experiment_6_5M_timesteps/AIRPPO_2023-04-22_11-19-24/AIRPPO_8a31a_00000_0_2023-04-22_11-19-25/checkpoint_000310"
    from SimpleSnakeEnv import Snake
else:
    checkpoint_path = "ray_checkpoints/with_assets_224x224_demo_140K_timesteps/AIRPPO_2023-04-24_18-04-08/AIRPPO_698ea_00000_0_2023-04-24_18-04-10/checkpoint_000070"
    from SnakeEnv import Snake
        
import ray
from ray.rllib.algorithms import ppo
from ray.air.config import RunConfig, ScalingConfig, CheckpointConfig
from ray.air.checkpoint import Checkpoint
from ray.train.rl import RLTrainer, RLCheckpoint, RLPredictor
from ray import tune, air
from ray.tune.registry import register_env
os.environ['RAY_DISABLE_MEMORY_MONITOR'] = '1'
ray.init(include_dashboard=False, ignore_reinit_error=True)

USE_CHECKPOINT = True

def snake_env_creator(env_config):
    return Snake(env_config)

register_env("snake", snake_env_creator)

checkpoint = RLCheckpoint(local_path = checkpoint_path)
predictor =  RLPredictor.from_checkpoint(checkpoint=checkpoint)

env = Snake("")
rewards = []
num_episodes=10
video_res = [400, 400]
for i in range(num_episodes):
    obs, _ = env.reset()
    reward = 0.0
    done = False
    while not done:
      action = predictor.predict(np.array([obs]))
      obs, r, done, _, _ = env.step(action[0])
      res_obs = cv2.resize(obs, (video_res[0], video_res[1]), 0, 0, interpolation = cv2.INTER_NEAREST)
      cv2.imshow("Snake Game RLlib", res_obs)
      cv2.waitKey(100)
      reward += r
    print(reward)
    rewards.append(reward)
print(rewards)
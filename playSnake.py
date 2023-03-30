from SnakeEnv import Snake
import cv2

env = Snake("{}")
obs, __ = env.reset()
total_reward = 0
while True:
    cv2.imshow("Snake Game", obs)
    key = cv2.waitKey(100)
    action = 4
    if(key & 0xFF == ord('d')):
        action = 0
    if(key & 0xFF == ord('a')):
        action = 1
    if(key & 0xFF == ord('s')):
        action = 2
    if(key & 0xFF == ord('w')):
        action = 3
    if(key & 0xFF == ord('r')):
        env.reset()
    if(key & 0xFF == ord('t')):
        break
    obs, reward, done, truncate, info = env.step(action)
    total_reward += reward
    if done:
        print(total_reward)
        total_reward = 0
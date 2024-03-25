import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

import csv

import os
os.environ["KERAS_BACKEND"] = "torch"

import keras
from DeepQLearning import DeepQLearning

print(f'{os.environ["KERAS_BACKEND"]}')

env = gym.make('LunarLander-v2')
#env.seed(0)
np.random.seed(0)

print('State space: ', env.observation_space)
print('Action space: ', env.action_space)

model = keras.Sequential()
model.add(keras.layers.Dense(512, activation="relu", input_dim=env.observation_space.shape[0]))
model.add(keras.layers.Dense(256, activation="relu"))
model.add(keras.layers.Dense(128, activation="relu"))
model.add(keras.layers.Dense(env.action_space.n, activation="linear"))
model.summary()
model.compile(loss=keras.losses.MeanSquaredError(), optimizer=keras.optimizers.Adam(learning_rate=1E-4))

gamma = 0.99
epsilon = 0.9
epsilon_min = 0.01
epsilon_dec = 0.99
episodes = 100
batch_size = 64
memory = deque(maxlen=10000) #talvez usar uma memoria mais curta
max_steps = 500

DQN = DeepQLearning(env, gamma, epsilon, epsilon_min, epsilon_dec, episodes, batch_size, memory, model, max_steps)
rewards = DQN.train()

import matplotlib.pyplot as plt
plt.plot(rewards)
plt.xlabel('Episodes')
plt.ylabel('# Rewards')
plt.title('# Rewards vs Episodes')
plt.savefig("results/lunar_lander_DeepQLearning.jpg")     
plt.close()

with open('results/lunar_lander_DeepQLearning_rewards.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    episode=0
    for reward in rewards:
        writer.writerow([episode,reward])
        episode+=1

model.save('data/model_cart_pole.keras')


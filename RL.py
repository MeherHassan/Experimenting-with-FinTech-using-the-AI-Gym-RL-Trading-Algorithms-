# -*- coding: utf-8 -*-
"""Reinforcement_Learning_GME_Trading_Tutorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XHNz7v7auYITjgNwSWzrKjQOA89jCCNA

# 0. Install and Import dependencies
"""

!pip install tensorflow==1.15 tensorflow-gpu==1.15 stable-baselines gym-anytrading gym

import subprocess
import sys
subprocess.check_call([sys.executable, "-m",
    "pip", "install", "--user", "tensorflow==1.15.0"])

import tensorflow as tf

!pip install tensorflow-gpu==1.15

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

print(tf.__version__)

!pip --version

!python --version

!pip install numpy pandas matplotlib

# Gym stuff
import gym
import gym_anytrading

# Stable baselines - rl stuff
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C

# Processing libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

"""# 1. Bring in Marketwatch GME Data 
https://www.marketwatch.com/investing/stock/gme/download-data?startDate=11/1/2019&endDate=03/12/2021
"""



df = pd.read_csv('/content/drive/MyDrive/AI/data/gmedata.csv')

from google.colab import drive
drive.mount('/content/drive')

df.head()

df['Date'] = pd.to_datetime(df['Date'])
df.dtypes

df.set_index('Date', inplace=True)
df.head()

env = gym.make('stocks-v0', df=df, frame_bound=(5,100), window_size=5)

env.signal_features

"""# 2. Build Environment"""

env.action_space

state = env.reset()
while True: 
    action = env.action_space.sample()
    n_state, reward, done, info = env.step(action)
    if done: 
        print("info", info)
        break
        
plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()

"""# 3. Build Environment and Train"""

env_maker = lambda: gym.make('stocks-v0', df=df, frame_bound=(5,100), window_size=5)
env = DummyVecEnv([env_maker])

model = A2C('MlpLstmPolicy', env, verbose=1) 
model.learn(total_timesteps=25000)

"""# 4. Evaluation"""

env = gym.make('stocks-v0', df=df, frame_bound=(90,110), window_size=5)
obs = env.reset()
while True: 
    obs = obs[np.newaxis, ...]
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        print("info", info)
        break

plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import ACKTR

env_maker2 = lambda: gym.make('stocks-v0', df=df, frame_bound=(5,100), window_size=5)
env = DummyVecEnv([env_maker2])

model = ACKTR('MlpLstmPolicy', env, verbose=1)
model.learn(total_timesteps=25000)

env = gym.make('stocks-v0', df=df, frame_bound=(90,110), window_size=5)
obs = env.reset()
while True: 
    obs = obs[np.newaxis, ...]
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        print("info", info)
        break

plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()
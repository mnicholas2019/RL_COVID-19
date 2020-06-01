import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

import tensorflow as tf


class DQNAgent:

	def __init__(self, state_dimensions=58, action_dimensions=15, num_layers=4, num_parameters=75):
		self.state_dimensions = state_dimensions
		self.action_dimensions = action_dimensions
		self.num_layers = num_layers
		self.num_parameters = num_parameters
		self.memory = deque() 
		self.epsilon = 0.25 # exploration rate
		self.gamma = 0.95 # discount future rewards rate
		self.learning_rate = 0.001
		self.model = self.build_model()
		#self.epsilon_min = 0.01
		#self.epsilon_decay = 0.99


	# initializes the model
	def build_model(self):
		model = Sequential()
		model.add(Dense(units=self.num_parameters, input_dim=self.state_dimensions, activation='relu'))#units is output dimension
		for i in range(self.num_layers - 2):
			model.add(Dense(units=self.num_parameters, activation='relu'))
		model.add(Dense(units=self.action_dimensions, activation='linear'))
		model.compile(loss='mse',
			optimizer=Adam(lr=self.learning_rate))
		return model


	# adds [state, action, reward, next_state, done] to memory deque
	def memorize(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))


	# with probability epsilon returns a random action. With probability
	# 1 - epsilon return the action with the minimum Q value (since our Q 
	# is cost function). An action should be [city, action]. 
	# city should be an integer 1-7 representing one of the cities.
	# action should be 1 for water station and 2 for field hospital
	def get_action(self, state):
		if np.random.rand() <= self.epsilon:
			action = 1
			return [random.randint(1,7),random.randint(1,3)]

		act_values = self.model.predict(state)

		#0-6 city = 1-7 and action 1 7-13 city = 1-7 and action 2 5 = do nothing
		index = np.argmin(act_values[0])
		if (index< 7):
			action = [index+1, 1] # city , action
		elif (index < 14):
			action = [index-6, 2]
		else:
			action = [-1, 3]
		return action  # returns action

	# trains the neural network using batch_size instances. sample randomly from memory
	def train_batch(self, state, action, reward, next_state, done, batch_size):
		minibatch = random.sample(self.memory, batch_size)
		for state, action, reward, next_state, done in minibatch:
			target = self.model.predict(state)
			if done:
				target[0][action] = reward
			else:
				# a = self.model.predict(next_state)[0]
				t = self.model.predict(next_state)[0]
				target[0][action] = reward + self.gamma * np.amax(t)
				# target[0][action] = reward + self.gamma * t[np.argmax(a)]
			self.model.fit(state, target, epochs=1, verbose=0)
		#if self.epsilon > self.epsilon_min:
		#   self.epsilon *= self.epsilon_decay
		return

	# train on specific instance
	def train_individual(self, state, action, reward, next_state, done):
		return

	def transform_state(self, state):
		states = self.flatten_state(state)
		states = np.reshape(states,(58,))
		states = np.reshape(states,(1,-1))
		return states

	def flatten_state(self, state):
		state_flatten = []
		for el in state:
		    if hasattr(el, "__iter__") and not isinstance(el, str):
		        state_flatten.extend(self.flatten_state(el))
		    else:
		        state_flatten.append(el)
		return state_flatten

	# save the model weights to 'name file path' so it can be loaded later
	def save_model(self, name):
		self.model.save_weights(name)
		return

	# load the model from name file path
	def load(self, name):
		self.model.load_weights(name)
		return


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
		self.action_memory = deque()
		self.epsilon = 0.99 # exploration rate
		self.gamma = 0.99 # discount future rewards rate
		self.learning_rate = 0.0001
		self.model = self.build_model()
		self.epsilon_min = 0.01
		self.epsilon_decay = 0.999
		self.num_cities = int((action_dimensions-1)/2)


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
		if (action[1] == 3):
			self.memory.append([state, action, reward, next_state, done])
		else:
			self.action_memory.append([state, action, reward, next_state, done])

	# with probability epsilon returns a random action. With probability
	# 1 - epsilon return the action with the minimum Q value (since our Q 
	# is cost function). An action should be [city, action]. 
	# city should be an integer 1-7 representing one of the cities.
	# action should be 1 for water station and 2 for field hospital
	def get_action(self, state, water_stations, field_hospitals, epsilon_enable = True):
		if np.random.rand() <= self.epsilon and epsilon_enable:
			city = random.randint(1,self.num_cities)
			action = 3
			if (water_stations > 0 and field_hospitals > 0):
				action = random.randint(1,3)
			elif (water_stations > 0):
				action = random.choice([1, 3])
			elif (field_hospitals > 0):
				action = random.randint(2,3)

			if action == 3:
				city = -1
			return [city, action]


		act_values = self.model.predict(state)
		print("Prediction: ", act_values[0])

		#Index 0-6: city 1-7 and action 1
		#index 7-13: city 1-7 and action 2 
		# index = 14 = do nothing
		index = np.argmin(act_values[0])
		# first action
		if (index< self.num_cities):
			if (water_stations > 0):
				action = [index+1, 1] # city , action
			else:
				index = np.argmin(act_values[0][self.num_cities:]) + self.num_cities
				if (index < 2*self.num_cities):
					if field_hospitals > 0:
						action = [index-self.num_cities+1, 2]
					else:
						action = [-1,3]
				else:
					action = [-1,3]

		elif (index < 2*self.num_cities):
			if (field_hospitals > 0):
				action = [index-self.num_cities+1, 2]
			else:
				index = np.argmin(act_values[0][0:self.num_cities])
				if act_values[0][index] < act_values[0][2*self.num_cities] and water_stations > 0:
					action = [index+1, 1]
				else:
					action = [-1,3]
		else:
			action = [-1, 3]
		return action  # returns action

	# trains the neural network using batch_size instances. sample randomly from memory
	def train_batch(self, batch_size, future_reward = False):
		# sample actions and no actions from memory
		if (batch_size > len(self.memory)):
			batch_size = len(self.memory)
		minibatch = random.sample(self.memory, batch_size)
		minibatch2 = []
		for x in range(batch_size):
			minibatch.append(random.sample(self.action_memory, 1)[0])


		# train each instance from minibatch
		for state, action, reward, next_state, done in minibatch:
			self.train_individual(state, action, reward, next_state, done, future_reward)
		if self.epsilon >= self.epsilon_min:
			self.epsilon*=self.epsilon_decay
		return

	def action_to_index(self, action):
		if action[1] == 3:
			action_index = 2*self.num_cities
		else:
			action_index = action[1]*(self.num_cities) - 1-self.num_cities + action[0]
		return action_index

	# train on specific instance
	def train_individual(self, state, action, reward, next_state, done, future_reward = False):
		# convert action to index
		action_index = self.action_to_index(action)

		target = self.model.predict(state)
		print("index of action:", action_index)
		print("Target before: ", target[0][action_index])
		if done:
			target[0][action_index] = reward
		else:
			t = self.model.predict(next_state)[0]
			next_action = self.get_action(next_state, next_state[0][-2], next_state[0][-1], epsilon_enable = False)
			next_action_index = self.action_to_index(next_action)
			### this is wrong. need to call get action
			if future_reward:
				target[0][action_index] = reward + self.gamma * t[next_action_index]
			else:
				target[0][action_index] = reward # delete this line later
		
		print("target after", target[0][action_index])
		self.model.fit(state, target, epochs=1, verbose=0)
		target = self.model.predict(state)
		print("After training: ", target[0][action_index])
		return

	def transform_state(self, state):
		states = self.flatten_state(state)
		states = np.reshape(states,(self.state_dimensions,))
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


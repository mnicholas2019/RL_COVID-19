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
		self.epsilon = 0.25 # exploration rate
		self.gamma = 0.95 # discount future rewards rate
		self.learning_rate = 0.001
		self.model = self.build_model()
		self.num_cities = int((state_dimensions-2)/8)
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
		if (action[1] == 3):
			self.memory.append([state, action, reward, next_state, done])
		else:
			self.action_memory.append([state, action, reward, next_state, done])

	# with probability epsilon returns a random action. With probability
	# 1 - epsilon return the action with the minimum Q value (since our Q 
	# is cost function). An action should be [city, action]. 
	# city should be an integer 1-7 representing one of the cities.
	# action should be 1 for water station and 2 for field hospital
	def get_action(self, state, water_stations, field_hospitals):
		if np.random.rand() <= self.epsilon:
			if (water_stations > 0 and field_hospitals > 0):
				return [random.randint(1,self.num_cities),random.randint(1,3)]
			elif (water_stations > 0):
				action = random.randint(1,2)
				if action == 1:
					return[random.randint(1,self.num_cities), 1]
			elif (water_stations > 0):
				return[random.randint(1,self.num_cities), random.randint(2,3)]
			else:
				return[-1, 3]

		act_values = self.model.predict(state)

		#Index 0-6: city 1-7 and action 1
		#index 7-13: city 1-7 and action 2 
		# index = 14 = do nothing
		index = np.argmin(act_values[0])
		
		# first action
		if (index< self.num_cities):#7):
			if (water_stations > 0):
				action = [index+1, 1] # city , action
			else:
				#print(act_values[0][self.num_cities:])
				index = np.argmin(act_values[0][self.num_cities:]) + self.num_cities
				#print(index)
				if (index < 2*self.num_cities):
					if field_hospitals > 0:
						action = [index-self.num_cities-1, 2]
					else:
						action = [-1,3]
				else:
					action = [-1,3]

		elif (index < 2*self.num_cities):
			if (field_hospitals > 0):
				action = [index-self.num_cities-1, 2]
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
	def train_batch(self, most_recent, batch_size):
		# sample actions and no actions from memory
		if (batch_size > len(self.memory)):
			batch_size = len(self.memory)
		minibatch = random.sample(self.memory, batch_size)
		if (batch_size > len(self.action_memory)):
			batch_size = len(self.action_memory)
		minibatch2 = random.sample(self.memory, batch_size)
		minibatch = minibatch + minibatch2
		minibatch.append(most_recent)

		# train each instance from minibatch
		for state, action, reward, next_state, done in minibatch:
			self.train_individual(state, action, reward, next_state, done)
		return

	# train on specific instance
	def train_individual(self, state, action, reward, next_state, done):
		target = self.model.predict(state)
		if done:
			target[0][action] = reward
		else:
			t = self.model.predict(next_state)[0]
			target[0][action] = reward + self.gamma * np.amin(t)
			#print("Q:",target[0][action])
		self.model.fit(state, target, epochs=1, verbose=0)
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


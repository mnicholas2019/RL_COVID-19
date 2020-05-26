from collections import deque

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


	# initializes the model
	def build_model(self):
		return

	# adds [state, action, reward, next_state, done] to memory deque
	def memorize(self, state, action, reward, next_state, done):
		return

	# with probability epsilon returns a random action. With probability
	# 1 - epsilon return the action with the minimum Q value (since our Q 
	# is cost function). An action should be [city, action]. 
	# city should be an integer 1-7 representing one of the cities.
	# action should be 1 for water station and 2 for field hospital
	def get_action(self, state)
		return

	# trains the neural network using batch_size instances. sample randomly from memory
	def train_batch(self, state, action, reward, next_state, done, batch_size):
		return

	# train on specific instance
	def train_individual(self, state, action, reward, next_state, done):
		return

	# save the model weights to 'name file path' so it can be loaded later
	def save_model(self, name):
		return

	# load the model from name file path
	def load(self, name):
		return

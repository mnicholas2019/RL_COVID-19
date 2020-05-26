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

	def build_model(self):
		return

	def memorize(self, state, action, reward, next_state, done):
		return

	def act(self, state)
		return

	def train_batch(self, state, action, reward, next_state, done, batch_size):
		return

	def train_individual(self, state, action, reward, next_state, done):
		return

	def save_model(self, name):
		return

	def save(self, name):
		return
		
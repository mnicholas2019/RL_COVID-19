from Person import Person

class City:

	"""
	Constructs a city with the given characteristics. We assume that zero are hospitalized at first,
	zero are dead, zero recovered. 
	"""
	def __init__(self, population, area, hospital_beds, num_infected):
		self.population = population # Total population of city
		self.area = area # Area of the city
		self.hospital_beds = hospital_beds # Number of hospital beds
		self.water_stations = 0 # Water Stations deployed to area
		self.susceptible = [] # list of susceptible people to disease
		self.infected_contagious = [] # List of infected, but not hospitalized people
		self.infected_hospitalized = [] # List of hospitalized people
		self.infected_needs_bed = [] # List of infected people in need of hospital beds, but don't have access
		self.recovered = [] # List of recovered people
		self.dead = [] # List of dead people

		# create num_infected persons
		for x in range(num_infected):
			self.infected_contagious.append(Person(age = 'random age', infected = True))

		for x in range(num_infected - population):
			self.susceptible.append(Person(age = 'random age', infected = False))


	"""
	Return the curent state of the city for input into RL model
	"""
	def get_state(self):
		return

	"""
	Adds x beds to hospital capacity
	"""
	def dispatch_hospital_bed(self, num_infected):
		return

	"""
	Adds water station to city
	"""
	def add_water_station(self):
		return

	"""
	Runs the simulation for x days. Should call 'update' for each person in the city. 
	Should move persons to different list accordingly and updates instance variables
	of the city and persons. We should decide who becomes infected here.
	"""
	def update(self, days):
		return
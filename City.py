from Person import Person
from collections import deque
import math
import random

class City:

	"""
	Constructs a city with the given characteristics. We assume that zero are hospitalized at first,
	zero are dead, zero recovered. 
	"""
	def __init__(self, population, area, hospital_beds, num_infected, baseline_transmission_rate, death_rate):
		self.population = population # Total population of city
		self.area = area # Area of the city
		self.baseline_transmission_rate = transmission_rate #transmission rate of disease w/ no water stations
		self.death_rate = death_rate
		self.hospital_beds = hospital_beds # Number of hospital beds
		self.water_stations = 0 # Water Stations deployed to area
		self.susceptible = deque # list of susceptible people to disease
		self.infected_contagious = deque # List of infected, but not hospitalized people
		self.infected_hospitalized = deque # List of hospitalized people
		self.infected_needs_bed = deque # List of infected people in need of hospital beds, but don't have access
		self.recovered = deque # List of recovered people
		self.dead = deque # List of dead people



		# create num_infected persons
		for x in range(num_infected):
			self.infected_contagious.append(Person(age = 'random age', infected = True))

		for x in range(population - num_infected):
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
		"""
		Determine who from the susceptible people to infect.
		Then Infect Them. Add them to contagious
		"""
		new_infected_people = determine_infections()
		for person in new_infected_people:
			person.infect()
			self.infected_contagious.append(person)



		"""
		See which hospitalized patients or patients needing bed
		will die from disease. Kill them if so. Free the beds accordingly
		"""
		new_killed_people = determine_deaths()
		for person in new_killed_people:
			person.die()
			self.dead.append(person)


		"""
		Recover patients and add them to list. Free beds accordingly
		"""
		new_recovered_people = determine_recoveries()
		for person in new_recovered_people:
			person.recover()
			self.recovered.append(person)

		"""
		Determine who of the Infected, Contagious People will
		need a hospital bed. Place move them put them on waiting queue
		"""
		new_needs_beds = determine_hospitalization()
		for person in new_needs_beds:
			self.infected_needs_bed.append(person)


		"""
		Place those that need a bed in a bed if available
		"""
		while (len(self.infected_hospitalized) < self.hospital_beds):
			self.infected_hospitalized.append(self.infected_needs_bed.popleft())		

		"""
		Increment days infected
		"""
		increment_days_infected()


		"""
		Do nothing for recovered and dead
		"""
		return

	"""
	Determines number of people will be infected from list of Susceptible.
	Previously infected individuals come into contact with 'x' people each
	depending on the density. For each person they come into contact with,
	There is a 'y'% chance they transmit the disease, which is dependent
	upon the number of sanitation stations dispatched to area.
	The people that are going to be infected are removed from susceptible
	and returned in a list
	"""
	def determine_infections(self):
		pop_density = self.population/self.area # people per sq km
		contact_ratio = 0.1 #percentage of people withink sq km you come into contact with
		num_contacts = math.ceil(pop_density * contact_ratio) # number of people an infected person comes into contact with
		tr = self.baseline_transmission_rate * (self.water_stations + 1) # current transmission rate of disease

		new_infected_people = []

		for x in range(num_contacts):
			person = self.susceptible.popleft()
			if (random.random() < tr):
				new_infected_people.append(person)
			else:
				self.susceptible.append(person)	
		return new_infected_people


	"""
	Look through list of all people who could die (hospitalized, or 
	hospitalized needs bed). Determine if they will die form disease.
	If they will be, then remove them from respective list and return them.
	If they were hospitalized, free up beds?
	"""
	def determine_deaths(self):

		new_killed_people = []

		num_hospitalized = len(self.infected_hospitalized)
		for x in range(num_hospitalized):
			person = self.infected_hospitalized.popleft()
			if (random.random() < person.death_rate):
				new_killed_people.append(person)
			else:
				self.infected_hospitalized.append(person)

		num_needs_bed = len(self.infected_needs_bed)
		for x in range(num_needs_bed):
			person = self.infected_needs_bed.popleft()
			if (random.random() < person.death_rate * 2): # This is just a placeholder. Will use better effect later
				new_killed_people.append(person)
			else:
				self.infected_needs_bed.append(person)

		return new_killed_people

	"""
	If person have been infected for >= 'x' days then they recover.
	Remove them from respective list and return them. 
	"""
	def determine_recoveries(self):
		new_recovered_people = []
		days_till_recovery = 15 # should I make this input to city? like a disease characteristics vector. placeholder for now

		num_hospitalized = len(self.infected_hospitalized)
		for x in range(num_hospitalized):
			person = self.infected_hospitalized.popleft()
			if (person.days_infected == days_till_recovery): ## should I make this input to city? like a disease characteristics vector
				new_recovered_people.append(person)
			else:
				self.infected_hospitalized.append(person)

		num_needs_bed = len(self.infected_needs_bed)
		for x in range(num_needs_bed):
			person = self.infected_needs_bed.popleft()
			if (person.days_infected == days_till_recovery): # This is just a placeholder. Will use better effect later
				new_recovered_people.append(person)
			else:
				self.infected_needs_bed.append(person)

		num_infected_contagious = len(self.infected_contagious)
		for x in range(num_needs_bed):
			person = self.infected_contagious.popleft()
			if (person.days_infected == days_till_recovery): # This is just a placeholder. Will use better effect later
				new_recovered_people.append(person)
			else:
				self.infected_contagious.append(person)



		return new_recovered_people



	def determine_hospitalizations(self):
		return


	def increment_days_infected(self):
		return

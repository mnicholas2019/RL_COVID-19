from Person import Person
from collections import deque
import math
import random

class City:

	"""
	Constructs a city with the given characteristics. We assume that zero are hospitalized at first,
	zero are dead, zero recovered. 
	"""
	def __init__(self, disease, population = 75000, area = 5, hospital_beds = 150, num_infected = 10):
		self.population = population # Total population of city
		self.area = area # Area of the city

		self.disease = disease

		self.hospital_beds = hospital_beds # Number of hospital beds
		self.water_stations = 0 # Water Stations deployed to area
		self.susceptible = deque() # list of susceptible people to disease
		self.infected_contagious = deque() # List of infected, but not hospitalized people
		self.infected_hospitalized = deque() # List of hospitalized people
		self.infected_needs_bed = deque() # List of infected people in need of hospital beds, but don't have access
		self.recovered = deque() # List of recovered people
		self.dead = deque() # List of dead people
		self.possible_spread = 1 # possible for disease to spread in city at the moment?

		self.cumulative_days_needing_bed = 0 # days someone has needed bed

		self.new_infections = 0
		self.new_deaths = 0

		# create num_infected persons
		for x in range(num_infected):
			person = Person(id = x, age = random.randint(0, 100))
			person.infect(self.disease)
			self.infected_contagious.append(person)

		for x in range(population - num_infected):
			self.susceptible.append(Person(id = x + num_infected, age = random.randint(0,100)))


	"""
	Return the curent state of the city for input into RL model
	"""
	def get_state(self):
		state = []
		state.append(len(self.susceptible))
		state.append(len(self.infected_contagious))
		state.append(len(self.infected_hospitalized))
		state.append(len(self.infected_needs_bed))
		state.append(len(self.recovered))
		state.append(len(self.dead))
		state.append(self.hospital_beds)
		state.append(self.water_stations)

		return state


	"""
	Adds x beds to hospital capacity
	"""
	def add_field_hospital(self, num_beds):
		self.hospital_beds += num_beds
		return

	"""
	Adds water station to city
	"""
	def add_water_station(self):
		self.water_stations += 1
		return

	"""
	Runs the simulation for x days. Should call 'update' for each person in the city. 
	Should move persons to different list accordingly and updates instance variables
	of the city and persons. We should decide who becomes infected here.
	"""
	def update(self, days = 1):
		"""
		Determine who from the susceptible people to infect.
		Then Infect Them. Add them to contagious
		"""

		new_infected_people = self.determine_infections()
		self.new_infections = len(new_infected_people)
		for person in new_infected_people:
			person.infect(self.disease)
			self.infected_contagious.append(person)



		"""
		See which hospitalized patients or patients needing bed
		will die from disease. Kill them if so. Free the beds accordingly
		"""
		new_killed_people = self.determine_deaths()
		self.new_deaths = len(new_killed_people)
		for person in new_killed_people:
			person.die()
			self.dead.append(person)


		"""
		Recover patients and add them to list. Free beds accordingly
		"""
		new_recovered_people = self.determine_recoveries()
		for person in new_recovered_people:
			person.recover()
			self.recovered.append(person)

		"""
		Determine who of the Infected, Contagious People will
		need a hospital bed. Place move them put them on waiting queue
		"""
		new_needs_beds = self.determine_hospitalizations()
		for person in new_needs_beds:
			person.needs_bed()
			self.infected_needs_bed.append(person)
			

		"""
		Place those that need a bed in a bed if available
		"""
		while (len(self.infected_hospitalized) < self.hospital_beds and len(self.infected_needs_bed) > 0):
			person = self.infected_needs_bed.popleft()
			person.hospitalize()
			self.infected_hospitalized.append(person)		

		"""
		Increment days infected
		"""
		self.increment_days_infected()

		if (len(self.infected_contagious) + len(self.infected_hospitalized) +
			len(self.infected_needs_bed) == 0):
			self.possible_spread = 0
			return 0

		"""
		Do nothing for recovered and dead
		"""
		return 1

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
		pop_density = len(self.susceptible)/self.area # susceptible people per sq km
		contact_ratio = 0.0005 #percentage of people within k sq km you come into contact with was 0.0005
		num_contacts = math.ceil(pop_density * contact_ratio) # number of people an infected person comes into contact with
		tr = self.disease.transmission_rate / (self.water_stations + 1) # current transmission rate of disease
		total_contacts = num_contacts * len(self.infected_contagious)
		potential_infections = min(total_contacts, len(self.susceptible))

		new_infected_people = []

		for x in range(potential_infections):
			person = self.susceptible.popleft()
			if (random.random() < tr):
				new_infected_people.append(person)
			else:
				self.susceptible.append(person)	
		#print("New infections this iteration: ", len(new_infected_people), "\ncontacts per infected individuals: ", num_contacts)
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
			if (random.random() < person.get_daily_death_rate()):
				new_killed_people.append(person)
			else:
				self.infected_hospitalized.append(person)

		num_needs_bed = len(self.infected_needs_bed)
		for x in range(num_needs_bed):
			person = self.infected_needs_bed.popleft()
			if (random.random() < person.get_daily_death_rate()):
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
		days_till_recovery = self.disease.mean_recovery_time # should I make this input to city? like a disease characteristics vector. placeholder for now

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
		for x in range(num_infected_contagious):
			person = self.infected_contagious.popleft()
			if (person.days_infected == days_till_recovery): # This is just a placeholder. Will use better effect later
				new_recovered_people.append(person)
			else:
				self.infected_contagious.append(person)



		return new_recovered_people



	def determine_hospitalizations(self):
		new_needs_beds = []
		days_till_hosp = self.disease.mean_time_to_hosp # placeholder for now. cmight make this input to city, or disease characteristics or whatever

		num_infected_contagious = len(self.infected_contagious)
		for x in range(num_infected_contagious):
			person = self.infected_contagious.popleft()
			if (person.days_infected == days_till_hosp): # This is just a placeholder. Will use better effect later
				if (random.random() < person.hospitalization_rate):
					new_needs_beds.append(person)
				else:
					self.infected_contagious.append(person)
			else:
				self.infected_contagious.append(person)
		return new_needs_beds


	def increment_days_infected(self):
		for person in self.infected_contagious:
			person.days_infected += 1
		for person in self.infected_needs_bed:
			person.days_infected += 1
			self.cumulative_days_needing_bed += 1
		for person in self.infected_hospitalized:
			person.days_infected += 1
		return

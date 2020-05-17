class Person:

	"""
	Initialize Person with given traits.
	Need a better way to tell what state person is in. Something like Enum in C

	States:
		Susceptible = 0
		Infected, Contagious = 1
		Infected, Hospitalized = 2
		Infected, Needs Bed = 3
		Recovered = 4
		Dead = 5
	"""
	#this is a test
	def __init__(self, id, age, infected):
		self.id = id
		self.age = age
		self.days_infected = 0
		self.death_rate = 0




		if (infected == True):
			self.states = 1
		else:
			self.states = 0



	"""
	Runs simulation for x days and updates person accordingly.

	What can happen according to current state of person:

		Susceptible
	-Can become infected, or remain Susceptible. Need to decide if we infect
	people from 'City' class, or here. I think its best from City and we make
	an infect function from the other class since it will be based on density
	and the number of water stations present

		Infected, Contagious
	-increment days_infected. 
	-if it is the 6th day infected, determine if they will enter hospital based
	on statistics from age (need to find a good source for this)
	-if not hospitalzed, keep incrementing until day 10 (maybe 14 days, need to
	find good number of days until recovery)

		Infected, Hospitalized
	- we assume hospitalization for some number of days (lets say 10 for now)
	- every day they die with some x% chance (need to find a good % for this) may
	also make this death rate dependent on age etc
	- if they don't die increment days_infected
	- after 15 days, if they dont die, they become recovered

		Infected, Needs Bed
	- same as Infected, Hospitalized, but much higher death rate TBD

		Recovered
	- no update needed. We assume immunity

		Dead
	- no update needed
	"""
	def update(self, infected, hospitalized, needs_bed, dead ):
		# Finite state machine
		if (self.states == 0): # susceptible
			if(infected == True):
				self.states = 1
				self.days_infected = 0
		elif (self.states == 1): # contagious
			if(hospitalized == True):
				self.states =2
				self.death_rate = 0.1 #rate1 # value TBD
			elif(needs_bed ==True): 
				self.states = 3
				self.death_rate = 0.1 + 0.2 #rate1 + rate2 # value TBD
			self.days_infected += 1

		elif (self.states == 2): # hospitalized
			if(dead==True):
				self.states = 5
			elif(self.days_infected == 15 ): #recovery time
				self.states = 4
			else:
				self.days_infected +=1
		elif (self.states == 3): # needs bed
			if(dead==True):
				self.states = 5
			elif(self.days_infected ==15): # recovery time
				self.states = 4
			elif(hospitalized == True):
				self.states == 2
				self.days_infected +=1
			else:
				self.days_infected +=1
		elif (self.states == 4): # recovered and immune
			self.death_rate = 0
		elif (self.states == 5): # dead
			self.death_rate = 1


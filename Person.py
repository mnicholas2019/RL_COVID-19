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
	def __init__(self, age, infected):
		self.age = age
		self.days_infected = 0
		self.death_rate = 0



		if (infected == True):
			self.status = 1
		else:
			self.status = 0



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
	def update(self, days):


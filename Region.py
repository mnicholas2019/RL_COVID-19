from City import City

class Region:

	def __init__(self, cities, water_stations = 4, field_hospitals = 4, field_hospital_capacity = 1000):
		self.cities = cities
		self.water_stations = water_stations
		self.field_hospitals = field_hospitals
		self.field_hospital_capacity = field_hospital_capacity

	def get_state(self):
		states = []
		for city in self.cities:
			states.append(city.get_state())
		return states

	def update(self):
		cities_finished = 0
		for city in self.cities:
			if (city.possible_spread):
				city.update()
			else:
				cities_finished += 1
		if (cities_finished == len(self.cities)):
			return 0
		return 1

	def take_action(self, city, action):
		if (action == 1 and self.water_stations > 0):
			self.cities[city].add_water_station()
		elif (action == 0 and self.field_hospitals > 0):
			self.cities[city].add_field_hospital()
		else:
			print("no action taken")
from City import City
from Disease import Disease
from Region import Region
import sys


def initialize_simulation():
	covid19 = Disease()

	cities = []
	city1 = City(disease = covid19)
	city2 = City(disease = covid19, population = 100000, area = 5, 
				 hospital_beds = 100000, num_infected = 2)
	city3 = City(disease = covid19, population = 50000, area = 10, 
				 hospital_beds = 50000, num_infected = 20)
	city4 = City(disease = covid19, population = 200000, area = 8, 
				 hospital_beds = 200000, num_infected = 3)
	city5 = City(disease = covid19, population = 20000, area = 3, 
				 hospital_beds = 20000, num_infected = 10)
	city6 = City(disease = covid19, population = 30000, area = 6, 
				 hospital_beds = 30000, num_infected = 15)
	city7 = City(disease = covid19, population = 125000, area = 5, 
				 hospital_beds = 125000, num_infected = 1)
	cities.append(city1)
	cities.append(city2)
	cities.append(city3)
	cities.append(city4)
	cities.append(city5)
	cities.append(city6)
	cities.append(city7)

	region = Region(cities)

	return region


def play_user_input():

	region = initialize_simulation()
	day = 0

	print("Day: ", day)
	print(region.get_state())

	while 1:
		day += 1
		data = input("proceed to next day? (y/n)\n")
		if data != 'n':
			print("Day: ", day)
			status = region.update()
			print(region.get_state())
		else:
			break
		if (status == 0):
			break

	print("simulation over")

	region.get_final_stats()

	# covid19 = Disease() # baseline parameters
	# test_city = City(disease = covid19)
	# day = 0
	# print("Day: ", day)
	# print(test_city.get_state())
	# while 1:
	# 	day += 1
	# 	data = input("proceed to next day? (y/n)\n")
	# 	if data != 'n':
	# 		print("Day: ", day)
	# 		status = test_city.update()
	# 		print(test_city.get_state())
	# 	else:
	# 		break
	# 	if (status == 0):
	# 		break

	# print("simulation over")


	return

if __name__ == "__main__":
	play_user_input()

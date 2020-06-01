from City import City
from Disease import Disease
from Region import Region
from DQNAgent import DQNAgent
import sys
import numpy as np
import collections

def initialize_simulation():
	covid19 = Disease()

	cities = []
	city1 = City(disease = covid19)
	city2 = City(disease = covid19, population = 100000, area = 5, 
				 hospital_beds = 200, num_infected = 2)
	city3 = City(disease = covid19, population = 50000, area = 10, 
				 hospital_beds = 100, num_infected = 20)
	city4 = City(disease = covid19, population = 200000, area = 8, 
				 hospital_beds = 400, num_infected = 3)
	city5 = City(disease = covid19, population = 20000, area = 3, 
				 hospital_beds = 40, num_infected = 10)
	city6 = City(disease = covid19, population = 30000, area = 6, 
				 hospital_beds = 60, num_infected = 15)
	city7 = City(disease = covid19, population = 125000, area = 5, 
				 hospital_beds = 250, num_infected = 1)
	cities.append(city1)
	cities.append(city2)
	cities.append(city3)
	cities.append(city4)
	cities.append(city5)
	cities.append(city6)
	cities.append(city7)

	region = Region(cities)

	return region


def play_step_days():

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
			print("Cost: ", region.get_reward())
		else:
			break
		if (status == 0):
			break

	print("simulation over")

	final_stats = region.get_final_stats()

	return final_stats

def play_user_input():

	region = initialize_simulation()
	day = 0

	print("Day: ", day)
	print(region.get_state())

	while 1:
		day += 1
		action = input("water station (1), field hospital (2), nothing (3)")
		print("action", action)
		if action == '1' or action == '2':
			city = input("which city? (1-7)")
			region.take_action(city, action)
		print("Day: ", day)
		status = region.update()
		print(region.get_state())
		print("Cost: ", region.get_reward())
		if (status == 0):
			break

	print("simulation over")

	final_stats = region.get_final_stats()


	return final_stats

def run_sim_through():
	region = initialize_simulation()
	day = 0

	print("Day: ", day)
	print(region.get_state())

	while 1:
		day += 1
		print("Day: ", day)
		status = region.update()
		print(region.get_state())
		print("Cost: ", region.get_reward())
		if (status == 0):
			break

	print("simulation over")

	final_stats = region.get_final_stats()


	return final_stats
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def train_agent(games):

	weights_path = 'training_checkpoints/'
	agent = DQNAgent()
	# agent.load(some path)

	game_counter = 0
	simulation_results = []

	while game_counter < games:
		day = 0
		region = initialize_simulation()
		state = region.get_state()
		done = 0
		while 1:
			state = region.get_state()
			print(state)

			flat_state = flatten(state)
			#print(flat_state)
			transpose = np.reshape(flat_state,(58,))
			#print(transpose)
			state = transpose
			print("Day: ", day)
			print(state.shape)
			action = agent.get_action(state)
			print(action)
			region.take_action(action[0], action[1])
			status = region.update()
			print(status)
			#if done, set done to 1
			new_state = region.get_state()
			print(new_state)

			reward = region.get_reward()

			agent.memorize(state, action, reward, next_state, done)
			#train with some probability for individual and group

			if status == 0:
				break

		game_counter += 1
		agent.save(weights_path + game_counter)




if __name__ == "__main__":
	
	final_stats_sim = train_agent(2)#run_sim_through()
	#final_stats_game = play_user_input()

	print("Not infected: ", final_stats_sim[0])
	print("Recovered: ", final_stats_sim[1])
	print("Dead: ", final_stats_sim[2])
	print("Cumulative days needing bed: ", final_stats_sim[3])

	print("Not infected: ", final_stats_game[0])
	print("Recovered: ", final_stats_game[1])
	print("Dead: ", final_stats_game[2])
	print("Cumulative days needing bed: ", final_stats_game[3])

	
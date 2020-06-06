from City import City
from Disease import Disease
from Region import Region
from DQNAgent import DQNAgent
import sys
import numpy as np
import collections
import matplotlib.pyplot as plt

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

	# city1 = City(disease = covid19, population = 200, area= .005,
	# 			 hospital_beds = 5, num_infected = 3)
	# city2 = City(disease = covid19, population = 100, area = .001, 
	# 			 hospital_beds = 2, num_infected = 2)
	# city3 = City(disease = covid19, population = 500, area = .01, 
	# 			 hospital_beds = 2, num_infected = 2)
	# city4 = City(disease = covid19, population = 75, area = .001, 
	# 			 hospital_beds = 2, num_infected = 2)
	# city5 = City(disease = covid19, population = 50, area = .001, 
	# 			 hospital_beds = 2, num_infected = 2)

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
			done = region.update()
			print(region.get_state())
			print("Cost: ", region.get_reward())
		else:
			break
		if (done == 1):
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
		done = region.update()
		print(region.get_state())
		print("Cost: ", region.get_reward())
		if (done == 1):
			break

	print("simulation over")

	final_stats = region.get_final_stats()


	return final_stats

def run_sim_through():
	region = initialize_simulation()
	day = 0

	print("Day: ", day)
	print(region.get_state())

	susceptible = []
	infected = []
	recovered = []
	dead = []

	while 1:
		# get current stats
		stats = region.get_graph_values()
		susceptible.append(stats[0])
		infected.append(stats[1])
		recovered.append(stats[2])
		dead.append(stats[3])


		day += 1
		print("Day: ", day)
		done = region.update()
		print(region.get_state())
		print("Cost: ", region.get_reward())
		if (done):
			break

	print("simulation over")

	days = []
	for x in range(day):
		days.append(x+1)
	plt.plot(susceptible, label = "susceptible")
	plt.plot(infected, label = "infected")
	plt.plot(recovered, label = "recovered")
	plt.plot(dead, label = "dead")
	plt.legend()

	# plt.plot(days, susceptible, days, infected, days, recovered, days, dead)
	plt.show()
	final_stats = region.get_final_stats()


	return final_stats


def run_agent(games = 1, train = True, model=False, save_model = True):

	weights_path = 'throwaway/'
	agent = DQNAgent(num_parameters=75)
	if (train == False):
		agent.epsilon = 0
	final_stats = []
	
	if model != False:
		agent.load(model)



	game_counter = 0
	simulation_results = []
	done = 0
	all_moves = []
	while game_counter < games:
		day = 0
		region = initialize_simulation()
		moves_made = []
		while 1:

			# get human readable state
			print("\nDay: ", day)
			state = region.get_state()
			region.print_state(state)

			# transform state for input into DQN
			state = agent.transform_state(state)

			# get action from DQN. Dependent on epsilon
			action = agent.get_action(state, region.water_stations, region.field_hospitals)

			# if (region.water_stations > 0):
			# 	action = [1,1]
			# else:
			# 	action = [-1, 3]

			print("wanted action: ", action)
			if (train == False and action != [-1, 3]):
				moves_made.append([day, action])

			# perform the action and update the state
			region.take_action(str(action[0]), str(action[1]))
			done = region.update()


			# get the new state we are in
			next_state = region.get_state()
			next_state = agent.transform_state(next_state)

			# get the reward for the state we are now in. Combination
			# of deaths and infections at new state
			reward = region.get_reward()

			if train:
				agent.train_individual(state, action, reward, next_state, done)
				print("Training!")

			# add to memory 
			agent.memorize(state, action, reward, next_state, done)

			if done == 1:
				break
			day += 1

			
			data = input("proceed to next day? (y/n)\n")
			if data == 'n':
				break

		game_counter += 1
		if train:
			agent.train_batch(400)
			print("training episode")
		if save_model and train and game_counter%20 == 0:
			agent.save_model(weights_path + 'post_game' + str(game_counter))
		final_stats.append(region.get_final_stats())
		all_moves.append(moves_made)
	return final_stats, all_moves






if __name__ == "__main__":

	################
	# run simulation
	################
	# results = run_sim_through()

	# print("Days of simulation: ", results[4])
	# print("Not infected: ", results[0])
	# print("Recovered: ", results[1])
	# print("Dead: ", results[2])
	# print("Cumulative days needing bed: ", results[3])
	# print("Water Stations Remaining: ", results[5])
	# print("Field Hospitals Remaining: ", results[6])
	# print("Game score: ", results[1] + results[2])




	##################
	# Training Here
	##################
	#results = run_agent(games=500, train=True, model = False, save_model = True)


	####################
	# Evaluation is here
	####################
	test_runs=[40]
	# for i in range(5):
	# 	test_runs.append((i+1))
	total_results = []
	game_scores = []
	moves = []

	for x in test_runs:
		model = 'throwaway/post_game' + str(x)
		final_stats_agent, all_moves = run_agent(games=1, train=False, model = model, save_model= False)
		total_results.append(final_stats_agent)
		moves.append(all_moves)
	for i, results in enumerate(total_results):
		print("\n\nSimulation for episode:",test_runs[i])
		print("Days of simulation: ", results[0][4])
		print("Not infected: ", results[0][0])
		print("Recovered: ", results[0][1])
		print("Dead: ", results[0][2])
		print("Cumulative days needing bed: ", results[0][3])
		print("Water Stations Remaining: ", results[0][5])
		print("Field Hospitals Remaining: ", results[0][6])
		print("Game score: ", results[0][1] + results[0][2])
		print("Moves Taken: ", moves[i][0])

		game_scores.append(results[0][1] + results[0][2])


	plt.plot(test_runs, game_scores)
	plt.show()

	# 
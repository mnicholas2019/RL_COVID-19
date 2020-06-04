from City import City
import numpy as np

class Region:

    def __init__(self, cities, water_stations = 4, field_hospitals = 4, field_hospital_capacity = 100):
        self.cities = cities
        self.water_stations = water_stations # number of water stations remaining
        self.field_hospitals = field_hospitals # number of field hospitals remaining
        self.field_hospital_capacity = field_hospital_capacity
        self.days = 0

    def get_state(self):
        states = []
        for city in self.cities:
            states.append(city.get_state())
        states.append(self.water_stations)
        states.append(self.field_hospitals)
        return states


    def update(self):
        self.days += 1
        cities_finished = 0
        for city in self.cities:
            if (city.possible_spread):
                city.update()
            else:
                cities_finished += 1
        if (cities_finished == len(self.cities)):
            return 1
        return 0

    def take_action(self, city, action):
        if (action == '1' and self.water_stations > 0):
            self.cities[int(city)-1].add_water_station()
            self.water_stations = self.water_stations - 1
            print("action 1 taken")
        elif (action == '2' and self.field_hospitals > 0):
            self.cities[int(city)-1].add_field_hospital(self.field_hospital_capacity)
            self.field_hospitals = self.field_hospitals - 1
            print("action 2 taken")
        else:
            print("no action taken")

    def get_final_stats(self):
        num_dead = 0
        num_recovered = 0
        num_not_infected = 0
        days_needing_bed = 0
        for city in self.cities:
            num_dead += len(city.dead)
            num_recovered += len(city.recovered)
            num_not_infected += len(city.susceptible)
            days_needing_bed += city.cumulative_days_needing_bed
            # TODO implement total days spent needing bed
        return [num_not_infected, num_recovered, num_dead, days_needing_bed, 
        self.days, self.water_stations, self.field_hospitals, self.get_reward()]

    def get_reward(self):
        deaths = 0
        infections = 0
        for city in self.cities:
            deaths += city.new_deaths
            infections += city.new_infections

        print("New Infections: ", infections, "New deaths: ", deaths)
        return (infections + 5*deaths)

    def print_state(self, state):
        for i, city in enumerate(state[0:7]):
            print("\nCity", i, ":")
            print("Sus: ", city[0], "Inf:", city[1], "inf_hosp:", city[2], 
                  "needs_bed:", city[3], "rec:", city[4], "dead:", city[5],
                  "hosp capacity:", city[6], "water stations:", city[7])

        print('\n Available Field Hospitals: ', self.field_hospitals, 'Available water stations:', self.water_stations)


        return

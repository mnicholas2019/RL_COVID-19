class Disease:

	def __init__(self, transmission_rate = 0.1, death_rate = [0.1, 0.1, 0.1], hospitalization_rate = [0.5, 0.5, 0.5],
				 mean_recovery_time = 15, mean_time_to_hosp = 6, age_brackets = [0, 50, 75]):

		self.transmission_rate = transmission_rate
		self.death_rate = death_rate
		self.hospitalization_rate = hospitalization_rate
		self.mean_recovery_time = mean_recovery_time
		self.mean_time_to_hosp = mean_time_to_hosp
		self.age_brackets = age_brackets # each element is the start of the age bracket

	def get_age_bracket_index(self, age):
		for x in range(len(self.age_brackets) - 1):
			if (age < self.age_brackets[x + 1]):
				return x
		return len(self.age_brackets) - 1

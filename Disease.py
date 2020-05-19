class Disease:

	def __init__(self, transmission_rate = 0.3, hospitalized_death_rate = 0.2, hospitalization_rate =0.2,
				 mean_recovery_time = 15, mean_time_to_hosp = 6):

		self.transmission_rate = transmission_rate
		self.hospitalized_death_rate = hospitalized_death_rate
		self.hospitalization_rate = hospitalization_rate
		self.mean_recovery_time = mean_recovery_time
		self.mean_time_to_hosp = mean_time_to_hosp



from City import City
from Disease import Disease
import sys

def main():

	covid19 = Disease() # baseline parameters
	test_city = City(disease = covid19)
	day = 0
	print("Day: ", day)
	print(test_city.get_state())
	while 1:
		day += 1
		data = input("proceed to next day? (y/n)\n")
		if data != 'n':
			print("Day: ", day)
			status = test_city.update()
			print(test_city.get_state())
		else:
			break
		if (status == 0):
			break

	print("simulation over")


	return

if __name__ == "__main__":
	main()

from classes.evolution import Evolution
from classes.shiftplan import Shiftplan

if  __name__ =='__main__':

	year = 2013
	month = 10
	workers = 5

	sh = Shiftplan()

	sh.setParameters(year, month, workers, 3)
	parCount = sh.getParameterCount()
	print(parCount)
	evolution = Evolution(parCount, 3, sh.evaluate)
	evolution.evolve(1)


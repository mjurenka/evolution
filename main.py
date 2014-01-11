from classes.evolution import Evolution
from classes.shiftplan import Shiftplan

if  __name__ =='__main__':

	year = 2013
	month = 10
	workers = 5

	sh = Shiftplan()

	sh.setParameters(year, month, workers, 2)
	parCount = sh.getParameterCount()
	# print(parCount)
	evolution = Evolution(parCount, 2, sh.evaluate)
	evolution.loadPopulation()

	evolution.evolve(500)

	best = evolution.getBestSolution(0)
	sh.loadChromosome(best)
	print(sh.renderToString())
	print(best.getFitness())

	evolution.exportPopulation()


from classes.evolution import Evolution
from classes.shiftplan import Shiftplan

if  __name__ =='__main__':

	year = 2013
	month = 10
	workers = 5

	sh = Shiftplan()
	sh.setParameters(year, month, workers)

	evolution = Evolution(year, month, workers, sh.evaluate)
	evolution.evolve(100)

	sh.loadChromosome(evolution.population[0])
	print(sh.renderToString())
	print(sh.evaluate(evolution.population[0]))
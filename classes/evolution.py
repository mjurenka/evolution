import random
from calendar import monthrange
from datetime import date
from copy import deepcopy

from classes.chromosome import Chromosome

class Evolution(object):
    """docstring for Evolution"""

    # CONSTANTS
    INITIAL_POPULATION_SIZE = 100
    TAKEOVER_POPULATION_SIZE = 30
    SELECT_BEST_COUNT = 20
    SELECT_WORST_COUNT = 10

    SHIFT_NOSHIFT = 0
    SHIFT_LATE = 1
    SHIFT_ONCALL = 2

    # CLASS VARIABLES
    workers = 0
    year = 0
    month = 0
    days = 0
    counter = 0
    population = []
    solutions = []
    evalFunction = None

    def __init__(self, year, month, numberOfWorkers, evaluationFunction):
        self.month = month
        self.year = year
        self.workers = numberOfWorkers
        self.days = monthrange(year, month)[1]
        self.evalFunction = evaluationFunction

    def evolveSingle(self):
        # create new population if none present
        self.createFirstPopulation()

        newPopulation = []

        # # add old population
        newPopulation.extend(self.population)

        # generate new individuals
        newPopulation.extend(self.generatePopulation(self.INITIAL_POPULATION_SIZE - len(self.population)))

        # # evaluate and sort
        newPopulation = self.evaluateAndSort(newPopulation)

        best = []
        # select best
        best.extend(newPopulation[0:self.SELECT_BEST_COUNT])

        worst = []
        # select worst
        worst.extend(newPopulation[len(newPopulation) - self.SELECT_WORST_COUNT : self.SELECT_WORST_COUNT])

        # genetic operators
        # NONE ATM

        # crossbreed
        # newPopulation.extend(self.crossbreed(best, newPopulation, 2))

        # # mutate
        newPopulation.extend(self.mutate(best, 30, 3))

        # newPopulation.extend(self.mutate(newPopulation, 10, 1))



        # # evaluate
        newPopulation = self.evaluateAndSort(newPopulation)

        # # substitute
        self.population = []

        self.population = self.evaluateAndSort(newPopulation)[0 : self.SELECT_BEST_COUNT]

    def createFirstPopulation(self):
        if(len(self.population) == 0):
            self.population.extend(self.generatePopulation(self.INITIAL_POPULATION_SIZE))

    def evolve(self, evolutionCount):
        for i in range(evolutionCount):
            self.evolveSingle()
            self.counter += 1

    def getBestSolution(self, index):
        if(len(self.population) == 0):
            return Chromosome()
        else:
            return self.population[index]

    def isWeekend(self, day):
        # days start from 0
        day += 1
        day = day % self.days
        if(day == 0):
            day += 1

        dt = date(self.year, self.month, day)
        if(dt.isoweekday() == 6):
            return True
        elif(dt.isoweekday() == 7):
            return True
        else:
            return False

    def generateSingle(self):
        single = Chromosome([self.SHIFT_NOSHIFT] * (self.workers * self.days))

        for i in range(self.days):

            if(not self.isWeekend(i)):
                single.changeGene(self.SHIFT_LATE, single.getRandomPositionByGene(self.SHIFT_NOSHIFT))

            single.changeGene(self.SHIFT_ONCALL, single.getRandomPositionByGene(self.SHIFT_NOSHIFT))
        return single

    def generatePopulation(self, populationSize):
        newPopulation = []
        for i in range(populationSize):
            single = self.generateSingle()
            newPopulation.append(single)

        return newPopulation

    def evaluate(self, chromosome):
        return self.evalFunction(chromosome)

    def evaluateAndSort(self, population):
        return sorted(population, key=lambda Ch: self.evaluate(Ch))


    def mutate(self, population, percentage, mutationSize):
        # p = population[:]
        newPopulation = []

        for i in range(int(len(population) * percentage)):
            place1 = random.randint(0, population[0].getSize() - 1)
            place2 = random.randint(0, population[0].getSize() - 1)
            randomNumber = random.randint(0, len(population) - 1)
            # WARNING, moze sa to dokaslat tu
            victim = deepcopy(population[randomNumber])

            for j in range(mutationSize):
                originalGene = victim.getGene(place1)
                victim.changeGene(victim.getGene(place2), place1)
                victim.changeGene(originalGene, place2)

            newPopulation.append(victim)

        return newPopulation

    def crossbreed(self, bestIndividuals, population, crossbreedSize):
        newPopulation = []

        for individual in bestIndividuals:
            day = random.randint(0, self.days - 1)
            person = random.randint(0, self.workers - 1) * self.days
            randomNumber = random.randint(0, len(population) - 1)

            child = deepcopy(individual)
            parent1 = deepcopy(population[randomNumber])

            for i in range(crossbreedSize):
                child.changeGene(parent1.getGene(person + day), person + day)

            newPopulation.append(child)

        return newPopulation

    def fuseChromos(firstCH, secondCH, fusionPosition):
        fusedChromo = Chromosome()
        for i in range(firstCH.getSize()):
            if(i < fusionPosition):
                fusedChromo.addGene(firstCH.getGene(i))
            else:
                fusedChromo.addGene(secondCH.getGene(i))

        return fusedChromo
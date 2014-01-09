import random
import collections
import gc
from calendar import monthrange
from datetime import date
from copy import deepcopy

from classes.chromosome import Chromosome

class Evolution(object):
    """docstring for Evolution"""

    # CONSTANTS
    INITIAL_POPULATION_SIZE = 10
    TAKEOVER_POPULATION_SIZE = 1
    SELECT_BEST_COUNT = 1
    SELECT_WORST_COUNT = 1

    # CLASS VARIABLES
    parCount = 0
    parBitSize = 0
    chromoSize = 0
    counter = 0
    population = []
    solutions = []
    evalFunction = None

    def __init__(self, parameterCount, parameterBitSize, evaluationFunction):
        self.parCount = parameterCount
        self.parBitSize = parameterBitSize
        self.chromoSize = self.parBitSize * self.parCount
        self.evalFunction = evaluationFunction

    def evalFirstTen(self, pop):
        out = []
        for i in range(10):
            out.append(self.evaluate(pop[i]))
        return out

    def evolveSingle(self):
        # create new population if none present
        self.createFirstPopulation()
        print(self.population[0].chromo)
        newPopulation = []
        # add old population
        newPopulation.extend(self.population)

        # generate new individuals
        newPopulation.extend(self.generatePopulation(self.INITIAL_POPULATION_SIZE - len(self.population)))

        # # evaluate and sort
        newPopulation = self.evaluateAndSort(newPopulation)

        # select best
        best = []
        best.extend(deepcopy(newPopulation[0:self.SELECT_BEST_COUNT]))

        # select worst
        worst = []
        worst.extend(deepcopy(newPopulation[len(newPopulation) - self.SELECT_WORST_COUNT : self.SELECT_WORST_COUNT]))

        # genetic operators
        # NONE ATM

        # # crossbreed
        # newPopulation.extend(self.crossbreed(best, newPopulation, 2))
        # newPopulation.extend(self.crossbreed(worst, newPopulation, 2))

        # mutate
        # newPopulation.extend(self.mutate(best, 100, 1))
        # newPopulation.extend(self.mutate(worst, 100, 1))
        # newPopulation.extend(self.mutate(newPopulation, 10, 5))



        # evaluate
        newPopulation = self.evaluateAndSort(newPopulation)

        # substitute
        self.population = []
        self.population = newPopulation[0 : self.SELECT_BEST_COUNT]
        gc.collect()

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
    
    def generateSingle(self):
        single = Chromosome([0] * self.chromoSize)
        worker = None
        for i in range(self.chromoSize):
            single.addGene(random.randint(0, 1))
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
        return sorted(population, key=lambda Ch: 0, reverse=True)


    def mutateIndividual(self, individual, percentage):
        offspring = Chromosome(individual.getChromo())
        usedPositions = []
        for i in range(self.chromoSize * percentage):
            while True:
                position = random.randint(0, self.chromoSize)
                if(not position in usedPositions):
                    break
<<<<<<< HEAD
            gene = offspring.getGene(position)
            if(gene == 1):
                newGene = 0
            elif(gene == 0):
                newGene = 1
            else:
                newGene = 0

            offspring.changeGene(newGene, position)
        return offspring

    def crossoverParents(self, parent1, parent2):
        while True:
            place1 = random.randint(0, self.chromoSize)
            place2 = random.randint(0, self.chromoSize)
            if(place1 > place2):
                break
        offspring = Chromosome([0] * self.chromoSize)
        interator = 0
        
        for i in parent1[0:place1] + parent2[place1:place2] + parent1[place2:self.chromoSize]:
            offspring.changeGene(i, interator)
            interator = interator + 1

        return offspring
    def exportPopulation(self):
        f = open('lastState.txt', 'w')
        for chromo in self.population:
            f.write(chromo.toString() + "\n")
        f.close

    def loadPopulation(self):
        f = open('lastState.txt', 'r')
        for line in f:
            single = Chromosome(len(line))
            single.fromString(line)
            self.population.append(single)
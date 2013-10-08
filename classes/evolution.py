import random
from calendar import monthrange
from datetime import date

from classes.chromosome import Chromosome

class Evolution(object):
    """docstring for Evolution"""

    # CONSTANTS
    INITIAL_POPULATION_SIZE = 10
    TAKEOVER_POPULATION_SIZE = 10
    SELECT_BEST_COUNT = 2
    SELECT_WORST_COUNT = 2
    GENERATE_NEW_COUNT = 10

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

    def __init__(self, month, year, numberOfWorkers):
        self.month = month
        self.year = year
        self.workers = numberOfWorkers
        self.days = monthrange(year, month)[1]

    def evolveSingle(self):
        # create new population if none present
        self.createFirstPopulation()

        # newPopulation = []

        # # generate new individuals
        # newPopulation.extend(self.generatePopulation(self.GENERATE_NEW_COUNT))

        # # add old population
        # newPopulation.extend(self.population)

        # # evaluate and sort
        # newPopulation = self.evaluateAndSort(newPopulation)

        # best = []
        # # select best 20
        # best.extend(newPopulation[0:self.E_SELECT_BEST_COUNT])

        # worst = []
        # # select worst 20
        # worst.extend(newPopulation[-(self.E_SELECT_WORST_COUNT)])

        # # genetic operators
        # # NONE ATM

        # # crossbreed
        # newPopulation.extend(self.crossbreed(best, newPopulation, 100))

        # # mutate
        # newPopulation.extend(self.mutate(best, 30, 100))

        # # evaluate
        # newPopulation = self.evaluateAndSort(newPopulation)

        # # substitute
        # self.population = []

        # # take 100 to new
        # #   if dont have 100, generate rest to have 100
        # if(len(newPopulation) < self.E_TAKEOVER_POPULATION_SIZE):
        #     newPopulation.extend(self.generatePopulation(self.E_TAKEOVER_POPULATION_SIZE - len(newPopulation)))

        # self.population = newPopulation[0:self.E_TAKEOVER_POPULATION_SIZE]

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
        dt = date(self.year, self.month, day)
        if(dt.isoweekday() == 6):
            return True
        elif(dt.isoweekday() == 7):
            return True
        else:
            return False

    def generateSingle(self):
        single = Chromosome([self.SHIFT_NOSHIFT] * self.workers * self.days)
        print(len(single.chromo))
        for i in range(self.days * self.workers):
            if(not self.isWeekend((i + 1) % self.days)):
                single.changeGene(self.SHIFT_LATE, single.getRandomPositionByGene(self.SHIFT_NOSHIFT))

            single.changeGene(self.SHIFT_ONCALL, single.getRandomPositionByGene(self.SHIFT_NOSHIFT))
        return single

    def generatePopulation(self, populationSize):
        if(populationSize <= 0):
            return None
        print(populationSize)
        newPopulation = []
        for i in range(populationSize):
            newPopulation.append(self.generateSingle())

        return newPopulation

    def evaluate(self, chromosome):
        return random.randint(0, 100)

    def evaluateAndSort(self, population):
        return sorted(population, key=lambda Ch: self.evaluate(Ch.chromo))


    def mutate(self, population, percentage, mutationSize):
        # p = population[:]
        newPopulation = []

        for i in range(int(len(population) * percentage)):
            randomNumer = random.randint(0, len(population))
            # WARNING, moze sa to dokaslat tu
            victim = Chromosome(population[randomNumer].chromo)

            for j in range(mutationSize):
                mutationPlace = random.randint(0, self.days)

                mutationSource = random.randint(0, self.workers) * mutationPlace
                mutationDest = random.randint(0, self.workers) * mutationPlace

                mutatedGene = victim.getGene(mutationSource)
                victim.changeGene(mutatedGene, mutationDest)

            newPopulation.append(victim)

        return newPopulation

        def crossbreed(self, bestIndividuals, population, crossbreedSize):
            newPopulation = []

            for individual in bestIndividuals:
                day = random.randint(0, self.days)
                person = random.randint(0, self.workers) * self.days
                randomNumber = random.randint(0, len(population))

                child = Chromosome(individual.chromo)
                parent1 = Chromosome(population[randomNumber.Chromo])

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
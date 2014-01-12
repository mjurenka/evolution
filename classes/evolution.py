import random
import collections
import gc
from calendar import monthrange
from datetime import date
from copy import deepcopy
import time

from classes.chromosome import Chromosome

class Evolution(object):
    """docstring for Evolution"""

    # CONSTANTS
    INITIAL_POPULATION_SIZE = 200
    SELECT_BEST_COUNT = 2
    REMOVE_WORST_COUNT = 5
    
    CROSSOVER_PERCENTAGE = .87
    CROSSOVER_OFFSPRING_COUNT = 2
    CROSSOVER_PARENT_PAIR_COUNT = 110
    MUTATE_PERCENTAGE = .02
    # CLASS VARIABLES
    parCount = 0
    parBitSize = 0
    chromoSize = 0
    counter = 0
    population = []
    solutions = []
    evalFunction = None
    roulette = []
    importedGeneration = False

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

    def rouletteSelectParents(self, population, selectSize):
        valueList = []
        for i in population:
            fitness = i.getFitness()
            valueList.append(fitness)

        # output pairs of chromosomes
        parentPairs = []
        parentChromosomes = []
        while len(parentPairs) < selectSize:
            

            chosenParents = []

            while len(chosenParents) < 2:
                # choose random number
                randomValue = random.randint(0, sum(valueList))
                # print(sum(valueList))

                parentIndex = 0
                bottomLimit = 0
                for i in valueList:
                    if(parentIndex == 0):
                        bottomLimit = 0

                   
                    # upper limit
                    upperIndex = parentIndex
                    if(not(upperIndex + 1 >= len(valueList))):
                        upperIndex = upperIndex + 1

                    upperLimit = bottomLimit + valueList[upperIndex]

                    # print(str(bottomLimit) + " > " + str(randomValue) + " > " + str(upperLimit))
                    # if number is between two limits
                    if((bottomLimit <= randomValue) and (randomValue < upperLimit)):
                        break

                    parentIndex = parentIndex + 1
                    bottomLimit = bottomLimit + i

                if(parentIndex == len(valueList)):
                    parentIndex = parentIndex - 1

                # now we have found our chosen parent
                # we have to check, if its not the same we have already selected as first parent
                if(not(parentIndex in chosenParents)):
                    # we add him as chosen parent
                    chosenParents.append(parentIndex)
                    
            parentPairs.append(chosenParents)

            chromo1 = deepcopy(population[chosenParents[0]])
            chromo2 = deepcopy(population[chosenParents[1]])
            parentChromosomes.append([chromo1, chromo2])
  
        # self.roulette.extend(chosenParents)
        # print(parentPairs)
        return parentChromosomes

    def evolveSingle(self):
        oldGeneration = self.population

        # create new population if none present
        if(self.createFirstPopulation() or self.checkIfImported()):
            # evaluate
            oldGeneration = self.evaluateAndSort(oldGeneration)

        # elitism
        self.elite = oldGeneration[0:self.SELECT_BEST_COUNT]

        # remove worst
        oldGeneration = oldGeneration[0:len(oldGeneration )- self.REMOVE_WORST_COUNT]

        # crossover 90% of pop
        newPopulation = self.crossover(oldGeneration, self.CROSSOVER_PERCENTAGE)
        # mutate 1% of population
        newPopulation = self.mutatePopulation(newPopulation, self.MUTATE_PERCENTAGE)
        # sometimes offspring copy of parent

        # this is new generation done
        # elitism append back
        newPopulation.extend(self.elite)

        # evaluate
        newPopulation = self.evaluateAndSort(newPopulation)

        # shrink population to initial size
        if(len(newPopulation) > self.INITIAL_POPULATION_SIZE):
            newPopulation = newPopulation[0:self.INITIAL_POPULATION_SIZE]

        self.population = newPopulation
#



    def createFirstPopulation(self):
        if(len(self.population) == 0):
            self.population.extend(self.generatePopulation(self.INITIAL_POPULATION_SIZE))
            return True
        else:
            return False

    def getBestFitness(self):
        if(len(self.population)== 0):
            return 0
        else:
            return self.population[0].getFitness()

    def evolve(self, evolutionCount):
        fitness = 0
        lastDelta = 0
        for i in range(evolutionCount):
            

            print("Evolution: " + str(i) + " ")

            start_time = time.time()
            self.evolveSingle()
            elapsed_time = time.time() - start_time
            
            if(fitness == self.getBestFitness()):
                lastDelta = lastDelta + 1
            else:
                fitness = self.getBestFitness()
                lastDelta = 0

            print("F: " + str(self.getBestFitness()) + "  ( " + str(lastDelta) + " )   " + str(elapsed_time) + " sec")
            self.counter += 1

    def getBestSolution(self, index):
        if(len(self.population) == 0):
            return Chromosome()
        else:
            return self.population[index]
    
    def generateSingle(self):
        single = Chromosome()
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
        fitness = self.evalFunction(chromosome)
        chromosome.setFitness(fitness)
        return fitness 

    def evaluateAndSort(self, population):
        return sorted(population, key=lambda Ch: self.evaluate(Ch), reverse=True)


    def mutatePopulation(self, population, percentage):
        geneList = []
        for chromo in population:
            geneList.extend(chromo.getChromo())

        index = 0
        chromoIndex = 0
        for gene in geneList:
            percentageTest = random.random()
            if(percentageTest < percentage):
                chromoIndex = int(index / self.chromoSize)
                geneIndex = index % self.chromoSize
                value = population[chromoIndex].getGene(index)
                # print(value)

            
            if(index >= self.chromoSize - 1):
                index = 0
                chromoIndex = chromoIndex + 1
            else:
                index = index + 1
        return population



    # def mutateIndividual(self, individual, percentage):
    #     offspring = Chromosome(individual.getChromo())
    #     usedPositions = []
    #     for i in range(self.chromoSize * percentage):
    #         while True:
    #             position = random.randint(0, self.chromoSize)
    #             if(not position in usedPositions):
    #                 break

    #         gene = offspring.getGene(position)
    #         if(gene == 1):
    #             newGene = 0
    #         elif(gene == 0):
    #             newGene = 1
    #         else:
    #             newGene = 0

    #         offspring.changeGene(newGene, position)
    #     return offspring

    def crossover(self, population, percentage):
        newGeneration = []
        parentPairs = self.rouletteSelectParents(population, self.CROSSOVER_PARENT_PAIR_COUNT)
        for parents in parentPairs:

            # create offspring
            for i in range(self.CROSSOVER_OFFSPRING_COUNT):
                offspring = self.crossoverParents(parents[0], parents[1])
                # limit by breed percentage
                percentageTest = random.random()            
                if(percentageTest < percentage):
                    newGeneration.append(offspring)

                # TODO random chance for pure copy of one parent

        return newGeneration

    def crossoverParents(self, parent1, parent2):
        while True:
            place1 = random.randint(0, self.chromoSize)
            place2 = random.randint(0, self.chromoSize)
            if(place1 > place2):
                break
        
        newChromosome = parent1.chromo[0:place1] + parent2.chromo[place1:place2] + parent1.chromo[place2:self.chromoSize]
        offspring = Chromosome(newChromosome)

        return offspring

    def exportPopulation(self):
        f = open('lastState.txt', 'w')
        outputString = ""
        for chromo in self.population:
            outputString = outputString + chromo.toString() + "\n"
        f.write(outputString[:-1])
        f.close()

    def loadPopulation(self):
        f = open('lastState.txt', 'r')
        population = []
        for line in f:
            single = Chromosome()
            single.fromString(line)
            population.append(single)
        self.population = population
        self.importedGeneration = True

    def checkIfImported(self):
        self.importedGeneration = not self.importedGeneration
        return not self.importedGeneration
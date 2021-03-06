import random
import collections

class Chromosome(object):
	chromo = []
	fitness = None
	def __init__(self, ch = []):
		self.chromo = ch

	def getSize(self):
		return len(self.chromo)

	def getChromo(self):
		return self.chromo
		
	def changeGene(self, singleGene, position):
		self.chromo[position] = singleGene

	def addGene(self, singleGene):
		self.chromo.append(singleGene)

	def getGene(self, position):
		return self.chromo[position]

	def getRandomPositionByGene(self, desiredGene):
		while True:
			randomPosition = random.randint(0, self.getSize() - 1)
			if(self.getGene(randomPosition) == desiredGene):
				return randomPosition

	def equals(self, otherChromosome):
		compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
		return compare(self.chromo, otherChromosome)

	def setFitness(self, fitness):
		self.fitness = fitness

	def getFitness(self):
		return self.fitness

	def toString(self):
		out = ""
		for i in self.chromo:
			out = out + str(i)
		return out

	def fromString(self, chString):
		ch = []
		for i in chString[:-1]:
			ch.append(int(i))
		self.chromo = ch
		print(ch)
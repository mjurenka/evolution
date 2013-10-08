import random
import collections

class Chromosome(object):
	chromo = []
	def __init__(self, ch = []):
		self.chromo = ch

	def getSize(self):
		return len(self.chromo)

	def changeGene(self, singleGene, position):
		self.chromo[position] = singleGene

	def addGene(self, singleGene):
		self.chromo.append(singleGene)

	def getGene(self, position):
		return self.chromo[position]

	def getRandomPositionByGene(self, desiredGene):
		while True:
			randomNumber = random.randint(0, self.getSize() - 1)
			if(self.chromo[randomNumber] == desiredGene):
				break

		return randomNumber

	def countGenes(self, needleGene):
		return self.chromo.count(needleGene)

	def equals(self, otherChromosome):
		compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
		return compare(self.chromo, otherChromosome)
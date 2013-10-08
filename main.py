from classes.evolution import Evolution

if  __name__ =='__main__':
      evolution = Evolution(10, 2013, 2)
      evolution.evolve(1)
      print(evolution.population)
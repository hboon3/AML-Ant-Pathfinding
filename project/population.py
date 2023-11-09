from ant import Ant
import random

class Population:
    def __init__(self, _screen, pop_size, tgt_pos):
        self.screen = _screen
        self.size = pop_size
        self.tgt = tgt_pos
        self.ant_population: list(Ant) = [Ant(_screen, 600, 600, tgt_pos) for _ in range(pop_size)]
    
    def drawall(self):
        for ant in self.ant_population:
            ant.draw()

    def update(self):
        for ant in self.ant_population:
            ant.move()

    def allStopped(self):
        for ant in self.ant_population:
            if not ant.dead():
                return False
            
        return True
    
    def getTopFitness(self):
        topfit = 0.
        for ant in self.ant_population:
            antfit = ant.calculateFitness()
            if antfit > topfit:
                topfit = antfit
        return topfit
    
    def getAverageFitness(self):
        totalfit = 0.
        for ant in self.ant_population:
            totalfit += ant.calculateFitness()
        avgfit = totalfit / len(self.ant_population)
        return avgfit

    def newGeneration(self):
        newgen = []
        topfit = self.getTopFitness()
        for _ in range(len(self.ant_population)):
            a = self.selectAntWithBias(topfit)
            newgen.append(a)
        self.ant_population = newgen

    def selectAntWithBias(self, delta):
        threshold = random.random() * (delta - (random.random() * delta))
        # threshold = random.random(delta - random.random(delta//2))
        for ant in self.ant_population:
            if ant.calculateFitness() > threshold:
                return ant.clone()
            
    def mutate(self):
        for ant in self.ant_population:
            ant.mutate()
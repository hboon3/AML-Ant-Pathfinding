from ant import Ant
import random

class Population:
    def __init__(self, _screen, pop_size, tgt_pos, mut_rate, spread, _t):
        self.screen = _screen
        self.size = pop_size
        self.tgt = tgt_pos
        # NOTE: 600 \ 600 is hardcoded here as this is the screen size designated in main.py
        # Would need to add this as a constructor parameter if we want variable screen sizes
        
        self.ant_population: list(Ant) = [Ant(_screen, 600, 600, tgt_pos, mut_rate, spread, _t) for _ in range(pop_size)]
        self.obstacles = []

    def setTarget(self, t):
        self.tgt = t

    def addObstacle(self, obs):
        self.obstacles.append(obs)

    def drawall(self):
        for ant in self.ant_population:
            ant.draw()

    def checkObstacleWithPosition(self, pos):
        for obst in self.obstacles:
            if obst.registerCollision(pos):
                    return True
        return False
    
    def checkObstacleCollisions(self):
        for obst in self.obstacles:
            for ant in self.ant_population:
                if obst.registerCollision(ant.position):
                    ant.setDead()


    def update(self):
        for obstacle in self.obstacles:
            obstacle.draw()

        for ant in self.ant_population:
            ant.move()
        
        self.checkObstacleCollisions()

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
    
    def getTotalFitness(self):
        return self.getAverageFitness() * len(self.ant_population)

    def countHitTarget(self):
        totalhit = 0
        for ant in self.ant_population:
            if ant.didHit():
                totalhit += 1
        return totalhit

    def newGeneration(self):
        newgen = []
        totalfit = self.getTotalFitness()
        for _ in range(len(self.ant_population)):
            r = random.random() * totalfit
            runningSum = 0.
            for ant in self.ant_population:
                runningSum += ant.calculateFitness()
                if runningSum > r:
                    newgen.append(ant.clone())
                    break
        self.ant_population = newgen

    def selectAntWithBias(self, delta):
        threshold = 0.8*delta
        for ant in self.ant_population:
            if ant.calculateFitness() > threshold:
                return ant.clone()
            
    def mutate(self):
        for ant in self.ant_population:
            ant.mutate()
class Species:
    def __init__(self, genotype, behavior, fitness, niche=None):
        if niche is None:
            niche = []
        self.genotype = genotype
        self.behavior = behavior
        self.fitness = fitness
        self.niche = niche
from instance import Instance
import random

NUM_PARTICLES = 100
NUM_ITERATIONS = 1000

class ParticleIBPSO:
    """Cestica IBPSO algoritma"""
    
    def __init__(self, instance):

        sets, n_vars, n_sets = instance.get()

        # Inicijalizujemo poziciju i memoriju cestice.
        self.instance = instance
        self.dimensions = n_sets
        self.pos = self.rand_bool()
        self.mem_pos = self.pos
        self.mem_fit = instance.fitness(self.pos)
        # ???: Ova promenljiva nije koriscena.
        self.fitness = self.mem_fit

    def get_best(self):
        """Vraca trenutno najbolju poziciju koju je cestica nasla."""
        
        return self.mem_fit, self.mem_pos

    def update_velocity(self):
        """Racuna brzinu u pripremi za sledecu iteraciju."""

        cog_fit, cog_pos = self.get_best()
        social_fit, social_pos = cog_fit, cog_pos

        for neighbor in self.neighbors:
            tmp_fit, tmp_pos = neighbor.get_best()
            if social_fit < tmp_fit:
                social_fit, social_pos = tmp_fit, tmp_pos

        # Racunamo brzinu po slozenoj formuli.
        omega1 = self.rand_bool()
        omega2 = self.rand_bool()

        social_diff = [t[0] != t[1] for t in zip(social_pos, self.pos)]
        social = [t[0] & t[1] for t in zip(omega1, social_diff)]

        cog_diff = [t[0] != t[1] for t in zip(cog_pos, self.pos)]
        cog = [t[0] and t[1] for t in zip(omega2, cog_diff)]

        # Brzina predstavlja bitove koje treba promeniti u sledecoj iteraciji.
        self.velocity = [t[0] or t[1] for t in zip(cog, social)]


    def update(self):
        """Racuna novu poziciju i azurira stanje cestice"""
        new_pos = [t[0] != t[1] for t in zip(self.velocity, self.pos)]
        new_fitness = self.instance.fitness(new_pos)

        self.pos = new_pos
        self.fitness = new_fitness
        
        if new_fitness >= self.fitness:
            self.mem_fit = new_fitness
            self.mem_pos = new_pos
        
        
    def init_neighbors(self, neighbors):
        """Cuva susedne cestice koje su preporucene od algoritma. Podrazumevamo samu cesticu."""

        self.neighbors = neighbors

    def rand_bool(self):
        """Vraca niz slucajnih istinitih vrednosti, potrebno za incijalizaciju pozicije cestica..."""

        # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python#6824868
        return [bool(random.getrandbits(1)) for t in range(self.dimensions)]
    
    

class BPSO:
    """Vrsi algoritam IBPSO za odredjenu instancu."""

    def __init__(self, instance):

        self.instance = instance
        self.particles = [ParticleIBPSO(instance) for t in range(NUM_PARTICLES)]
        
        # Inicijalizujemo komsiluke za prstenastu topologiju.
        for i in range(NUM_PARTICLES):
            self.particles[i].init_neighbors([self.particles[(i-1) % NUM_PARTICLES],
                                              self.particles[(i+1) % NUM_PARTICLES]])

        self.best_pos = None
        self.best_fit = 0

        for p in self.particles:
            self.update_best(p)



    def update_best(self, particle):
        """Azurira najbolje vrednosti ako je cestica bolja od prethodnih."""

        tmp_fit, tmp_pos = particle.get_best()
        if self.best_pos == None or self.best_fit <= tmp_fit:
            self.best_pos = tmp_pos
            self.best_fit = tmp_fit

    def run(self):
        """Izvrsava algoritam za definisanim parametrima."""

        for i in range(NUM_ITERATIONS):
            self.update()

        return self.best_fit, self.best_pos
    
    def update(self):
        """Vrsi iteraciju algoritma."""

        for part in self.particles:
            part.update_velocity()

        for part in self.particles:
            part.update()
            self.update_best(part)

        
            
        
        
    

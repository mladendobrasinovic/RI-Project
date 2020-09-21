from instance import Instance
import random
import math

# NUM_PARTICLES = 484 - Ovo izracunavamo na osnovu velicine problema.
NUM_ITERATIONS = 1000

def rand_bit():
    return bool(random.getrandbits(1))

class ParticleIBPSO:
    """Cestica IBPSO algoritma"""
    
    def __init__(self, instance):

        sets, n_vars, n_sets = instance.get()

        # Inicijalizujemo poziciju i memoriju cestice.
        self.instance = instance
        self.dimensions = n_sets
        self.pos = self.rand_init()
        self.mem_pos = self.pos
        self.mem_fit = instance.fitness(self.pos)
        # ???: Ova promenljiva nije koriscena.
        self.fitness = self.mem_fit
        self.heat = True

    def get_best(self):
        """Vraca trenutno najbolju poziciju koju je cestica nasla."""
        
        return self.mem_fit, self.mem_pos

    def update_velocity(self):
        """Racuna brzinu u pripremi za sledecu iteraciju."""

        cog_fit, cog_pos = self.get_best()
        social_fit, social_pos = cog_fit, cog_pos

        for neighbor in self.neighbors:
            tmp_fit, tmp_pos = neighbor.get_best()
            if social_fit <= tmp_fit:
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

        # Toplota predstavlja potencijal da se cestica poboljsa.
        self.heat = False
        for x in self.neighbors:
            if self.mem_pos != x.mem_pos or self.pos != self.mem_pos:
                self.heat = True


    def update(self):
        """Racuna novu poziciju i azurira stanje cestice"""
        new_pos = [t[0] != t[1] for t in zip(self.velocity, self.pos)]
        new_fitness = self.instance.fitness(new_pos)

        self.pos = new_pos
        self.fitness = new_fitness

        # Ovde je pitanje da li treba prebrisati memoriju ako je jednak novi fitness.
        if new_fitness > self.mem_fit:
            self.mem_fit = new_fitness
            self.mem_pos = new_pos
        
        
    def init_neighbors(self, neighbors):
        """Cuva susedne cestice koje su preporucene od algoritma. Podrazumevamo samu cesticu."""

        self.neighbors = neighbors

    def rand_init(self):
        """Vraca niz slucajnih istinitih vrednosti, potrebno za incijalizaciju pozicije cestica."""
        
        # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python#6824868
        return [rand_bit() and rand_bit() for t in range(self.dimensions)]

    def rand_bool(self):
        """Vraca niz slucajnih istinitih vrednosti, za racunanje brzina."""
        
        # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python#6824868
        return [rand_bit()  for t in range(self.dimensions)]
    
    

class BPSO:
    """Vrsi algoritam IBPSO za odredjenu instancu."""

    def __init__(self, instance):

        self.instance = instance
        sets, n_vars, n_sets = instance.get()
        self.NUM_PARTICLES = 50000
        for i in range(1000):
            if i*i > n_sets * 2:
                self.NUM_PARTICLES = i*i
                self.NUM_PARTICLES_SQRT = i
                break
        
        self.particles = [ParticleIBPSO(instance) for t in range(self.NUM_PARTICLES)]
            
        self.best_pos = None
        self.best_fit = 0

        self.init_topo_neumann()
        # self.init_topo_ring()
        # self.init_topo_gbest()

        for p in self.particles:
            self.update_best(p)


    def init_topo_ring(self):
        """Postavljanje susednosti u skladu sa prstenastom topologijom."""
        
        # Inicijalizujemo komsiluke za prstenastu topologiju.
        for i in range(self.NUM_PARTICLES):
            self.particles[i].init_neighbors([self.particles[(i-1) % self.NUM_PARTICLES],
                                              self.particles[(i+1) % self.NUM_PARTICLES]])

            
    def init_topo_gbest(self):
        """Postavljanje susednosti u skladu sa gbest topologijom."""
        
        for i in range(self.NUM_PARTICLES):
            self.particles[i].init_neighbors(self.particles)

    def init_topo_neumann(self):
        """Postavljanje susednosti u skladu sa Von Nojmanovom topologijom."""

        length = self.NUM_PARTICLES_SQRT

        def clamp(x):
            return x % length

        for t in range(self.NUM_PARTICLES):
            i = t // length
            j = t % length

            tmp = []
            
            tmp.append(self.particles[i*length + clamp(j+1)])
            tmp.append(self.particles[i*length + clamp(j-1)])
            tmp.append(self.particles[clamp(i-1)*length + j])
            tmp.append(self.particles[clamp(i+1)*length + j])

            self.particles[t].init_neighbors(tmp)


    def update_best(self, particle):
        """Azurira najbolje vrednosti ako je cestica bolja od prethodnih."""

        tmp_fit, tmp_pos = particle.get_best()
        if self.best_pos == None or self.best_fit <= tmp_fit:
            self.best_pos = tmp_pos
            self.best_fit = tmp_fit
            


        # Proveravanje da li ima smisla nastaviti algoritam.
        if particle.heat:
            self.heat = True

    def run(self):
        """Izvrsava algoritam za definisanim parametrima."""

        for i in range(NUM_ITERATIONS):
            self.update()
            if i%4 == 0:
                print("{}, {}".format(i, self.best_fit))
            if not self.heat:
                break

        return self.best_fit, self.best_pos
    
    def update(self):
        """Vrsi iteraciju algoritma."""

        for part in self.particles:
            part.update_velocity()

        for part in self.particles:
            self.heat = False
            part.update()
            self.update_best(part)



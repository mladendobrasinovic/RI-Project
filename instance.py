from random import randint

class Instance:
    """Instanca problema maksimalno pakovanje skupova."""
    
    def __init__(self):
        
        self.sets = []
        self.n_vars = 0
        self.n_sets = 0

    def load_delorme(self, filename):
        """Ucitavanje instance dobijene sa https://www.emse.fr/~delorme/SetPacking.html."""
        
        with open(filename, 'r') as file:
            # Ucitavamo instancu u skladu sa opisom datom na sajtu. ???: Validacija se ne radi.
            content = file.readlines()
            self.n_sets, self.n_vars = map(int, content[0].split())

            for ip in range(self.n_sets):
                # Nalazimo liniju koja opisuje skup.
                i = ip * 2 + 3
                # Dodajemo skup na listu skupova.
                self.sets.append(list(map(int, content[i].split())))

    def load_kexu(self, filename):
        """Ucitavanje sa http://sites.nlsde.buaa.edu.cn/~kexu/benchmarks/set-benchmarks.htm"""

        with open(filename, 'r') as file:
            # Sadrzaj datoteke je zasnovan na ASCII DIMACS formatu.
            content = file.readlines()
            lines = list(map(str.split, content))
            
            c = 0
            while True:
                if lines[c][0] == 'p':
                    break
                else:
                    c += 1
                    continue

            # Ucitavanje podataka o broju promenljivih i skupova.
            self.n_vars, self.n_sets = map(int, lines[c][2:])

            for i in range(c+1, c+1+self.n_sets):
                self.sets.append(list(map(int, lines[i][1:])))

    def fitness(self, candidate):
        """Racuna pogodnost tako da su neprihvatljive cestice kaznjavane za broj preklapanja."""
        
        candidate_cover = dict()
        size = 0
        badness = 0

        for i in range(len(candidate)):
            if candidate[i]:
                # Brojimo skupove i dodajemo clanove skupova kandidatu za pokrivac.
                for el in self.sets[i]:
                    if el not in candidate_cover:
                        candidate_cover[el] = 0
                    else:
                        candidate_cover[el] += 1
                        badness += 1
                size += 1

        if badness == 0:
            return size
        else:
            return -badness
        
                
    def get(self):
        """Vraca trenutnu instancu."""
        
        return self.sets, self.n_vars, self.n_sets
    
    def monte_carlo(self, tries=-1):
        """Rad Monte-Karlo metode zasnovane na permutacijama"""

        if tries == -1:
            tries = self.n_sets

        max_result = 0
        # rng = random.SystemRandom()
        
        for i in range(tries):
            cover = []
            cover_sets = []
            failed = False
            result = 0
            while not failed and not result >= self.n_sets:
                success = False
                while not success:
                    new_set = randint(0, self.n_sets - 1)
                    if not new_set in cover_sets:
                        set_vars = self.sets[new_set]
                        if set(set_vars).intersection(set(cover)) != set():
                            failed = True
                            break
                        
                        cover += self.sets[new_set]
                        cover_sets.append(new_set)
                        result += 1
                        if result >= max_result:
                            max_result = result
                            
                        success = True
                        
        return max_result

    def __str__(self):
        
        string = 'Broj skupova: {}, broj promenljivih: {}\n'.format(self.n_sets, self.n_vars)
        for constraint in self.sets:
            string += '\n' + str(constraint)

        print(str(self.sets))
        return string
    

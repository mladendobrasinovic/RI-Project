from random import randint

class Instance:
    """Instanca problema maksimalno pakovanje skupova."""
    
    def __init__(self):
        
        self.sets = []
        self.n_vars = 0
        self.n_sets = 0

    def load_delorme(self, filename):
        """Ucitavanje instance dobijena sa https://www.emse.fr/~delorme/SetPacking.html."""
        
        with open(filename, 'r') as file:
            # Ucitavamo instancu u skladu sa opisom datom na sajtu. ???: Validacija se ne radi.
            content = file.readlines()
            self.n_sets, self.n_vars = map(int, content[0].split())

            for ip in range(self.n_sets):
                # Nalazimo liniju koja opisuje skup.
                i = ip * 2 + 3
                # Dodajemo skup na listu skupova.
                self.sets.append(list(map(int, content[i].split())))

    def fitness(self, candidate):
        """Racuna pogodnost tako da su neprihvatljive cestice kaznjavane za broj preklapanja."""
        
        candidate_cover = list()
        size = 0

        for i in range(len(candidate)):
            if candidate[i]:
                # Brojimo i dodajemo clanove seta kandidatu za pokrivac.
                candidate_cover = self.sets[i] + candidate_cover
                size += 1

        badness = len(candidate_cover) - len(set(candidate_cover))
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
    

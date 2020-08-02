import os
from bpso import BPSO
from instance import Instance


if __name__ == "__main__":
    
    # Ucitavanje instanci.
    inst_files = os.listdir('./instances')
    inst_names = [fname[0:len(fname) - 6] for fname in inst_files]

    # Testiranje klase instance.
    inst = Instance()
    inst.load_delorme("./instances/" + inst_files[8])

    algorithm = BPSO(inst)
    fit, pos = algorithm.run()

    print(fit, pos)
    # print(inst.monte_carlo(10000))
    # print(inst_names)
    # print(inst)

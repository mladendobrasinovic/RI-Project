import os
from bpso import BPSO
from instance import Instance
import sys

def test_kexu():
    
    inst_files = os.listdir('./frb30-15-msc')
    inst = Instance()
    inst.load_kexu("./frb30-15-msc/" + inst_files[0])

    algorithm = BPSO(inst)
    fit, pos = algorithm.run()

    print(fit)
    print(pos)

def test_delorme():
    
    inst_files = os.listdir('./instances')
    inst_names = [fname[0:len(fname) - 6] for fname in inst_files]

    #Testiranje klase instance.
    inst = Instance()
    #inst.load_delorme("./instances/" + inst_files[8])
    #20
    inst.load_delorme("./instances/" + inst_files[22])

    algorithm = BPSO(inst)
    fit, pos = algorithm.run()

    print(fit)
    print(pos)

if __name__ == "__main__":
    
    # Ucitavanje instanci.

    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        test_delorme()
    else:
        test_kexu()
    
    # print(inst.monte_carlo(10000000))

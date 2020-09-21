import os
from bpso import BPSO
from instance import Instance
import sys

def test_kexu():
    
    inst_files = os.listdir('./frb30-15-msc')
    inst = Instance()
    inst.load_kexu("./frb30-15-msc/" + inst_files[0])

    return inst

def test_delorme():
    
    inst_files = os.listdir('./instances')
    inst_names = [fname[0:len(fname) - 6] for fname in inst_files]

    #Testiranje klase instance.
    inst = Instance()
    # 8 
    #inst.load_delorme("./instances/" + inst_files[8])
    #20, 22
    inst.load_delorme("./instances/" + inst_files[13])

    # algorithm = BPSO(inst)
    # fit, pos = algorithm.run()

    return inst



if __name__ == "__main__":
    
    # Ucitavanje instanci.

    inst = 0
    bpso_flag = True
    delorme_flag = False
    generate_flag = False
    
    if len(sys.argv) == 2 and sys.argv[1][0] == '-':
        if 'd' in sys.argv[1]:
            delorme_flag = True
        if 'f' in sys.argv[1]:
            bpso_flag = False
        if 'g' in sys.argv[1]:
            generate_flag = True

    if delorme_flag:
        inst = test_delorme()
    elif generate_flag:
        inst = Instance()
        inst.generate(50, 50, 4, 2)
    else:
        inst = test_kexu()

    if bpso_flag:
        algorithm = BPSO(inst)
        fit, pos = algorithm.run()
        
        print(fit)
        print(pos)

        # print(inst.brute_force())    

    else:
        # print(inst.brute_force())        
    
        print(inst.monte_carlo(1000000))

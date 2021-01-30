import os
from bpso import BPSO
from instance import Instance
import sys
import time
import json

def test_kexu(target):
    
    inst_files = os.listdir('./frb30-15-msc')
    inst_names = [fname[0:len(fname) - 4] for fname in inst_files]
    inst = Instance()
    inst.load_kexu("./frb30-15-msc/" + inst_files[target])

    return (inst, inst_names[target])

def test_delorme(target):
    
    inst_files = os.listdir('./instances')
    inst_names = [fname[0:len(fname) - 6] for fname in inst_files]

    #Testiranje klase instance.
    inst = Instance()
    # 8 
    #inst.load_delorme("./instances/" + inst_files[8])
    #20, 22
    # 13
    inst.load_delorme("./instances/" + inst_files[target])

    return (inst, inst_names[target])

def test_generated(target):
    
    inst_files = os.listdir('./generated')
    inst_names = [fname[0:len(fname)] for fname in inst_files]

    # Testiranje klase instance.
    inst = Instance()
    inst.load_delorme("./generated/" + inst_files[target])

    return (inst, inst_names[target])

if __name__ == "__main__":
    
    # Ucitavanje instanci.

    inst = 0
    method = 0
    bpso_flag = False
    monte_flag = False
    brute_flag = False
    delorme_flag = False
    kexu_flag = False
    self_flag = False
    generate_flag = False
    low_flag = False
    
    if len(sys.argv) >= 2 and sys.argv[1][0] == '-':
        if 'd' in sys.argv[1]:
            delorme_flag = True
        if 'k' in sys.argv[1]:
            kexu_flag = True
        if 'g' in sys.argv[1]:
            generate_flag = True
        if 'l' in sys.argv[1]:
            low_flag = True
        if 'b' in sys.argv[1]:
            bpso_flag = True
            method = "_ibpso"
        if 's' in sys.argv[1]:
            self_flag = True
        if 'f' in sys.argv[1]:
            brute_flag = True
            method = "_brute"
        if 'm' in sys.argv[1]:
            monte_flag = True
            method = "_monte"

    if generate_flag:
        target = sys.argv[2]
    else:
        target = int(sys.argv[2])

    name = 0
    if delorme_flag:
        inst, name = test_delorme(target)
    elif generate_flag:
        inst, name = Instance()
        if low_flag:
            inst.generate(30, 30, 4, 2)
        else:
            inst.generate(50, 50, 4, 2)
        inst.write_delorme(target)
        inst.load_delorme("generated/" + target)
    elif self_flag:
        inst, name = test_generated(target)
    else:
        inst, name = test_kexu(target)

    # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
    if not generate_flag:
        start_time  = time.time()
        
        if bpso_flag:
            algorithm = BPSO(inst)
            fit, pos = algorithm.run()
        
            print(fit)
            print(pos)

        if brute_flag:
            fit = inst.brute_force()
            print(fit)   

        if monte_flag:
            fit = inst.monte_carlo(1000000)
            print(fit)

        time_to_fit = time.time() - start_time
        print(time_to_fit)
        print(name)
        text = json.dumps([fit, time_to_fit])
        with open("results/" + name + method, 'w') as file:

            file.write(text)

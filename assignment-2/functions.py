import numpy as np
import pcoding

def BEC_channel_output(x, erasure):

    y = []
    for i in range(len(x)):
        e = np.random.binomial(1, erasure)
        if(e==1): y.append(-1) # erasure
        else: y.append(x[i])
    
    return np.asarray(y)

def capacity_BEC(erasure):
    return 1-erasure


def simulation(num_exp, erasure, blocklength, rate):

    info_bits = blocklength*rate

    for i in range(num_exp):
        x = list(np.random.randint(0, 2, int(info_bits)))
        x_ = pcoding.full_pass(x, erasure, blocklength)

        # print(x)
        # print(x_)
        print(x==x_)
    
    return None


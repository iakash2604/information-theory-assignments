import numpy as np
import pcoding
import random
from matplotlib import pyplot as plt


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
    correct=0
    ber=0
    info_bits = blocklength*rate

    for i in range(num_exp):
        x = list(np.random.randint(0, 2, int(info_bits)))
        x_ = pcoding.full_pass(x, erasure, blocklength)

        result = (x==x_)
        if(result): correct=correct+1

        if(x_==-1): ber=ber+1
    
    print("N = ", blocklength)
    print("accurate recovery: ", correct/num_exp)
    print("bit erasure rate: ", ber/num_exp)
    print("")

    return ber/num_exp, correct/num_exp

def mutual_info_BEC(blocklength, erasure):
    
    z_vector = pcoding.z_bec(erasure, blocklength)
    for i, z in enumerate(z_vector):
        z_vector[i] = 1-z
    
    return z_vector

def scatter_plot(y, i):
    x = np.arange(len(y))
    plt.scatter(x, y, s=5)
    # plt.show()
    plt.savefig("scatter_"+str(i)+".png")
    plt.clf()
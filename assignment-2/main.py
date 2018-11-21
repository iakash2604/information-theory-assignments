import numpy as np
import pcoding
import functions
import random
from matplotlib import pyplot as plt


erasure = 0.5
blocklength = 2**1
rate = 0.4
num_exp = 50

bers = []
cors = []
erasures = [0, 0.3, 0.5, 1]
# for i in range(1, 12):
for i, erasure in enumerate(erasures):
    # ber, cor = functions.simulation(num_exp, erasure, 2**i, rate)
    # cors.append(cor)
    # bers.append(ber)

    mi = functions.mutual_info_BEC(2**11, erasure)
    functions.scatter_plot(mi, i)
    ones = 0
    for m in mi:
        if(np.round(m)==1): ones=ones+1
    print ("fraction of channels with MI close to 1: ", ones/len(mi))

# cors = np.asarray(cors)
# bers = np.asarray(bers)
# x = np.arange(len(bers))
# plt.plot(x, bers, cors)
# plt.savefig("bers.png")

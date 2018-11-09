import math
import numpy as np
from variables import *
from random import randint

def decoder(y, codebook):

    decoded_index = []
    num_codewords = len(codebook)

    for i in range(num_codewords):
        codeword = codebook[i]
        temp = -h_XY
        for j in range(n):
            prob = 0
            if(codeword[j]==y[j]): prob = (1-a)*0.5
            else: prob = a*0.5
            temp = temp - math.log(prob, 2)/n

            if(float(np.abs(temp))>e): continue
            else: decoded_index.append(i)
    
    return decoded_index

def bsc_output(a, x):
    """
    a is the transition probability 
    x is the input sequence
    """
    y = []
    transitions = list(np.random.binomial(size=len(x), n=1, p= a))
    for i in range(len(x)):
        if(transitions[i]==1): y.append(1-x[i])
        else: y.append(x[i])
    return y

def generate_codebook(R, n):
    codebook = []
    num_words = math.ceil(math.pow(2, (n*R)))

    for i in range(num_words):
        codebook.append(list(np.random.binomial(size=n, n=1, p=p_X)))
    return codebook

def channel_experiment(codebook):
    errors = 0
    undecoded = 0
    num_words = len(codebook)

    for i in range(num_experiments):
        index = randint(0, num_words-1)
        x = codebook[index]
        y = bsc_output(a, x)
        decoded_index = decoder(y, codebook)

        if(len(decoded_index)!=1):
            errors = errors + 1
            undecoded = undecoded + 1
            continue
        
        if(len(decoded_index)==1 and decoded_index[0]!=index):
            errors = errors + 1

    results = []
    results.append(errors)
    results.append(undecoded)

    return results

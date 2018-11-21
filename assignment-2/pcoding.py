import numpy as np
from functions import *
def x2u(x):
    blocklength = len(x)
    n = np.log2(blocklength)
    base = np.asarray([[1, 0], [1, 1]])
    generator = base
    for i in range(n-1):
        generator = np.kron(generator, base)

    return np.dot(x, generator)

def u2x(u):
    blocklength = len(u)
    n = np.log2(blocklength)
    base = np.asarray([[1, 1], [0, 1]])
    generator = base
    for i in range(n-1):
        generator = np.kron(generator, base)

    return np.dot(u, generator)

def z_bec(erasure, blocklength):
    # finds the bhattacharyya parameters for all the channels produced
     
    z_vector = [erasure]

    for i in range(int(np.log2(blocklength))):
        z_prev = z_vector
        z_vector = []

        for z in z_prev:
            z_vector.append(2*z-z**2)
            z_vector.append(z**2)
    
    return z_vector

def find_good_channels(z_vector, k):
    # returns the indices of the smallest k elements in the z_vector
    # these are the high capacity channels. 

    top_channel_indices = np.argsort(z_vector)[:k]
    top_channel_indices.sort()
    return top_channel_indices
    
def encoding(blocklength, good_channels, x):

    encoded = [0]*blocklength
    for i, z in enumerate(good_channels):
        encoded[int(z)] = x[i]

    return encoded

def decoding(y, good_channels):
    
    blocklength = len(y)
    decoded = [0]*blocklength

    for i in range(len(good_channels)):
        genie = decoded[:good_channels[i]]
        lr_i = likelihood_ratio(y, genie, good_channels[i])
        decoded_i = lookup(lr_i)
        decoded[good_channels[i]] = decoded_i

        if(decoded_i == -1):
            return None

    decoded_info_bits = []
    for i in good_channels:
        decoded_info_bits.append(decoded[i])
    
    return decoded_info_bits
        
def likelihood_ratio(y, genie, i):
    # y is the output of BEC
    # genie is the prev decoded u 
    # i is the index of the channel at which decoding needs to be done 

    blocklength = len(y)

    if(blocklength==1):
        if(y[0]==0):
            return np.inf
        if(y[0]==1):
            return 0
        if(y[0]==-1):
            # erasure
            return 1
    
    if((i+1)%2==1):
        genie_odd = []
        genie_even = []
        for j in range(int(i+1)-1):
            if((j+1)%2==0):
                genie_even.append(genie[j])
            else:
                genie_odd.append(genie[j])
        
        genie_mod_2 = []
        for j in range(len(genie_even)):
            genie_mod_2.append((genie_even[j]+genie_odd[j])%2)

        L1 = likelihood_ratio(y[:int(blocklength/2)], genie_mod_2, i/2)
        L2 = likelihood_ratio(y[int(blocklength/2):], genie_even, i/2)

        if((L1 == 0 and L2 == 0) or ((not np.isfinite(L1)) and (not np.isfinite(L2)))):
            return np.inf
        if((L1 == 0 and (not np.isfinite(L2))) or ((not np.isfinite(L1)) and L2 == 0)):
            return 0
        if((L1 == 1 and (not np.isfinite(L2))) or ((not np.isfinite(L1)) and L2 == 1)):
            return 1
        else:
            return (L1*L2 + 1)/(L1+L2)
    
    else:
        genie_odd = []
        genie_even = []
        for j in range(int(i+1)-2):
            if((j+1)%2==0):
                genie_even.append(genie[j])
            else:
                genie_odd.append(genie[j])

        genie_mod_2 = []
        for j in range(len(genie_even)):
            genie_mod_2.append((genie_even[j]+genie_odd[j])%2)

        L1 = likelihood_ratio(y[:int(blocklength/2)], genie_mod_2, (i-1)/2)
        L2 = likelihood_ratio(y[int(blocklength/2):], genie_even, (i-1)/2)

        if(genie[-1]==0):
            return L2*L1
        else:
            if(L1!=0):
                return L2/L1
            else:
                return np.inf

def lookup(lr):        
                
    if(lr == 0):
        return 1
    if(not np.isfinite(lr)):
        return 0
    if(lr == 1):
        return -1
    
def full_pass(x, erasure, blocklength):
    
    info_bits = len(x)
    z_vector = z_bec(erasure, blocklength)
    good_channels = find_good_channels(z_vector, info_bits)
    encoded_input = encoding(blocklength, good_channels, x)
    output_bec = BEC_channel_output(encoded_input, erasure)
    decoded_output = decoding(output_bec, good_channels)
    
    if(decoded_output!=None):
        return list(decoded_output)
    
    else:
        return -1
        print("cant decode")



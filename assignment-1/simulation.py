from functions import *
from variables import *

codebook = generate_codebook(R, n)

results = channel_experiment(codebook)
errors = results[0]
undecoded = results[1]

print (errors/num_experiments)
print (undecoded/num_experiments)
    





import matplotlib.pyplot as plt
import collections
import numpy as np
import operator

with open('rating.txt', 'r') as f:
    rating = f.read().split()

dict = {}
for i in rating:
    if i in dict:
        dict[i] += 1
    else:
        dict[i] = 1
print(dict)
maxs = []
max_value2 = max(dict.values());  {key for key, value in dict.items() if value == max_value2}
file = open('names.txt', 'r')
for k, v in dict.items():
        if v == max_value2:
            maxs.append(k)
for item in maxs:
    text = open('names.txt', 'r').readlines()[int(item) - 1]
    print('Победитель', text)
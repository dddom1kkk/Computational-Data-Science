import time
import pandas as pd
import numpy as np
from implementations import all_implementations

data = pd.DataFrame(columns=['algorithm', 'size', 'time'])

sizes = [2500, 10000, 20000]
for size in sizes:
    random_array = np.random.randint(0, 10001, size=size)
    for sort in all_implementations:
        total = 0
        for i in range(100):
            st = time.time()
            res = sort(random_array)
            en = time.time()
            data.loc[len(data.index)] = [sort.__name__, size, en - st]

data.to_csv('data.csv', index=False)
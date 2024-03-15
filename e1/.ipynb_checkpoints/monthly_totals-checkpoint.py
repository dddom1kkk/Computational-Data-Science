import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame ({'a': [2, 3, 4, 5, 6], 'b': [1.0, 2.0, 3.0, 4.0, 1.0]})
print(df['a'] + df['b'])
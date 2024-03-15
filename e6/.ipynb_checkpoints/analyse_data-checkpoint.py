import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

alg1 = data[data['algorithm'].str.contains('qs1')]
alg2 = data[data['algorithm'].str.contains('qs2')]
alg3 = data[data['algorithm'].str.contains('qs3')]
alg4 = data[data['algorithm'].str.contains('qs4')]
alg5 = data[data['algorithm'].str.contains('qs5')]
alg6 = data[data['algorithm'].str.contains('merge1')]
alg7 = data[data['algorithm'].str.contains('partition_sort')]

anova = f_oneway(alg1['time'], alg2['time'], alg3['time'], alg4['time'], alg5['time'], alg6['time'], alg7['time'])

posthoc = pairwise_tukeyhsd(data['time'], data['algorithm'], alpha=0.05)

print('ANOVA test (comparing all means with alpha = 0.05): ', anova.pvalue)
print(posthoc)
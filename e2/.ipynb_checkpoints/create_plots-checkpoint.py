import sys
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

filedata1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
filedata2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])

filesorted1 = filedata1.sort_values(by='views', ascending=False)

mergedata = pd.merge(filedata1, filedata2, left_index=True, right_index=True)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Popularity Distribution')
plt.xlabel('Rank')
plt.ylabel('Views')
plt.plot(filesorted1['views'].values)
plt.subplot(1, 2, 2)
plt.title('Hourly Correlation')
plt.xlabel('Hour 1 views')
plt.ylabel('Hour 2 views')
plt.scatter(mergedata['views_x'], mergedata['views_y'])
plt.xscale('log')
plt.yscale('log')
plt.savefig('wikipedia.png')
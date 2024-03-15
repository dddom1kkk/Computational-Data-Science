import pandas as pd
import sys
from difflib import *

def find_matches(title):
    match = get_close_matches(title, data['title'].tolist(), n=1, cutoff=0.6)
    return match[0] if match else None

filename = sys.argv[2]
with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

ratings = pd.read_csv(filename)

data = pd.DataFrame(lines, columns=['trash'])
print(data)
data['title'] = data['trash'].str.strip()
data = data.drop('trash', axis=1)

ratings['matching'] = ratings['title'].apply(find_matches)

ratings = ratings.drop('title', axis=1)

ratings = ratings.dropna()
ratings = ratings.groupby(by=["matching"]).mean()
ratings = ratings.round(2)
ratings = ratings.reset_index()
ratings = ratings.rename(columns={'matching': 'title'})

ratings.to_csv(sys.argv[3], index=False)
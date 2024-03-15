import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

city_sum = totals.sum(axis=1)

print("City with lowest total precipitation:")
print(city_sum.idxmin())

month_sum = totals.sum(axis=0)
mdays_count = counts.sum(axis=0)

print("Average precipitation in each month:")
print(month_sum.divide(mdays_count))

cdays_count = counts.sum(axis=1)

print("Average precipitation in each city:")
print(city_sum.divide(cdays_count))
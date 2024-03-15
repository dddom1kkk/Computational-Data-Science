import numpy as np

data = np.load('monthdata.npz')

totals = data['totals']
counts = data['counts']

prec_city_sum = np.sum(totals, axis=1) # sums all the rows and creates array of row sums
print("Row with lowest total precipitation:")
print(np.argmin(prec_city_sum))

prec_month_sum = np.sum(totals, axis=0)
month_days_sum = np.sum(counts, axis=0)

print("Average precipitation in each month:")
print(np.divide(prec_month_sum, month_days_sum))

city_days_sum = np.sum(counts, axis=1)

print("Average precipitation in each city:")
print(np.divide(prec_city_sum, city_days_sum))

row, column = np.shape(totals)

reshaped_totals = np.reshape(totals, (4*row, 3))

sum_reshaped = np.sum(reshaped_totals, axis=1)

print("Quarterly precipitation totals:")
print(np.reshape(sum_reshaped, (row, column//3)))
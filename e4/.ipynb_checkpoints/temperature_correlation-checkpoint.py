import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dist_formula(lat1, lon1, lat2, lon2):
    r = 6371 # meters
    a = np.sin(((lat2 - lat1) * (np.pi / 180)) / 2) * np.sin(((lat2 - lat1) * (np.pi / 180)) / 2) + np.cos(lat1 * (np.pi / 180)) * np.cos(lat2 * (np.pi / 180)) * np.sin(((lon2 - lon1) * (np.pi / 180)) / 2) * np.sin(((lon2 - lon1) * (np.pi / 180)) / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return r * c

def distance(city, stations):
    all_dists = dist_formula(city['latitude'], city['longitude'], stations['latitude'], stations['longitude'])
    return all_dists

def best_tmax(city, stations):
    dists = distance(city, stations)
    dists_series = pd.Series(dists)
    idx_min = dists_series.idxmin()
    return stations.iloc[idx_min]['avg_tmax']

def main():
    stations = pd.read_json(sys.argv[1], lines=True)
    cities = pd.read_csv(sys.argv[2])

    stations['avg_tmax'] = stations['avg_tmax'].div(10)

    cities = cities.dropna()
    cities['area'] = cities['area'].div(1000000)
    cities = cities[(cities['area'] < 10000)]
    
    cities['best_tmax'] = cities.apply(best_tmax, stations=stations, axis=1)
    cities['density'] = cities['population'] / cities['area']
    
    plt.scatter(cities['best_tmax'], cities['density'])
    plt.title('Temperature vs Population Density')
    plt.xlabel('Avg Max Temperature (\u00b0C)')
    plt.ylabel('Population Density (people/km\u00b2)')
    plt.savefig(sys.argv[3])
    
if __name__ == '__main__':
    main()
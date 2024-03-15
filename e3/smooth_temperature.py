import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

filename = sys.argv[1]

cpu_data = pd.read_csv(filename, parse_dates=['timestamp'])

loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=0.03)

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([1, 1, 1, 1]) ** 2
transition_covariance = np.diag([0.01, 0.004, 0.004, 0.004]) ** 2
transition = [[0.95,0.5,0.4,-0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]]

kf = KalmanFilter(transition_matrices=transition, initial_state_mean=initial_state, observation_covariance=observation_covariance, transition_covariance=transition_covariance)
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['Temperature Sensor readings','LOESS Smoothing Signal','Kalman Smoothing Signal'])
plt.xlabel('Timestamp')
plt.ylabel('CPU Temperature')
plt.savefig('cpu.svg')
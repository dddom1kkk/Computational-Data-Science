import sys
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
from pykalman import KalmanFilter

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def dist_formula(lat1, lon1, lat2, lon2):
    r = 6371000 # meters
    a = np.sin(((lat2 - lat1) * (np.pi / 180)) / 2) * np.sin(((lat2 - lat1) * (np.pi / 180)) / 2) + np.cos(lat1 * (np.pi / 180)) * np.cos(lat2 * (np.pi / 180)) * np.sin(((lon2 - lon1) * (np.pi / 180)) / 2) * np.sin(((lon2 - lon1) * (np.pi / 180)) / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return r * c

def distance(data):
    all_dist = dist_formula(data['lat'], data['lon'], data['lat'].shift(-1), data['lon'].shift(-1))
    return np.nansum(all_dist)

def smooth(data):
    trans = 10 / (10 ** 5) # position error
    obs = 17.5 / (10 ** 5) # measurement error
    
    transition_covariance = np.diag([trans,trans]) ** 2
    observation_covariance = np.diag([obs,obs]) ** 2
    
    kf = KalmanFilter(transition_matrices=[[1, 0], [0, 1]],initial_state_mean=data.iloc[0],transition_covariance=transition_covariance,observation_covariance=observation_covariance)
    
    kalman_smoothed, _ = kf.smooth(data)
    
    return pd.DataFrame(kalman_smoothed, columns=['lat', 'lon'])
    
def main():    
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    namespace = {'default': 'http://www.topografix.com/GPX/1/0'}

    points = pd.DataFrame([{'lat': float(trkpt.get('lat')), 'lon': float(trkpt.get('lon'))} for trkpt in root.findall('.//default:trkpt', namespace)])
    
    print('Unfiltered distance: %0.2f' % (distance(points)))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points)))
    output_gpx(smoothed_points, 'out.gpx')
    
if __name__ == '__main__':
    main()
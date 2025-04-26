from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

_logger = logging.getLogger(__name__)

def detect_outliers(taxi_rides_data: pd.DataFrame) -> (pd.DataFrame, dict):
    raw_data = taxi_rides_data

    data = pd.DataFrame()
    data['ride_dist'] = raw_data['trip_distance']
    raw_data['tpep_pickup_datetime'] = pd.to_datetime(raw_data['tpep_pickup_datetime'])
    raw_data['tpep_dropoff_datetime'] = pd.to_datetime(raw_data['tpep_dropoff_datetime'])
    data['ride_time'] = (raw_data['tpep_dropoff_datetime'] - raw_data['tpep_pickup_datetime']).dt.total_seconds()
    data['date'] = raw_data['tpep_pickup_datetime'].dt.date
    data['ride_id'] = raw_data.index

    X = data[['ride_dist', 'ride_time']]
    results = _cluster_and_label(X, create_and_show_plot=False)
    data['label'] = results['labels']

    outliers = data[data['label'] == -1]
    _logger.debug('Found %d outliers' % len(outliers))
    del results['labels']
    return outliers.drop(columns=['label']), results


def _cluster_and_label(X, create_and_show_plot=True):
    X = StandardScaler().fit_transform(X)
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)

    # Find labels from the clustering
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    _logger.debug('Estimated number of clusters: %d' % n_clusters_)
    _logger.debug('Estimated number of noise points: %d' % n_noise_)
    #logger.debug("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    #logger.debug("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    #logger.debug("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    #logger.debug("Adjusted Rand Index: %0.3f"
    #      % metrics.adjusted_rand_score(labels_true, labels))
    #logger.debug("Adjusted Mutual Information: %0.3f"
    #      % metrics.adjusted_mutual_info_score(labels_true, labels))
    _logger.debug("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, labels))

    run_metadata = {
        'nClusters': n_clusters_,
        'nNoise': n_noise_,
        'silhouetteCoefficient': metrics.silhouette_score(X, labels),
        'labels': labels,
    }
    if create_and_show_plot == True:
        fig = plt.figure(figsize=(10,10))
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = [plt.cm.cool(each)
                  for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]
            class_member_mask = (labels== k)
            xy = X[class_member_mask & core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                     markeredgecolor='k', markersize=14)
            xy = X[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], '^', markerfacecolor=tuple(col),
                     markeredgecolor='k', markersize=14)
            
        plt.xlabel('Standard Scaled Ride Dist.')
        plt.ylabel('Standard Scaled Ride Time')
        plt.title('Estimated number of clusters: %d' % n_clusters_)
        plt.show()
    else:
        pass
    return run_metadata
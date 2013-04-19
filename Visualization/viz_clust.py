# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import numpy as np
import pylab as pl
import matplotlib.cm as cm

from sklearn.utils import shuffle
from sklearn.utils import check_random_state
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans

random_state = np.random.RandomState(0)

n_clusters = 6


def make_data(file):
    return np.genfromtxt(file, delimiter = ',')

# Part 2: Qualitative visual inspection of the convergence

X = make_data("data.csv")
km = MiniBatchKMeans(k=n_clusters, init='random', n_init=10,
                     random_state=random_state).fit(X)

print km.labels_	 

fig = pl.figure()
for k in range(n_clusters):
    my_members = km.labels_ == k
    color = cm.spectral(float(k) / n_clusters, 1)
    pl.plot(X[my_members, 0], X[my_members, 1], 'o', marker='.', c=color)
    cluster_center = km.cluster_centers_[k]
    pl.plot(cluster_center[0], cluster_center[1], 'o',
            markerfacecolor=color, markeredgecolor='k', markersize=6)
    pl.title("Example cluster allocation with a single random init\n"
             "with MiniBatchKMeans")

pl.show()
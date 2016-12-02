# This script conducts various types of clustering on generated data.

################
# IMPORT MODULES
################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans

###############
# GENERATE DATA
###############
# This section generates the data that will be clustered.

# Set random seed for reproducibility.
np.random.seed(seed = 12346)

# Create small and large squares of data.
small_rectangle = pd.DataFrame(data = {'x': np.random.uniform(low = -1,
                                                              high = 1,
                                                              size = 500),
                                       'y': np.random.uniform(low = -1,
                                                              high = 1,
                                                              size = 500)})
large_rectangle = pd.DataFrame(data = {'x': np.random.uniform(low = -5,
                                                              high = 5,
                                                              size = 1000),
                                       'y': np.random.uniform(low = -5,
                                                              high = 5,
                                                              size = 1000)})

# Remove most of the points in the interior of the rectangles.
# The remaining points will be around the borders.
small_rectangle = small_rectangle[(small_rectangle.x.abs() > 0.75) | (small_rectangle.y.abs() > 0.75)]                        
large_rectangle = large_rectangle[(large_rectangle.x.abs() > 4) | (large_rectangle.y.abs() > 4)]

# Combine data and reset index.
all_data = pd.concat([small_rectangle, large_rectangle])

# Set style for plots.
style.use('ggplot')

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add scatter plot data.
plt.scatter(all_data.x,
            all_data.y,
            color = 'black')

# Set plot and axes titles.
plt.title('Data Points')
plt.xlabel('x')
plt.ylabel('y')

# Show plot.
plt.show()

# Scale 'all_data'.
all_data_scaled = scale(all_data)

##############################
# DETERMINE NUMBER OF CLUSTERS
##############################
# This section finds optimal number of clusters according to some common metrics.
# Results vary widely and are not always helpful.
# For the clustering algorithms below, I will use 2 clusters when possible.

# TBA

###################
# KMEANS CLUSTERING
###################
# This section conducts k-means clustering with 2 clusters.
# I couldn't find a way to check cluster stability, but...
# This implementation is slightly different from the kmeans I run in the R branch.
# It runs kmeans 10 (can be changed with 'n_init' parameter) times and uses the best result
# according to some metric.
# In my view, this somewhat removes the need for checking cluster stability,
# since I'm using the best clustering result found in 'n_init' runs.

# Conduct k-means clustering with 2 clusters.
kmeans = KMeans(n_clusters = 2,
                random_state = 12346).fit(all_data_scaled)

# Get scaled cluster centers.
kmeans_centers = pd.DataFrame(kmeans.cluster_centers_)
kmeans_centers.columns = ['x', 'y']

# Unscale 'kmeans_centers' and view unscaled cluster centers.
kmeans_centers.x = (kmeans_centers.x * all_data.x.std(ddof = 0)) + all_data.x.mean()
kmeans_centers.y = (kmeans_centers.y * all_data.y.std(ddof = 0)) + all_data.y.mean()
kmeans_centers

# Add cluster labels to 'all_data'.
all_data['kmeans_clusters'] = kmeans.labels_

# View cluster sizes.
all_data.kmeans_clusters.value_counts()

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add scatter plot data, 1 cluster at a time.
plt.scatter(all_data[all_data.kmeans_clusters == 0].x,
            all_data[all_data.kmeans_clusters == 0].y,
            color = 'red')
plt.scatter(all_data[all_data.kmeans_clusters == 1].x,
            all_data[all_data.kmeans_clusters == 1].y,
            color = 'blue')

# Add cluster centers.
plt.text(x = kmeans_centers.x[0],
         y = kmeans_centers.y[0],
         s = 'C1',
         fontsize = 15)
plt.text(x = kmeans_centers.x[1],
         y = kmeans_centers.y[1],
         s = 'C2',
         fontsize = 15)

# Set plot and axes titles.
plt.title('Kmeans Clustering Result')
plt.xlabel('x')
plt.ylabel('y')

# Show plot.
plt.show()

#########################
# HIERARCHICAL CLUSTERING
#########################
# This section conducts hierarchical clustering with 2 clusters.

##########################################
# EXPECTATION MAXIMIZATION (EM) CLUSTERING
##########################################
# This section conducts EM clustering with 2 clusters.

#####################
# SPECTRAL CLUSTERING
#####################
# This section conducts spectral clustering with 2 clusters.

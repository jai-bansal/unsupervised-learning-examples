# This script conducts various types of clustering on generated data.

################
# IMPORT MODULES
################
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabaz_score
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.preprocessing import scale
from sklearn import mixture
from sklearn.cluster import KMeans, SpectralClustering
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

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
# This section finds optimal number of clusters using the silhouette score.
# I obtain the silhouette score for kmeans clustering using between 2 and 20 clusters.
# I could also obtain silhouette scores using other clustering methods.
# The best value is 1 and the worst is -1.
# For the clustering algorithms below, I will use 2 clusters when possible.

# Create empty lists for clusters and silhouette scores.
cluster_list = []
silhouette_scores = []
ch_index = []

# Obtain silhouette scores.
for i in range(2, 21):

    # Add the cluster 'i' to 'cluster_list'.
    cluster_list.append(i)

    # Get the silhouette score for kmeans clustering with 'i' clusters
    sil_score = silhouette_score(X = all_data_scaled,
                                 labels = KMeans(n_clusters = i,
                                                 random_state = 12346).fit(all_data_scaled).labels_,
                                 random_state = 12346)

    # Add 'sil_score' to 'silhouette_scores'.
    silhouette_scores.append(sil_score)

    # Get the Calinski - Harabasz score.
    ch_score = calinski_harabaz_score(X = all_data_scaled,
                                      labels = KMeans(n_clusters = i,
                                                      random_state = 12346).fit(all_data_scaled).labels_)

    # Add 'ch_score' to 'ch_index'.
    ch_index.append(ch_score)
                                      
# Print the optimal number of clusters according to the 2 metrics above and those metric values.
print('Optimal # of Clusters according to Silhouette Score: ' + 
      str(cluster_list[silhouette_scores.index(max(silhouette_scores))]))
print('Best Silhouette Score: ' + 
      str(round(max(silhouette_scores), 2)))
print('Optimal # of Clusters according to Calinski - Harabasz score: ' + 
      str(cluster_list[ch_index.index(max(ch_index))]))
print('Best Calinski - Harabasz Score: ' + 
      str(round(max(ch_index), 2)))

# Plot silhouette scores.

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add silhouette scores.
ax1.plot(cluster_list,
         silhouette_scores,
         color = 'black')

# Set plot and axes titles.
plt.title('Silhouette Scores')
plt.xlabel('# of Clusters')
plt.ylabel('Silhouette Scores')

# Show plot.
plt.show()

###################
# KMEANS CLUSTERING
###################
# This section conducts k-means clustering with 2 clusters.
# I couldn't find a way to check cluster stability, but...
# This implementation is slightly different from the kmeans I run in the R branch.
# It runs 10 (can be changed with 'n_init' parameter) times and uses the best result
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
# I use 'scipy' instead of 'sklearn' to access an easy way of doing dendrograms.
# I could not find a way to show cluster centers or check cluster stability.

# Create distance matrix and conduct hierarchical clustering.
linkage_matrix = linkage(all_data_scaled)

# Add cluster assignments to 'all_data'.
all_data['hier_clusters'] = fcluster(linkage_matrix,
                                     t = 2,
                                     criterion = 'maxclust')

# View cluster sizes.
all_data.hier_clusters.value_counts()

# Create figure and subplot for truncated dendrogram.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Specify dendrogram.
dendrogram(linkage_matrix,
           truncate_mode = 'lastp',
           p = 30)

# Specify dendrogram title, x-axis label, and y-axis label.
plt.title('Hierarchical Clustering Dendrogram')
plt.ylabel('Distance')
plt.xlabel('Sample Index')

# Show truncated dendrogram.
plt.show()

# Create figure and subplot for scatter plot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add scatter plot data, 1 cluster at a time.
plt.scatter(all_data[all_data.hier_clusters == 1].x,
            all_data[all_data.hier_clusters == 1].y,
            color = 'red')
plt.scatter(all_data[all_data.hier_clusters == 2].x,
            all_data[all_data.hier_clusters == 2].y,
            color = 'blue')

# Set plot and axes titles.
plt.title('Hierarchical Clustering Result')
plt.xlabel('x')
plt.ylabel('y')

# Show plot.
plt.show()

##########################################
# EXPECTATION MAXIMIZATION (EM) CLUSTERING
##########################################
# This section conducts EM clustering with 2 clusters.
# I didn't find anything explicitly called 'Expectation Maximization',
# but the 'GaussianMixture' function used below seems similar.
# The result is unexpected and looks like 2 ellipsoid normal distributions
# creating a sort of 'X' pattern.
# I couldn't find a way to check cluster stability, but...
# This implementation is slightly different from the kmeans I run in the R branch.
# It runs 10 (can be changed with 'n_init' parameter) times and uses the best result
# according to some metric.
# In my view, this somewhat removes the need for checking cluster stability,
# since I'm using the best clustering result found in 'n_init' runs.

# Conduct EM clustering.
em = mixture.GaussianMixture(n_components = 2,
                             init_params = 'random',
                             n_init = 25,
                             random_state = 12346).fit(all_data_scaled)

# Get scaled cluster centers.
em_centers = pd.DataFrame(em.means_)
em_centers.columns = ['x', 'y']

# Unscale 'em_centers' and view unscaled cluster centers.
# Note that EM cluster centers may not be that meaningful.
# 2 clusters could have the same EM center but different variance parameters
# on the normal distribution and so have different points associated with the cluster.
em_centers.x = (em_centers.x * all_data.x.std(ddof = 0)) + all_data.x.mean()
em_centers.y = (em_centers.y * all_data.y.std(ddof = 0)) + all_data.y.mean()
em_centers

# Add EM cluster assignments to 'all_data'.
# I couldn't find a built-in way of looking at these for training data,
# so I used 'predict' functionality'.
all_data['em_clusters'] = em.predict(all_data_scaled)

# View cluster sizes.
all_data.em_clusters.value_counts()

# Create figure and subplot for scatter plot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add scatter plot data, 1 cluster at a time.
plt.scatter(all_data[all_data.em_clusters == 0].x,
            all_data[all_data.em_clusters == 0].y,
            color = 'red')
plt.scatter(all_data[all_data.em_clusters == 1].x,
            all_data[all_data.em_clusters == 1].y,
            color = 'blue')

# Add cluster centers.
plt.text(x = em_centers.x[0],
         y = em_centers.y[0],
         s = 'C1',
         fontsize = 15)
plt.text(x = em_centers.x[1],
         y = em_centers.y[1],
         s = 'C2',
         fontsize = 15)

# Set plot and axes titles.
plt.title('Expectation Maximization Clustering Result')
plt.xlabel('x')
plt.ylabel('y')

# Show plot.
plt.show()

#####################
# SPECTRAL CLUSTERING
#####################
# This section conducts spectral clustering with 2 clusters.
# I could not find a way to show cluster centers, but I think this is not very important
# for spectral clustering.
# I couldn't find a way to check cluster stability, but...
# This implementation is slightly different from the spectral clustering I run in the R branch.
# It runs 10 (can be changed with 'n_init' parameter) times and uses the best result
# according to some metric.
# In my view, this somewhat removes the need for checking cluster stability,
# since I'm using the best clustering result found in 'n_init' runs.

# Conduct spectral clustering with 2 clusters.
spectral = SpectralClustering(n_clusters = 2,
                              affinity = 'nearest_neighbors',
                              random_state = 12346,).fit(all_data_scaled)

# View the affinity matrix.
spectral.affinity_matrix_

# Add spectral clustering labels to 'all_data'.
all_data['spectral_clusters'] = spectral.labels_

# View cluster sizes.
all_data.spectral_clusters.value_counts()

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add scatter plot data, 1 cluster at a time.
plt.scatter(all_data[all_data.spectral_clusters == 0].x,
            all_data[all_data.spectral_clusters == 0].y,
            color = 'red')
plt.scatter(all_data[all_data.spectral_clusters == 1].x,
            all_data[all_data.spectral_clusters == 1].y,
            color = 'blue')

# Set plot and axes titles.
plt.title('Spectral Clustering Result')
plt.xlabel('x')
plt.ylabel('y')

# Show plot.
plt.show()

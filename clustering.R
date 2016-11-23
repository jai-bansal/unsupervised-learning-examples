# This script conducts various types of clustering on generated data.

# LOAD LIBRARIES --------------------------------------------------------------------
# This section loads necessary libraries.
library(data.table)
library(ggplot2)
library(dplyr)
library(fpc)
library(mclust)
library(kernlab)

# GENERATE DATA -----------------------------------------------------------
# This section generates the data that will be clustered.

  # Create small and large squares of data.
  set.seed(12346)
  small_rectangle = data.table(x = runif(500, 
                                         min = -1, 
                                         max = 1), 
                               y = runif(500, 
                                         min = -1, 
                                         max = 1))
  large_rectangle = data.table(x = runif(1000, 
                                         min = -5, 
                                         max = 5), 
                               y = runif(1000, 
                                         min = -5, 
                                         max = 5))
  
  # Remove most of the points in the interior of the rectangles.
  # The remaining points will be around the borders.
  small_rectangle = small_rectangle[abs(x) > 0.75 | abs(y) > 0.75]
  large_rectangle = large_rectangle[abs(x) > 4 | abs(y) > 4]
  
  # Plot 'small_rectangle' and 'large_rectangle' data.
  ggplot(data = small_rectangle, 
         aes(x = x, 
             y = y)) + 
    geom_point() + 
    geom_point(data = large_rectangle, 
               aes(x = x, 
                   y = y)) +
    xlim(c(-7, 7)) + 
    ylim(c(-7, 7)) + 
    ggtitle('Data Points') + 
    xlab('x') + 
    ylab('y')
  
  # Combine 'small_rectangle' and 'large_rectangle' to conduct clustering.
  all_data = rbind(small_rectangle, large_rectangle)
  
  # Scale data columns and create data table with scaled data. This should be done prior to clustering.
  # I do this separately so I can later access the mean and standard deviation of scaling.
  x_scaled = scale(all_data$x)
  y_scaled = scale(all_data$y)
  scaled_data = data.table(x_scaled = x_scaled, 
                           y_scaled = y_scaled)
  scaled_data = rename(scaled_data, 
                       x_scaled = x_scaled.V1, 
                       y_scaled = y_scaled.V1)
  

# DETERMINE NUMBER OF CLUSTERS --------------------------------------------
# Find optimal number of clusters according to some common metrics.
# Results vary widely and are not always helpful.
# For the clustering algorithms below, I will use 2 clusters when possible.
  
  # Method 1: Plot 'Total Within clusters Sum of Squares' against 'Number of clusters' (SCREE plot).
  # 'Elbow' of the following plot indicates best number of clusters.
  # This method appears to recommend 4 clusters. Or maybe 7.
  
    # Choose maximum number of clusters to consider.
    max_clusters = 20
  
    # Compute 'Total Within cluster Sum of Squares' (wss):
    within_sum_squares = (nrow(scaled_data) - 1) * sum(apply(scaled_data, 
                                                             2, 
                                                             var))
    for (i in 2:max_clusters) 
      
      {
      
        # Compute within sum of squares for each number of clusters.
        within_sum_squares[i] = sum(kmeans(scaled_data, 
                                           centers = i)$withinss)
        
      }
  
    # Plot 'wss' against 'Number of clusters':  
    plot(1:max_clusters, 
         within_sum_squares, 
         type = 'b', 
         xlab = '# of clusters', 
         ylab = 'Total Within clusters Sum of Squares')
    
  # Method 2: 'kmeansruns()' with Calinski - Harabasz Index.
  # This method recommends 1 cluster.
      
    # Best number of clusters as identified by this method.
    kmeansruns(all_data, 
               krange = 1:max_clusters, 
               criterion = 'ch', 
               scaledata = T)$bestk
  
    # Critical values using above method:
    kmeansruns(all_data, 
               krange = 1:max_clusters, 
               criterion = 'ch', 
               scaledata = T)$crit

  # Method 3: 'kmeansruns()' with Average Silhouette Width.
  # This method recommends 1 cluster.

    # Best number of clusters as identified by this method.
    kmeansruns(all_data, 
               krange = 1:max_clusters, 
               criterion = 'asw',
               scaledata = T)$bestk
  
    # Critical values using above method.
    kmeansruns(all_data, 
               krange = 1:max_clusters, 
               criterion = 'asw', 
               scaledata = T)$crit
    
  # For the clustering algorithms below, I will use 2 clusters when possible.
  clusters = 2

# KMEANS CLUSTERING -------------------------------------------------------
# This section conducts k-means clustering with 2 clusters.
  
  # Conduct k-means clustering with 2 clusters.
  set.seed(12346)
  kmeans = kmeans(scaled_data, 
                  centers = clusters)
  
  # View cluster sizes.
  kmeans$size
  
  # Convert cluster centers back into unscaled values and view cluster centers.
  kmeans_centers = data.table(kmeans$centers)
  kmeans_centers$x_scaled = (kmeans_centers$x_scaled * attr(x_scaled, 
                                                            'scaled:scale')) + attr(x_scaled, 
                                                                                    'scaled:center')
  kmeans_centers$y_scaled = (kmeans_centers$y_scaled * attr(y_scaled, 
                                                            'scaled:scale')) + attr(y_scaled, 
                                                                                    'scaled:center')
  kmeans_centers = rename(kmeans_centers, 
                          x = x_scaled, 
                          y = y_scaled)
  print(kmeans_centers)
  
  # Add kmeans clusters to 'all_data'.
  all_data$kmeans_clusters = kmeans$cluster
  
  # Check stability of 'k-means' clusters.
  # Neither cluster is very stable.
  kmeans_stability = clusterboot(as.data.frame(scaled_data), 
                                 clustermethod = kmeansCBI, 
                                 krange = clusters,
                                 seed = 12346)
  kmeans_stability$bootmean
  
  # Plot kmeans clustering results and cluster centers (black Cs).
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(kmeans_clusters))) + 
    geom_point() + 
    annotate('text', 
             x = kmeans_centers$x[1], 
             y = kmeans_centers$y[1], 
             label = 'C1', 
             size = 5) + 
    annotate('text', 
             x = kmeans_centers$x[2], 
             y = kmeans_centers$y[2], 
             label = 'C2', 
             size = 5) + 
    theme(legend.position = 'none') +
    ggtitle('Kmeans Clustering Result')
 

# HIERARCHICAL CLUSTERING -------------------------------------------------
# This section conducts hierarchical clustering with 2 clusters.
  
  # Create distance matrix.
  hier_distance = dist(scaled_data, 
                       method = 'euclidean')
  
  # Perform hierarchical clustering.
  hier_clust = hclust(hier_distance)
  
  # Add hierarchical clusters to 'all_data'.
  all_data$hier_clust = cutree(hier_clust, 
                               k = 2)
  
  # View hierarchical cluster sizes.
  table(all_data$hier_clust)
  
  # Check hierarchical cluster stability.
  hier_stability = clusterboot(as.data.frame(scaled_data), 
                               clustermethod = hclustCBI, 
                               method = 'ward.D',
                               k = 2,
                               seed = 12346)
  
  # View stability of clusters.
  # One cluster is relatively stable and the other is moderately stable.
  hier_stability$bootmean
  
  # Plot dendogram.
  # Note: this plot is crowded.
  plot(hier_clust)
  
  # Plot hierarchical clustering results.
  # I don't include cluster centers as I don't think they are important for hierarchical clustering.
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(hier_clust))) + 
    geom_point() + 
    theme(legend.position = 'none') +
    ggtitle('Hierarchical Clustering Result')

# EXPECTATION MAXIMIZATION (EM) CLUSTERING -------------------------------------
# This section conducts EM clustering with 2 clusters.
# I couldn't find a cluster stability method for EM.

  # Conduct EM clustering with 2 clusters.
  set.seed(12346)
  em = Mclust(scaled_data, 
              G = 2)
  
  # Add EM clustering assignments to 'all_data'.
  all_data$em_clusters = em$classification
  
  # View cluster sizes.
  table(all_data$em_clusters)
  
  # View cluster centers.
  
    # Save 'scaled_data' cluster centers in 'em_clust_centers'.
    em_clust_centers = data.table(em$parameters$mean)
    
    # Unscale the data in 'em_clust_centers'.
    em_clust_centers$V1 = (em_clust_centers$V1 * attr(x_scaled, 
                                                      'scaled:scale')) + attr(x_scaled, 
                                                                              'scaled:center')
    em_clust_centers$V2 = (em_clust_centers$V1 * attr(y_scaled, 
                                                      'scaled:scale')) + attr(y_scaled, 
                                                                              'scaled:center')
    
    # Rename columns of 'em_clust_centers'.
    em_clust_centers = rename(em_clust_centers, 
                              x = V1, 
                              y = V2)
    
    # View cluster centers.
    em_clust_centers
  
  # Plot EM clustering results 1 with cluster centers.
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(em_clusters))) + 
    geom_point() + 
    annotate('text', 
             x = em_clust_centers$x[1], 
             y = em_clust_centers$y[1], 
             label = 'C1', 
             size = 5) + 
    annotate('text', 
             x = em_clust_centers$x[2], 
             y = em_clust_centers$y[2], 
             label = 'C2', 
             size = 5) + 
    theme(legend.position = 'none') +
    ggtitle('Expectation Maximization Clustering Result')
  
  # Plot EM clustering results 2 with cluster centers (for scaled data).
  plot(em, 
       what = 'classification')


# SPECTRAL CLUSTERING -----------------------------------------------------
# This section conducts spectral clustering with 2 clusters.

  # Conduct spectral clustering with 2 clusters.
  spec_clust = specc(as.matrix(scaled_data), 
                     centers = 2)
  
  # View cluster sizes.
  size(spec_clust)
  
  # View cluster centers.
  
    # Save 'scaled_data' cluster centers in 'spec_clust_centers'.
    spec_clust_centers = data.table(centers(spec_clust))

    # Unscale the data in 'spec_clust_centers'.
    spec_clust_centers$V1 = (spec_clust_centers$V1 * attr(x_scaled, 
                                                          'scaled:scale')) + attr(x_scaled, 
                                                                                  'scaled:center')
    spec_clust_centers$V2 = (spec_clust_centers$V2 * attr(y_scaled, 
                                                          'scaled:scale')) + attr(y_scaled, 
                                                                                  'scaled:center')
    spec_clust_centers = rename(spec_clust_centers, 
                                x = V1, 
                                y = V2)
    
    # View cluster centers.
    spec_clust_centers
    
  # Check spectral cluster stability.
  # Warning: this takes a while.
  # Both clusters are perfectly stable (both have scores of 1).
  spectral_stability = clusterboot(as.data.frame(scaled_data), 
                                   clustermethod = speccCBI, 
                                   k = 2, 
                                   seed = 12346)
  spectral_stability$bootmean
  
  # Plot spectral clustering results.
  # I exclude cluster centers from the plot as I don't think they are important for spectral clustering.
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(spec_clust))) + 
    geom_point() + 
    theme(legend.position = 'none') +
    ggtitle('Spectral Clustering Result')
# This script conducts various types of clustering on generated data.

# LOAD LIBRARIES --------------------------------------------------------------------
# This section loads necessary libraries.
library(data.table)
library(ggplot2)
library(dplyr)
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

# KMEANS CLUSTERING -------------------------------------------------------
  
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
  
  # NEED TO CHECK HOW MANY CLUSTERS ARE IDEAL (3 ways?)
  
  # Conduct k-means clustering with 2 clusters.
  set.seed(12346)
  kmeans = kmeans(scaled_data, 
                  centers = 2)
  
  # Convert cluster centers back into unscaled values and view cluster centers.
  kmeans_centers = data.table(kmeans$centers)
  kmeans_centers$x_scaled = (kmeans_centers$x_scaled * attr(x_scaled, 
                                                            'scaled:scale')) + attr(x_scaled, 
                                                                                    'scaled:center')
  kmeans_centers$y_scaled = (kmeans_centers$y_scaled * attr(y_scaled, 
                                                            'scaled:scale')) + attr(y_scaled, 
                                                                                    'scaled:center')
  print(kmeans_centers)
  
  # Add kmeans clusters to 'all_data'.
  all_data$kmeans_clusters = kmeans$cluster
  
  # BOOTSTRAPPING FOR STABILITY CHECK????
  
  # Plot kmeans clustering results and cluster centers (black Cs).
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(kmeans_clusters))) + 
    geom_point() + 
    annotate('text', 
             x = kmeans_centers$x_scaled[1], 
             y = kmeans_centers$y_scaled[1], 
             label = 'C1', 
             size = 5) + 
    annotate('text', 
             x = kmeans_centers$x_scaled[2], 
             y = kmeans_centers$y_scaled[2], 
             label = 'C2', 
             size = 5) + 
    theme(legend.position = 'none') +
    ggtitle('Kmeans Clustering Result')

# EXPECTATION MAXIMIZATION (EM) CLUSTERING -------------------------------------
  ??????????????
  # Conduct EM clustering.
  set.seed(134)
  em = Mclust(scaled_data, 
              G = 2)
  
  # Add EM clustering assignments to all data.
  all_data$em_clusters = em$classification
  
  # Plot EM clustering results 1.
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(em_clusters))) + 
    geom_point() + 
    theme(legend.position = 'none') +
    ggtitle('Expectation Maximization Clustering Result')
  
  # Plot EM clustering results 2 (for scaled data).
  plot(em, 
       what = 'classification')

# SPECTRAL CLUSTERING -----------------------------------------------------

  # Conduct spectral clustering with 2 clusters.
  spec_clust = specc(as.matrix(scaled_data), 
                     centers = 2)
  
  # View cluster centers and sizes.
  centers(spec_clust)     # cluster centers
  size(spec_clust)        # cluster sizes
  
  # Save spectral clustering cluster centers for plot.
  # I'm not sure what cluster centers mean in the context of spectral clustering.
  spectral_centers = data.table(centers(spec_clust))
  
  # Plot spectral clustering results.
  ggplot(data = all_data, 
         aes(x = x, 
             y = y, 
             color = as.character(spec_clust))) + 
    geom_point() + 
    annotate('text', 
             x = spectral_centers$V1[1], 
             y = spectral_centers$V2[1], 
             label = 'C', 
             size = 5) +
    annotate('text', 
             x = spectral_centers$V1[2], 
             y = spectral_centers$V2[2], 
             label = 'C', 
             size = 5) +
    theme(legend.position = 'none') +
    ggtitle('Spectral Clustering Result')
  
  
  
   annotate('text', 
             x = kmeans_centers$x_scaled[1], 
             y = kmeans_centers$y_scaled[1], 
             label = 'C1', 
             size = 5)
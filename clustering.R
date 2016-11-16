# This script conducts various types of clustering on generated data.

# LOAD LIBRARIES --------------------------------------------------------------------
# This section loads necessary libraries.
library(data.table)
library(ggplot2)

# GENERATE DATA -----------------------------------------------------------
# This section generates the data that will be clustered.

  # Create small and large squares of data.
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

# EXPECTATION MAXIMIZATION CLUSTERING -------------------------------------

# SPECTRAL CLUSTERING -----------------------------------------------------


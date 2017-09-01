# This script conducts T-Distributed Stochastic Neighbor Embedding (TSNE) on generated data.
# Unlike PCA, there does not seem to be an implemented mechanism to "predict" points into the 
# dimension-reduced TSNE space.
# Due to the theory of TSNE, this appears to be a non-trivial problem.

# I have used TSNE as a precursor to clustering and as a visualization tool for clustering results.

# LOAD LIBRARIES --------------------------------------------------------------------
# This section loads necessary libraries for this script.
library(data.table)
library(ggplot2)
library(dplyr)
library(Rtsne)

# GENERATE DATA -----------------------------------------------------------
# This section generates the data that will be dimension-reduced using TSNE.

  # Set seed for reproducible analysis.
  set.seed(8583)

  # Generate linear original data.
  data = data.table(x = rep(c(1:100), 2), 
                    y = rep(c(1:100), 2), 
                    z = rep(c(1:100), 2))

  # 'Jitter' the data so it's not exactly linear.
  data$x = jitter(data$x, 
                  amount = 7)
  data$y = jitter(data$y, 
                  amount = 7)
  data$z = jitter(data$z, 
                  amount = 7)

# TSNE --------------------------------------------
# This section conducts TSNE.

  # Conduct TSNE on 'data'.
  # The TSNE function includes a scaling argument.
    set.seed(8583)
    ts = Rtsne(data, 
               pca_center = T, 
               pca_scale = T,
               check_duplicates = F)
    
  # Get new 2D representation of 'data'.
  tsne_data = data.table(ts$Y)
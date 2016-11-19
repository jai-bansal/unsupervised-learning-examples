# This script conducts various types of clustering on generated data.

################
# IMPORT MODULES
################
import numpy as np
import pandas as pd

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

# Plot initial data.

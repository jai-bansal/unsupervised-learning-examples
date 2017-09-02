# This script conducts T-Distributed Stochastic Neighbor Embedding (TSNE) on generated data.
# Unlike PCA, there does not seem to be an implemented mechanism to "predict" points into the 
# dimension-reduced TSNE space.
# Due to the theory of TSNE, this appears to be a non-trivial problem.

# I have used TSNE as a precursor to clustering and as a visualization tool for clustering results.

##############
# LOAD MODULES
##############
# This section loads necessary modules.
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import scale
from sklearn.manifold import TSNE

###############
# GENERATE DATA
###############
# This section generates the data that will be dimension-reduced with TSNE.

# Set seed for reproducible analysis.
random_seed = np.random.RandomState(8583)

# Generate linear original data.
data = pd.DataFrame()
data['x'] = np.repeat(list(range(1, 101)), 2)
data['y'] = np.repeat(list(range(1, 101)), 2)
data['z'] = np.repeat(list(range(1, 101)), 2)

# Add random noise to 'data' values so they're not exactly linear.
data['noise_1'] = random_seed.randint(-15, 16, size = data.shape[0]) / 2
data['noise_2'] = random_seed.randint(-15, 16, size = data.shape[0]) / 2
data['noise_3'] = random_seed.randint(-15, 16, size = data.shape[0]) / 2
data.x = data.x + data.noise_1
data.y = data.y + data.noise_2
data.z = data.z + data.noise_3

# Remove unneeded columns from 'data' and 'new_data'.
data = data[['x', 'y', 'z']]

######
# TSNE
######
# This section conducts TSNE.

# For completeness, scale data.
scaled_data = pd.DataFrame(scale(data))
scaled_data.columns = ['x', 'y', 'z']

# Conduct TSNE on 'scaled_data'.
ts = TSNE(random_state = 8583).fit_transform(scaled_data)


# This script conducts principal component analysis (PCA) on generated data.
# It then projects new (also generated) data onto the components yielded from PCA.

##############
# LOAD MODULES
##############
# This section loads necessary modules for this script.
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

###############
# GENERATE DATA
###############
# This section generates the data that will be used for PCA.
# It also generates 'new' data that the PCA will be applied to.

# Set seed for reproducible analysis.
random_seed = np.random.RandomState(8583)

# Generate linear original and 'new' data.
data = pd.DataFrame()
data['x'] = np.repeat(list(range(1, 101)), 2)
data['y'] = np.repeat(list(range(1, 101)), 2)
new_data = pd.DataFrame()
new_data['x'] = np.repeat(list(range(1, 101)), 2)
new_data['y'] = np.repeat(list(range(1, 101)), 2)

# Add random noise to 'data' and 'new_data' values so they're not exactly linear.
data['noise_1'] = random_seed.randint(-15, 16, size = data.shape[0]) / 2
data['noise_2'] = random_seed.randint(-15, 16, size = data.shape[0]) / 2
new_data['noise_1'] = random_seed.randint(-15, 16, size = new_data.shape[0]) / 2
new_data['noise_2'] = random_seed.randint(-15, 16, size = new_data.shape[0]) / 2
data.x = data.x + data.noise_1
data.y = data.y + data.noise_2
new_data.x = new_data.x + new_data.noise_1
new_data.y = new_data.y + new_data.noise_2

# Set style for plots.
style.use('ggplot')

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add scatter plot data.
plt.scatter(data.x,
            data.y,
            color = 'black')

# Set plot and axes titles.
plt.title('Initial Data Points')
plt.xlabel('x')
plt.ylabel('y')

# Show plot.
plt.show()

# Create an empty table called 'first_components'.
# This will be filled with the first components of PCA below.
# Specifically, it will be filled with the first principal component from the original data and the projection of 'new_data' onto
# the results of PCA.
first_components = pd.DataFrame()

# Remove unneeded columns from 'data' and 'new_data'.
data = data[['x', 'y']]
new_data = new_data[['x', 'y']]

##############################
# PRINCIPAL COMPONENT ANALYSIS
##############################
# This section conducts principal component analysis.
# I couldn't find a simple way to generate a biplot :(

# Scale data.
scaled_data = pd.DataFrame(scale(data))
scaled_data.columns = ['x', 'y']
scaled_new_data = pd.DataFrame(scale(new_data))
scaled_new_data.columns = ['x', 'y']

# Conduct principal component analysis on 'scaled_data'.
pca = PCA(n_components = 1,
          random_state = 8583).fit(scaled_data)

# View percentage of variance explained by the single component.
pca.explained_variance_ratio_

# Add the first principal component to 'first_components'.
pca_first_orig = pd.DataFrame(pca.transform(scaled_data))
first_components = first_components.append(pca_first_orig)

# Project 'new_data' onto 'pca' and add to 'first_components'.
first_components['pca_first_pred'] = pd.DataFrame(pca.transform(scaled_new_data))
first_components.columns = ['pca_first_orig', 'pca_first_pred']
del(pca_first_orig)

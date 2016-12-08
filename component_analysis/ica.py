# This script conducts independent component analysis (ICA) using generated data.
# I create 2 signal 'sources' and mix them with a mixing matrix.
# Then, I use ICA to attempt to separate the mixed signals.

##############
# LOAD MODULES
##############
# This section loads necessary modules.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.decomposition import FastICA

# GENERATE DATA -----------------------------------------------------------
# This section generates the 'sources' and mixes them with a mixing matrix.

# Generate signal 'sources'.
signals = pd.DataFrame()
signals['signal_1'] = np.sin(range(1, 101))
signals['signal_2'] = np.tile(range(1, 26), 4) / 25

# Generate mixing matrix.
mixing = np.matrix('0.3, 0.5; 0.4 -0.6')

# Mix 'signal_1' and 'signal_2'.
mixed_signals = pd.DataFrame(np.dot(signals, mixing))
mixed_signals.columns = ['m1', 'm2']

# Plot original signals.

# Set style.
style.use('ggplot')

# Plot signal 1. 

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add line data.
ax1.plot(range(1, 101),
         signals['signal_1'],
         color = 'black')

# Set title and axes labels.
plt.title('Signal 1')
plt.xlabel('')
plt.ylabel('Signal 1')

# Show plot.
plt.show()

# Plot signal 2. 

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add line data.
ax1.plot(range(1, 101),
         signals['signal_2'],
         color = 'black')

# Set title and axes labels.
plt.title('Signal 2')
plt.xlabel('')
plt.ylabel('Signal 2')

# Show plot.
plt.show()

# Plot linearly mixed signals.

# Plot mixed signal 1.

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add line data.
ax1.plot(range(1, 101),
         mixed_signals['m1'],
         color = 'black')

# Set title and axes labels.
plt.title('Mixed Signal 1')
plt.xlabel('')
plt.ylabel('Mixed Signal 1')

# Show plot.
plt.show()

# Plot mixed signal 2.

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add line data.
ax1.plot(range(1, 101),
         mixed_signals['m2'],
         color = 'black')

# Set title and axes labels.
plt.title('Mixed Signal 2')
plt.xlabel('')
plt.ylabel('Mixed Signal 2')

# Show plot.
plt.show()

################################
# INDEPENDENT COMPONENT ANALYSIS
################################
# This section conducts independent component analysis.

# Conduct ICA.
ica = FastICA(n_components = 2,
              random_state = 8583).fit(mixed_signals)

# View estimated mixing matrix.
# This is a bit different than the actual mixing matrix 'mixing',
# but similar to the estimated mixing matrix in the R branch.
ica.mixing_

# Reconstruct source signals.
estimated_signals = pd.DataFrame(ica.transform(mixed_signals))
estimated_signals.columns = ['e1', 'e2']

# Plot the source signal estimates found by ICA.
# The estimate for source signal 1 looks pretty good,
# but not so much for the estimate for source signal 2.
# The results are very similar to the plotted estimates in the R branch.

# Plot source signal 1 estimate.

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add line data.
ax1.plot(range(1, 101),
         estimated_signals['e1'],
         color = 'black')

# Set title and axes labels.
plt.title('Source Signal 1 Estimate')
plt.xlabel('')
plt.ylabel('Source Signal 1 Estimate')

# Show plot.
plt.show()

# Plot source signal 2 estimate.

# Create figure and subplot.
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Add line data.
ax1.plot(range(1, 101),
         estimated_signals['e2'],
         color = 'black')

# Set title and axes labels.
plt.title('Source Signal 2 Estimate')
plt.xlabel('')
plt.ylabel('Source Signal 2 Estimate')

# Show plot.
plt.show()

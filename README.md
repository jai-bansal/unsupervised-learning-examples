#### Summary:
This project contains reference code and visualizations for various unsupervised learning techniques in R and Python. The goal is to provide examples and reference code/visualizations for unsupervised learning techniques.

The main techniques included are clustering, principal component analysis (PCA), and independent component analysis (ICA). The clustering algorithms included are kmeans, hierarchical, expectation maximization, and spectral. For clustering, best number of clusters analysis, cluster sizes, cluster centers, stability analysis, and relevant plots are provided whenever possible. For component analysis, relevant plots are provided whenever possible.

#### Motivation:
I created this project to learn about and document code and visualizations for unsupervised learning techniques.

#### Contents:
The R and Python analyses are located in the "R" and "Python" branches respectively.
Both branches contain a "clustering" and "component_analysis" folder containing clustering and component analysis material, respectively.

The "R" branch "clustering" folder contains:
- a script with all clustering and related code ("clustering.R")
- a plot of the initial data ("initial_data.png")
- an "elbow plot" image to help decide how many clusters are needed ("elbow_plot.png")
- the result of kmeans clustering ("kmeans_clustering_result.png")
- the result of hierarchical clustering and a dendrogram ("hierarchical_clustering_result.png" and "hierarchical_clustering_dendrogram.png" respectively)
- 2 plots of the result of expectation maximization clustering ("em_clustering_result_1.png" and "em_clustering_result_2.png")
- the result of spectral clustering ("spectral_clustering_result.png")

The "R" branch "component_analysis" folder contains:
- scripts with PCA and ICA code ("pca.R" and "ica.R" respectively)
- a plot with the initial data for PCA ("pca_initial_data.png")
- a biplot of the result of PCA ("pca_biplot.png")
- the source signals for ICA ("ica_source_signal_1.png" and "ica_source_signal_2.png")
- the mixed signals for ICA ("ica_mixed_signal_1.png" and "ica_mixed_signal_2.png")
- the source signal estimates for ICA ("ica_source_signal_estimate_1.png" and "ica_source_signal_estimate_2.png")

The "Python" branch "clustering" folder contains:
- a script with all clustering and related code ("clustering.py")
- a plot of the initial data ("initial_data.png")
- a plot of silhouette scores to help decide how many clusters are needed ("silhouette_scores.png")
- the result of kmeans clustering ("kmeans_clustering_result.png")
- the result of hierarchical clustering and a dendrogram ("hierarchical_clustering_result.png" and "hierarchical_clustering_dendrogram.png" respectively)
- the result of expectation maximization clustering ("em_clustering_result.png")
- the result of spectral clustering ("spectral_clustering_result.png")

The "Python" branch "component_analysis" folder contains:
- scripts with PCA and ICA code ("pca.py" and "ica.py" respectively)
- a plot with the initial data for PCA ("pca_initial_data.png")
- the source signals for ICA ("ica_source_signal_1.png" and "ica_source_signal_2.png")
- the mixed signals for ICA ("ica_mixed_signal_1.png" and "ica_mixed_signal_2.png")
- the source signal estimates for ICA ("ica_source_signal_estimate_1.png" and "ica_source_signal_estimate_2.png")

#### Dataset Details:
I generate all data depending on the technique being used.

#### License:
GNU General Public License

# This scripts conducts principal, independent, and random component analysis on generated data.
# It then applies the analyses above to new (also generated) data.

# LOAD LIBRARIES --------------------------------------------------------------------
# This section loads necessary libraries for this script.
library(data.table)
library(ggplot2)
library(dplyr)

# GENERATE DATA -----------------------------------------------------------
# This section generates the data that will be used for principal, independent, and random component analysis.
# It also generates 'new' data that the component analyses will be applied to.

  # Set seed for reproducible analysis.
  set.seed(8583)

  # Generate linear original and 'new' data.
  data = data.table(x = rep(c(1:100), 2), 
                    y = rep(c(1:100), 2))
  new_data = data.table(x = rep(c(1:100), 2), 
                        y = rep(c(1:100), 2))

  # 'Jitter' the data so it's not exactly linear.
  data$x = jitter(data$x, 
                  amount = 7)
  data$y = jitter(data$y, 
                  amount = 7)
  new_data$x = jitter(new_data$x, 
                      amount = 7)
  new_data$y = jitter(new_data$y, 
                      amount = 7)

  # Plot initial data points.
  ggplot(data = data, 
         aes(x = x, 
             y = y)) + 
  geom_point() + 
  ggtitle('Initial Data Points') + 
  xlab('x') + 
  ylab('y')

  # Create an empty table called 'first_components'.
  # This will be filled with the first components of principal, independent, and random component analysis below.
  # Specifically, it will be filled with the first component from the original data and the projection of 'new_data' onto
  # the results of the 3 component analyses.
  first_components = data.table(pca_first_orig = rep(NA, nrow(data)), 
                                pca_first_pred = rep(NA, nrow(data)),
                                ica_first_orig = rep(NA, nrow(data)), 
                                ica_first_pred = rep(NA, nrow(data)),
                                rca_first_orig = rep(NA, nrow(data)), 
                                rca_first_pred = rep(NA, nrow(data)))

# PRINCIPAL COMPONENT ANALYSIS --------------------------------------------
# This section conducts principal component analysis.

  # Conduct principal component analysis on 'data'.
  # The principal component analysis function includes a scaling argument.
  pca = prcomp(data, 
               scale = T,
               center = T)

  # View summary of 'pca'.
  summary(pca)

  # Plot the variances associated with each principal component.
  plot(pca)

  # View the biplot of 'pca'.
  biplot(pca, 
         scale = 0)

  # Add the first principal component to 'first_components'.
  first_components$pca_first_orig = data.table(pca$x)[, .(PC1)]

  # Project 'new_data' onto 'pca' and add to 'first_components'.
  first_components$pca_first_pred = data.table(predict(pca, 
                                                       newdata = new_data))[, .(PC1)]

# INDEPENDENT COMPONENT ANALYSIS --------------------------------------------
# This section conducts independent component analysis.

# RANDOM COMPONENT ANALYSIS --------------------------------------------
# This section conducts random component analysis.
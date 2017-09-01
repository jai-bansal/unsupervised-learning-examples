# This script conducts independent component analysis (ICA) using generated data.
# I create 2 signal 'sources' and mix them with a mixing matrix.
# Then, I use ICA to attempt to separate the mixed signals.

# LOAD LIBRARIES --------------------------------------------------------------------
# This section loads necessary libraries for this script.
library(data.table)
library(ggplot2)
library(ica)

# GENERATE DATA -----------------------------------------------------------
# This section generates the 'sources' and mixes them with a mixing matrix.

  # Generate signal 'sources'.
  signals = data.table(signal_1 = sin(1:100), 
                       signal_2 = rep((1:25) / 25))

  # Generate mixing matrix.
  mixing = matrix(c(0.3, 0.4, 0.5, -0.6), 2, 2)

  # Mix 'signal_1' and 'signal_2'.
  mixed_signals = data.table(as.matrix(signals) %*% mixing)

  # Plot original signals.

    # Signal 1
    ggplot(data = signals, 
           aes(x = 1:100, 
               y = signal_1)) + 
      geom_line() + 
      ggtitle('Signal 1') + 
      ylab('Signal 1') + 
      xlab('')

    # Signal 2
    ggplot(data = signals, 
           aes(x = 1:100, 
               y = signal_2)) + 
      geom_line() + 
      ggtitle('Signal 2') + 
      ylab('Signal 2') + 
      xlab('')

  # Plot linearly mixed signals.
  
    # Mixed signal 1.
    ggplot(data = mixed_signals, 
           aes(x = 1:100, 
               y = V1)) + 
      geom_line() + 
      ggtitle('Mixed Signal 1') + 
      ylab('Mixed Signal 1') + 
      xlab('')

    # Mixed signal 2.
    ggplot(data = mixed_signals, 
           aes(x = 1:100, 
               y = V2)) + 
      geom_line() + 
      ggtitle('Mixed Signal 2') + 
      ylab('Mixed Signal 2') + 
      xlab('')

# INDEPENDENT COMPONENT ANALYSIS --------------------------------------------
# This section conducts independent component analysis.

  # Conduct ICA.
  ica = icafast(mixed_signals, 
                center = T,
                nc = 2)

  # View the estimated mixing matrix.
  # This is a bit different than the actual mixing matrix 'mixing'.
  ica$M

  # Plot the source signal estimates found by ICA.
  # ICA estimates source signal 1 well, but source signal 2 looks different.

    # Source signal estimate 1.
    ggplot(data = data.table(ica$S), 
           aes(x = 1:100, 
               y = V1)) + 
      geom_line() + 
      ggtitle('Source Signal Estimate 1') + 
      ylab('Source Signal Estimate 1') + 
      xlab('')

    # Source signal estimate 2.
    ggplot(data = data.table(ica$S), 
           aes(x = 1:100, 
               y = V2)) + 
      geom_line() + 
      ggtitle('Source Signal Estimate 2') + 
      ylab('Source Signal Estimate 2') + 
      xlab('')
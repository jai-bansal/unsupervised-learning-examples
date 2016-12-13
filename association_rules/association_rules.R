# This script conducts association rule analysis on generated data.

# LOAD LIBRARIES ----------------------------------------------------------
# This section loads relevant libraries.
library(data.table)
library(readr)
library(arules)

# GENERATE DATA -----------------------------------------------------------
# This section generates the data to be used for association rule analysis.

  # Create data.
  # All data must be of type 'factor' to allow conversion to 'transaction' object.
  data = data.table(transaction = as.factor(c(rep(1, 4), 
                                              rep(2, 4), 
                                              rep(3, 4), 
                                              rep(4, 4), 
                                              rep(5, 4), 
                                              rep(6, 4))), 
                    item = as.factor(c('milk', 'cheese', 'bread', 'soda', 
                                       'milk', 'ice cream', 'meat', 'candy', 
                                       'bread', 'milk', 'water', 'juice', 
                                       'tools', 'eggs', 'milk', 'soda', 
                                       'fruit', 'tools', 'water' ,'milk', 
                                       'milk', 'fruit', 'bread', 'candy')))
  
  # Write 'data' to CSV.
  # The easiest way to get the data into the format required for association rules
  # is to import from CSV.
  write_csv(data, 
            'association_rules_data.csv')

# SUMMARY AND ASSOCIATION RULES ANALYSIS ----------------------------------
# This section conducts summary and association rule analysis.
  
  # Look at the count of each item.
  data[, 
       .N, 
       by = 'item']
  
  # Import data in 'transaction' format.
  txn_data = read.transactions('association_rules_data.csv', 
                               format = 'single', 
                               cols = c('transaction', 'item'), 
                               sep = ',')
  
  # Find and inspect item sets.
  item_sets = eclat(txn_data, 
                    parameter = list(minlen = 2))
  head(inspect(item_sets), 10)
  
  # View only item sets containing 'eggs'.
  inspect(subset(item_sets, 
                 subset = items %in% c('eggs')))
  
  # Find and inspect association rules.
  arules = apriori(txn_data, 
                   parameter = list(support = 0.2, 
                                    confidence = 0.5, 
                                    minlen = 2))
  inspect(arules)
  
  # View only rules containing 'milk' on the left hand side.
  inspect(subset(arules, 
                 subset = lhs %in% c('milk')))
  
  # View p-values (Fisher's exact test) and summary for rules.
  p_values = interestMeasure(arules, 
                             measure = c('fishersExactTest'), 
                             transactions = txn_data)
  summary(p_values)
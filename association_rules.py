# This script conducts association rule analysis on generated data.

################
# IMPORT MODULES
################
# This section imports relevant modules.
from apyori import apriori

###############
# GENERATE DATA
###############
# This section generates the data to be used for association rules analysis.
# There's no need to write to CSV like in R!
data = [['milk', 'cheese', 'bread', 'soda'],
        ['milk', 'ice cream', 'meat', 'candy'],
        ['bread', 'milk', 'water', 'juice'],
        ['tools', 'eggs', 'milk', 'soda'],
        ['fruit', 'tools', 'water' ,'milk'],
        ['milk', 'fruit', 'bread', 'candy']]

###########################
# ASSOCIATION RULE ANALYSIS
###########################
# This section conducts association rule analysis.

# Conduct association rule analysis.
results = list(apriori(data))

# Check the length of 'results'.
# 'results' is a list and each element has item statistics or an
# association rule.
len(results)

# View the first element of 'result'.
results[0]

# Look at the items in the first element of 'results'.
results[0].items

# Look at the support in the first element of 'results'.
results[0].support

# Look at the 'ordered_statistics' (?) in the first element of 'results'.
# Couldn't find good documentation on what exactly this is...
results[0].ordered_statistics
results[0].ordered_statistics[0]

# Look at 'items_base' for the first element of 'results'.
# Couldn't find good documentation on what exactly this is...
results[0].ordered_statistics[0].items_base

# Look at 'items_add' for the first element of 'results'.
# Couldn't find good documentation on what exactly this is...
results[0].ordered_statistics[0].items_add

# View confidence and lift for the first element of 'results'.
results[0].ordered_statistics[0].confidence
results[0].ordered_statistics[0].lift

# Find records with arbitrarily high support, confidence, and items in 'items_base'.
# NOTE: THE FOLLOWING SEARCH IS FOR EXAMPLE PURPOSES ONLY.
# Some records contain confidence and lift measures for adding multiple items to the base item set specified.
# This means that some records have multiple elements in the list(?) 'ordered_statistics'.
# However, some records contain confidence and lift only for adding 1 item.
# Thus, I use a nested loop below.
# The procedure below returns every record where 'support' or the number of items in 'items_base' is high enough.
# However, it only checks the maximum confidence and lift in each record and compares that maximum against 'confidence_cutoff'
# and lift cutoff.
# So it's possible there are records where 'confidence' > 'confidence_cutoff' or 'lift' > 'lift_cutoff' that aren't returned.

# Create empty lists for records with relevant values of the quantities above.
high_support = []
high_confidence = []
high_lift = []
item_base = []

# Create support, confidence, lift, and 'items_base' cutoffs.
# Records with support, confidence, lift, or 'items_base' greater than these values will be added
# to their respective lists.
support_cutoff = 0.75
confidence_cutoff = 1
lift_cutoff = 6
item_base_cutoff = 3

# Loop through records to fill 'high_support', 'high_confidence', 'high_lift', and 'item_base'.
for i in range(0, len(results)):
    
    # Check if record 'i' has high support (higher than 'support_cutoff').
    # If so, add the record number to 'high_support'.
    if results[i].support >= support_cutoff:
        high_support.append(i)

    # Create 'counter' variables to mark the highest 'confidence' and 'lift' achieved in 'results[i].ordered_statistics'.
    confidence_counter = -1
    confidence_index = -1
    lift_counter = -1
    lift_index = -1    

    # Loop through all elements in 'results[i].ordered_statistics'.
    for j in range(0, len(results[i].ordered_statistics)):

        # Check if 'results[i].ordered_statistics[j]' has more items in 'items_base' than 'item_base_cutoff'.
        # If so, add the record number combo to 'item_base'.
        if len(results[i].ordered_statistics[j].items_base) >= item_base_cutoff:
            item_base.append([i, j])
        
        # Check if 'results[i].ordered_statistics[j].confidence' is higher than 'confidence_counter'.
        # If so, replace 'confidence_counter' and 'confidence_index'.
        if results[i].ordered_statistics[j].confidence >= confidence_counter:
            confidence_counter = results[i].ordered_statistics[j].confidence
            confidence_index = j

        # Check if 'results[i].ordered_statistics[j].lift' is higher than 'lift_counter'.
        # If so, replace 'lift_counter' and 'lift_index'.
        if results[i].ordered_statistics[j].lift >= lift_counter:
            lift_counter = results[i].ordered_statistics[j].lift
            lift_index = j

    # If the 'confidence_counter' or 'lift_counter' (the highest confidence and lift respectively
    # in 'results[i].ordered_statistics[j]') are higher than 'confidence_cutoff' or 'lift_cutoff'
    # the record combo is added to 'high_confidence' or 'high_lift'.
    if confidence_counter >= confidence_cutoff:
        high_confidence.append([i, j])
    if lift_counter >= lift_cutoff:
        high_lift.append([i, j])

# For an element of a list of form [i, j], the corresponding record can be viewed by using:
# results[i].ordered_statistics[j]

    

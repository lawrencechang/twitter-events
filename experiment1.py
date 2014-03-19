from processdata import *

print 'Running Experiment 1.';

# Make sure I can actually use the functions from the processdata.py file
#list = findFollowersOf('lawchang');
#print list;

# Generate keyword list for the Miami Heat
miamiHeatKeywords = findRelatedWordsForTeam(['miami heat','the heat','#heat']);
# Result: top keywords, in order:
  # :, RT, Heat, LeBron, Miami, James, heat, game, time, NBA, ...
  # Probably want to get rid of :, RT at some point

# Get a list of followers from the Miami Heat, say 1,000
# @MiamiHEAT
miamiHeatFollowers = findFollowersOf('miamiheat');
  # unnecessarily sorted, but whatever

# From this list, get the top 20 users who match the keyword list


# Then, from this same list (or a new list), select 20 random users.

# Manually compare

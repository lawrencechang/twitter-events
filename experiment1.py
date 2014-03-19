from processdata import *
import pickle;

def makeCollection(tokenizedTweets):
    nouns  = [];
    for tupl in tokenizedTweets:
        for token in tupl:
            tokenList = list(token)                                
            t       =  tokenList[0]            
            typ     =  tokenList[1]
            if typ in NOUN:
                nouns.append(t)
    mycounter = collections.Counter();
    mycounter.update(nouns)
    return mycounter;
        

print 'Running Experiment 1.';

# Make sure I can actually use the functions from the processdata.py file
#list = findFollowersOf('lawchang');
#print list;

# Generate keyword list for the Miami Heat
seedKeywords = ['miami heat','the heat','#heat'];
print 'The seed keywords are:';
print seedKeywords;
miamiHeatKeywords = [];
# Getting the top 20 keywords, removing the counts
# Read from file to save API calls
readFromFile = True;
if readFromFile:
    print 'Reading miamiHeatKeywords from file.';
    with open('miamiHeatKeywords.pickle') as f:
        miamiHeatKeywords = pickle.load(f);
else:
    print 'Generating new miamiHeatKeywords list.';
    #miamiHeatKeywords = tuple(element[0] for element in findRelatedWordsForTeam(seedKeywords).most_common(20));
    miamiHeatKeywords = findRelatedWordsForTeam(seedKeywords).most_common(20);
if len(miamiHeatKeywords) == 0:
    print 'Didnt find any keywords, exiting.';
    raise SystemExit;
else:
    with open('miamiHeatKeywords.pickle','w') as f:
        pickle.dump(miamiHeatKeywords,f);

# Make this a collection
miamiHeatKeywordsCollection = collections.Counter();
miamiHeatKeywordsCollection.update([element[0] for element in miamiHeatKeywords]);

# Result: top keywords, in order:
  # :, RT, Heat, LeBron, Miami, James, heat, game, time, NBA, ...
  # Probably want to get rid of :, RT at some point

# Get a list of followers from the Miami Heat, say 1,000
# @MiamiHEAT
print 'Getting followers of @miamiheat.';
miamiHeatFollowers = tuple(element[0] for element in findFollowersOf('miamiheat'));
  # unnecessarily sorted, but whatever
print 'Got '+str(len(miamiHeatFollowers))+' followers.';

# From this list, get the top 20 users who match the keyword list
# Make a list of tuples like (username, score)
print 'Scoring followers.';
userScores = [];
for i,user in enumerate(miamiHeatFollowers):
    print 'Getting tweets for user '+str(i)+'. '+user;
    usersTweets = findAllUserTweets(user);
    if len(usersTweets) == 0:
        print 'Couldnt find any Tweets for this user.';
    else:
        usersTweetsTokenized = runtagger_parse(usersTweets);
        usersTweetsCollection = makeCollection(usersTweetsTokenized);
    
        print 'Scoring user.';
        userScores.append([user,counter_cosine_similarity(usersTweetsCollection,miamiHeatKeywordsCollection)]);


# Then, from this same list (or a new list), select 20 random users.

# Manually compare

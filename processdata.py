import csv
import collections
from twython import Twython
from sets import Set
from twython.exceptions import TwythonError
from CMUTweetTagger import runtagger_parse

APP_KEY = 'APP_KEY'
APP_SECRET = 'APP_SECRET'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

KEYWORDS = []
NUMERAL  = ['$']
NOUN     = ['^','N','@','#','~']

USERS = Set([])
USER_DATASET_PATH = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/data/'
TWEETNOUNS        = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tweetNouns/'
FOLLOWER_PATH     = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/follower/'

#-----------------------------------------------
# Returns the 1o most frequently appearing words 
# from the inputFile. 
#-----------------------------------------------
def wordCounter(inputFile):    
    mycounter = collections.Counter();        
    # Update counter with new line
    with open(inputFile,'r') as file:
        for line in file:
            mycounter.update(line.split());
    file.closed        
    return mycounter.most_common(10);


#-----------------------------------------------
# Saves extracted tweets to file 
#-----------------------------------------------
def saveTweets(listOfTweets,outputFile):
    if outputFile:    
        outFile = open(outputFile, 'w')
        for tweet in listOfTweets:
            if outputFile:
                print>> outFile, tweet['text']    
        outFile.close()
    else:
        for tweet in listOfTweets:
            username = tweet['user']['screen_name']
            tweet    = tweet['text']            
            print username,tweet
            USERS.add(username)


#-----------------------------------------------
# Save parsed tweets to file
#-----------------------------------------------
def saveParsedTweets(nounList,outputFile):
    if outputFile:    
        outFile = open(outputFile, 'w')
        for tweet in nounList:
            if outputFile:
                print>> outFile, tweet['text']    
        outFile.close()
        

#-----------------------------------------------
# Extract the 200 recent tweets from a  
# Twitter user account
#-----------------------------------------------
def twitterExtractUserTimeline(name,path):    
    try:
        twitter = Twython(APP_KEY, APP_SECRET)
        user_timeline = twitter.get_user_timeline(screen_name=name, count=200 )
        outputFilePath = path + name                    
        saveTweets(user_timeline,outputFilePath)
    except TwythonError as e:
        print e  


#-----------------------------------------------
# Extracts recent tweets from a list of users    
#-----------------------------------------------
def findUserTweets(keyword):    
    twitterCheck( keyword,None )
    for u in USERS:
        twitterExtractUserTimeline(u,USER_DATASET_PATH)


#-----------------------------------------------
# Get a list of users whose tweets contain
# a keyword
#-----------------------------------------------                
def usersByKeywordGet(query):
    twitter = Twython(APP_KEY, APP_SECRET)
    popularTweets =  twitter.search(q=query,  count=30, lang = 'en', include_entities= False)
    listOfTweets  =  popularTweets["statuses"]
    res = []    
    for tweet in listOfTweets:
        username = tweet['user']['screen_name']
        tweet    = tweet['text']                        
        res.append(username)
    return res        


#-----------------------------------------------
# Gets a list of tweets from users who have a tweet
# that contains a keyword
#-----------------------------------------------                        
def findAllUserTweets(keyword):
    twitter = Twython(APP_KEY, APP_SECRET)    
    users   = usersByKeywordGet(keyword)
    tweetList = []
    for u in users:        
        user_timeline = twitter.get_user_timeline(screen_name=u, count=15 )                        
        for tweet in user_timeline:
            tweetList.append( tweet['text'] )
    return tweetList


#-----------------------------------------------
# Gets a list of tweets from users who have a tweet
# that contains a keyword
#-----------------------------------------------                        
def findAllRelatedWordsForKeywords(keywords):
    try:
        allTweets = []
        for w in keywords:            
            tweets = findAllUserTweets(w)            
            allTweets = list(set(tweets + allTweets ))            
        nouns  = []    
        tokenizedTweets = runtagger_parse(allTweets)            
        for tupl in tokenizedTweets:
            for token in tupl:
                tokenList = list(token)                                
                t       =  tokenList[0]            
                typ     =  tokenList[1]
                if typ in NOUN:
                    nouns.append(t)
        return nouns
    except TwythonError as e:
        print e


#-----------------------------------------------
# Counts the number of times 
# every word appears in a list 
#-----------------------------------------------                        
def counterForWordsGet(nouns):
    mycounter = collections.Counter();
    mycounter.update(nouns)
    print mycounter.most_common(20);
    return mycounter


#-----------------------------------------------
# Find recent tweets by users who have tweets  
# that contain a keyword, and count the number
# of times each word appears in those tweets
#-----------------------------------------------                            
def findRelatedWordsForTeam(keywords):
    nouns = findAllRelatedWordsForKeywords(keywords)    
    return counterForWordsGet(nouns)


#-----------------------------------------------
# Finds tweets that contain a certain keyword
# and save them to a file
#-----------------------------------------------      
def twitterCheck( query, outputFile ):
    twitter = Twython(APP_KEY, APP_SECRET)
    popularTweets =  twitter.search(q=query,  count=100, lang = 'en', include_entities= False)
    listOfTweets  =  popularTweets["statuses"]    
    print "Fetched ",len(listOfTweets)," tweets."
    saveTweets(listOfTweets,None)


#-----------------------------------------------
# Finds followers of a specific user 
# that have the most followers
#-----------------------------------------------          
def findFollowersOf(user):
    twitter = Twython(APP_KEY, APP_SECRET);
    followerList = [];    
    # Cursoring over follower pages    
    mycursor = -1;
    for i in range(0,5):
        print 'Cursor page '+str(i);
        f = twitter.get_followers_list(
            screen_name=user,cursor=mycursor,count=20,skip_status='true',include_user_entities='true');        
        for follower in f['users']:
            followerList.append((follower['screen_name'],follower['followers_count']));
        mycursor = f['next_cursor'];
    print 'Got list, sorting'
    return sorted(followerList,key=lambda followers:followers[1],reverse=True);


#-----------------------------------------------
# Find the last 800 tweets of a follower  
#-----------------------------------------------
def findLastTweetsOfFollower(followerName):
    twitter = Twython(APP_KEY, APP_SECRET)    
    nouns  = []
    tweets = []
    i      = 0
    try:
        user_timeline = twitter.get_user_timeline(screen_name=followerName, count=200 )
        low_id        = user_timeline[0]['id']                    
        for tweet in user_timeline:            
            cur_id  = tweet['id']
            if low_id > cur_id:
                low_id = cur_id                                                    
            tweet   = tweet['text']                                
            tweets.append(tweet)                                                                            
        for i in range (0,3):
            user_timeline = twitter.get_user_timeline(screen_name=followerName, max_id= low_id, count=200 )                                        
            for tweet in user_timeline:                
                cur_id  = tweet['id']
                if low_id > cur_id:
                    low_id = cur_id                                                    
                tweet   = tweet['text']                                    
                tweets.append(tweet)                                                                                    
        tokenizedTweets = runtagger_parse(tweets)            
        for tupl in tokenizedTweets:
            for token in tupl:
                tokenList = list(token)                
                t       =  tokenList[0]            
                typ     =  tokenList[1]
                if typ in NOUN:                    
                    nouns.append(t)                            
            i+=1                                    
        mycounter = collections.Counter();
        mycounter.update(nouns)
        print mycounter.most_common(20);
        return mycounter
    except TwythonError as e:
        print e


#-----------------------------------------------
# Find the cosine similarity between two python
# collections
#-----------------------------------------------
import math
def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


#-----------------------------------------------
# Find elements that are in the inputList but
# not in the comparedToList
#-----------------------------------------------    
def findWordsNotInIntersection(inputList,comparedToList):
    res = [val for val in inputList if val not in comparedToList]
    return res        

        

def experiment2A():
    entity = findRelatedWordsForTeam(['Kobe Bryant'])
    teamA  = findRelatedWordsForTeam(['lakers'])    
    teamB  = findRelatedWordsForTeam(['san antonio spurs'])
    teamC  = findRelatedWordsForTeam(['miami hit'])
    print counter_cosine_similarity(entity, teamA)
    print counter_cosine_similarity(entity, teamB)    
    print counter_cosine_similarity(entity, teamC)


def experiment2B():
    entity = findRelatedWordsForTeam(['Kobe Bryant'])
    teamA  = findRelatedWordsForTeam(['lakers','LAL','Los Angeles Lakers'])    
    teamB  = findRelatedWordsForTeam(['celtics','BOS','Boston Celtics'])
    teamC  = findRelatedWordsForTeam(['clippers','LAC','Los Angeles Clippers'])
    print counter_cosine_similarity(entity, teamA)
    print counter_cosine_similarity(entity, teamB)    
    print counter_cosine_similarity(entity, teamC)


def experiment3A():
    teamA = findRelatedWordsForTeam(['lakers'])    
    teamB = findRelatedWordsForTeam(['celtics'])
    teamC = findRelatedWordsForTeam(['clippers'])        
    print counter_cosine_similarity(teamB, teamA)
    print counter_cosine_similarity(teamA, teamC)
    print counter_cosine_similarity(teamC, teamB)


def experiment3B():
    teamA = findRelatedWordsForTeam(['lakers','LAL','Los Angeles Lakers'])    
    teamB = findRelatedWordsForTeam(['celtics','Boston Celtics'])
    teamC = findRelatedWordsForTeam(['clippers','LAC','Los Angeles Clippers'])
    print counter_cosine_similarity(teamB, teamA)
    print counter_cosine_similarity(teamA, teamC)
    print counter_cosine_similarity(teamC, teamB)


def experiment4():    
    initTeamA = findAllRelatedWordsForKeywords(['lakers'])    
    initTeamB = findAllRelatedWordsForKeywords(['celtics'])
    filteredTeamA = findWordsNotInIntersection(initTeamA,initTeamB)
    filteredTeamB = findWordsNotInIntersection(initTeamB,initTeamA)            
    teamA  = counterForWordsGet(filteredTeamA)
    teamB  = counterForWordsGet(filteredTeamB)
    teamC  = findRelatedWordsForTeam(['clippers'])    
    entity = findRelatedWordsForTeam(['Kobe Bryant'])    
    print counter_cosine_similarity(entity, teamA)
    print counter_cosine_similarity(entity, teamB)    
    print counter_cosine_similarity(entity, teamC)    
    print counter_cosine_similarity(teamA, teamB)
    print counter_cosine_similarity(teamB, teamC)    
    print counter_cosine_similarity(teamA, teamC)        


if __name__ == '__main__':    
    experiment2A()    
    experiment2B()
    experiment3A()
    experiment3B()
    experiment4()

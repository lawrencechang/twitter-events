import csv
import collections
from twython import Twython
from sets import Set
from twython.exceptions import TwythonError

APP_KEY = 'eiKbuTUzZ7G4cN1NrAcU6Q'
APP_SECRET = '06lT99eKgIke0ZHczBA2wiXawvNwEKBSGUm5wiELY'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

KEYWORDS = []
NUMERAL = ['$']
NOUN    = ['^','N','@','#','~']

USERS = Set([])
USER_DATASET_PATH = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/data/'
TWEETNOUNS = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tweetNouns/'
FOLLOWER_PATH = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/follower/'

#-----------------------------------------------
# Returns the 1o most frequently appearing words 
# from the inputFile. 
#-----------------------------------------------
def wordCounter(inputFile):
    # Create counter object, initialize to nothing
    mycounter = collections.Counter();    
    # In a loop, read each line
    # Update counter with new line
    with open(inputFile,'r') as file:
        for line in file:
            mycounter.update(line.split());
    file.closed    
    # Print counter results
    return mycounter.most_common(10);

from os import listdir
from os.path import isfile, join
def processUsers(mypath):
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]    
    outFileName = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/results.txt'
    outFile = open(outFileName, 'w')
    for f in onlyfiles:
        filePath = USER_DATASET_PATH + f
        result = wordCounter(filePath)
        print f, result
        print>> outFile, f,result
    outFile.close()        

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

def saveParsedTweets(nounList,outputFile):
    if outputFile:    
        outFile = open(outputFile, 'w')
        for tweet in nounList:
            if outputFile:
                print>> outFile, tweet['text']    
        outFile.close()
    
    

def twitterExtractUserTimeline(name,path):    
    try:
        twitter = Twython(APP_KEY, APP_SECRET)
        user_timeline = twitter.get_user_timeline(screen_name=name, count=200 )
        outputFilePath = path + name                    
        saveTweets(user_timeline,outputFilePath)
#        for tweet in user_timeline:
#            print tweet["text"]
    except TwythonError as e:
        print e


def findUserTweets(keyword):    
    twitterCheck( keyword,None )
    for u in USERS:
        twitterExtractUserTimeline(u,USER_DATASET_PATH)


def findTweetsByTime( query, time, outputFile ):
    twitter = Twython(APP_KEY, APP_SECRET)
    popularTweets =  twitter.search(q=query,  count=100, lang = 'en', 
                                    until = time, result_type = 'recent', include_entities= False)
    listOfTweets  =  popularTweets["statuses"]    
    print "Fetched ",len(listOfTweets)," tweets."
    saveTweets(listOfTweets,None)

    
def twitterCheck( query, outputFile ):
    twitter = Twython(APP_KEY, APP_SECRET)
    popularTweets =  twitter.search(q=query,  count=100, lang = 'en', include_entities= False)
    listOfTweets  =  popularTweets["statuses"]    
    print "Fetched ",len(listOfTweets)," tweets."
    saveTweets(listOfTweets,None)

            
def twitterSearch():
    twitter = Twython( APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)        
    twitter.search(q='twitter')
    twitter.search(q='twitter', result_type='popular')

    
def extractKeywords(keywordsFile,savedTweetsFile):
    file_str = open( keywordsFile ).read()
    seq = file_str.split('\n')
    log_file = open( savedTweetsFile, 'w' )
    i = 0 
    print 'There are ',len(seq), ' tweets'
    for line in seq:
        if line:
            print i,line
            #print>> log_file, line
            twitterCheck(line,log_file)
            i+=1 
    log_file.close()


def loadKeywords(keywordsFile):
    #file_str = open( '/home/tomerwei/Downloads/keywords.txt').read()
    file_str = open( keywordsFile ).read()
    seq = file_str.split('\n')    
    i = 0 
    print 'There are ',len(seq), ' tweets'
    for line in seq:
        if line:
            KEYWORDS.append(line.lower())            
    file_str.close()

    
def initialStatesRead():
    with open('/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tokenized/adidas_227.out', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        TWEET_ID_COUNTER = 0        
        for r in spamreader:            
            row = r[0].split('\t')
            tokens      = row[0].split(' ')            
            tokensTypes = row[1].split(' ')
            tweet       = row[2]            
            i = 0            
            for typ in tokensTypes:                            
                if typ in NOUN:                    
                    if tokens[i].lower() in KEYWORDS:
                        print tokens[i], "|",tweet, TWEET_ID_COUNTER                                                    
                i+=1                                        
            TWEET_ID_COUNTER+=1    
            
            
def nounFinder(infile):
    tweet_nouns = []
    with open(infile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        TWEET_ID_COUNTER = 0        
        for r in spamreader:            
            row = r[0].split('\t')
            tokens      = row[0].split(' ')            
            tokensTypes = row[1].split(' ')
            tweet       = row[2]            
            i = 0

            for typ in tokensTypes:                            
                if typ in NOUN:                    
                    tweet_nouns.append(tokens[i])                
                i+=1                                                                                
            TWEET_ID_COUNTER+=1
    return tweet_nouns                 


def refCountGet(mypath):
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]            
    res = []
    for f in onlyfiles:
        nouns = nounFinder(mypath + f)
        res += nouns        
    ##for r in res:
    ##    print r            
    mycounter = collections.Counter();    
    mycounter.update(nouns);
    print mycounter.most_common(17);
    return mycounter

    
def findFollowersOf(user):
    twitter = Twython(APP_KEY, APP_SECRET);
    followerList = [];    
    # Proper cursoring
    print 'Proper cursoring'
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
            

from CMUTweetTagger import runtagger_parse
def findLastTweetsOfFollower(followerName):
    try:
        twitter = Twython(APP_KEY, APP_SECRET)
        user_timeline = twitter.get_user_timeline(screen_name=followerName, count=1000 )        
        tweets = []
        nouns  = []
        print len(user_timeline)
        for tweet in user_timeline:            
            tweet    = tweet['text']                        
            tweets.append(tweet)                
        tokenizedTweets = runtagger_parse(tweets)
        i=0
        for tupl in tokenizedTweets:
            #print '----------'
            for token in tupl:
                tokenList = list(token)                
                #print tokenList[0], tokenList[1]
                t       =  tokenList[0]            
                typ     =  tokenList[1]
                tweet   =  tweets[i]
                if typ in NOUN:                    
                    #print t, typ, "|",tweet, i
                    nouns.append(t)                            
            i+=1            
        mycounter = collections.Counter();
        mycounter.update(nouns)
        print mycounter.most_common(20);
        return mycounter
    except TwythonError as e:
        print e


import math
def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


if __name__ == '__main__':
    #print 'hello world'
    #extractKeywords('/home/tomerwei/Downloads/keywords.txt','/home/tomerwei/Downloads/superlog.txt')
    #loadKeywords( '/home/tomerwei/Downloads/keywords.txt' )
    #print KEYWORDS
    #findUserTweets('lakers')
    #processUsers(USER_DATASET_PATH)    
    #initialStatesRead()
    #twitterCheck('UCLA', None)
    #findTweetsByTime('Lakers', '2014-03-03',None) #YYYY-MM-DD
    followers = findFollowersOf('lakers')
    print followers
    counter1 = refCountGet('/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tokenized/')   
    counter2 = findLastTweetsOfFollower("AngryLakersFan")
    
    print counter_cosine_similarity(counter1, counter2)

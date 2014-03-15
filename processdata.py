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
USERSDATA = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/data/'
TWEETNOUNS = '/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tweetNouns/'



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
        filePath = USERSDATA + f
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
    
    

def twitterExtractUserTimeline(name):    
    try:
        twitter = Twython(APP_KEY, APP_SECRET)
        user_timeline = twitter.get_user_timeline(screen_name=name, count=200 )
        outputFilePath = USERSDATA + name
        print    outputFilePath              
        saveTweets(user_timeline,outputFilePath)
#        for tweet in user_timeline:
#            print tweet["text"]
    except TwythonError as e:
        print e


def findUserTweets():
    twitterCheck("lakers",None)
    
    for u in USERS:
        twitterExtractUserTimeline(u)


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

    
def extractKeywords():
    file_str = open( '/home/tomerwei/Downloads/keywords.txt').read()
    seq = file_str.split('\n')
    log_file = open('/home/tomerwei/Downloads/superlog.txt', 'w')
    i = 0 
    print 'There are ',len(seq), ' tweets'
    for line in seq:
        if line:
            print i,line
            #print>> log_file, line
            twitterCheck(line,log_file)
            i+=1 
    log_file.close()


def loadKeywords():
    file_str = open( '/home/tomerwei/Downloads/keywords.txt').read()
    seq = file_str.split('\n')
    log_file = open('/home/tomerwei/Downloads/superlog.txt', 'w')
    i = 0 
    print 'There are ',len(seq), ' tweets'
    for line in seq:
        if line:
            KEYWORDS.append(line.lower())            
    log_file.close()

    
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
            
            
def nounFinder(file):
    tweet_nouns = []
    with open(file, 'rb') as csvfile:
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

    for r in res:
        print r
            
    mycounter = collections.Counter();    
    mycounter.update(nouns);
    print mycounter.most_common(17);

    #print res
    if 0:
        nouns = nounFinder('/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tokenized/CoachKSnyd.out')
        mycounter = collections.Counter();    
        mycounter.update(nouns);
        print mycounter.most_common(17);
    
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
        
    # f['users'][0]['screen_name']
                
#Main Function
if __name__ == '__main__':
    
    
    #print 'hello world'
    #extractKeywords()
    #loadKeywords()
    #print KEYWORDS
    #findUserTweets()
    #processUsers(USERSDATA)
    #twitterExtractUserTimeline('MileyCyrus')
    #initialStatesRead()
    #twitterCheck('UCLA', None)
    #findTweetsByTime('Lakers', '2014-03-03',None) #YYYY-MM-DD
    
    #refCountGet('/home/tomerwei/UCLA_assignments/CS263A/twitter-events/tokenized/')
    
    followers = findFollowersOf('lakers');
    

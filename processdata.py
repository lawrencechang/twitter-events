import csv
from twython import Twython
from twython.exceptions import TwythonError

APP_KEY = 'eiKbuTUzZ7G4cN1NrAcU6Q'
APP_SECRET = '06lT99eKgIke0ZHczBA2wiXawvNwEKBSGUm5wiELY'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''



KEYWORDS = []
NUMERAL = ['$']
NOUN    = ['^','N','@','#','~']


def twitterCheck( query, outputFile ):
    twitter = Twython(APP_KEY, APP_SECRET)
    popularTweets =  twitter.search(q=query,  count=100, lang = 'en', include_entities= False)
    listOfTweets  =  popularTweets["statuses"]
    
    print "Fetched ",len(listOfTweets)," tweets."
    for tweet in listOfTweets:
        print>> outputFile, tweet["text"]                               

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
    with open('/home/tomerwei/UCLA_assignments/CS263A/ark-tweet-nlp-0.3.2/supersprlog.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        allStates       = []            
        for row in spamreader:
            st = []
            if False and len(row) == 0:
                print row            
            if len(row) > 1:
                str = row[0]
                typ = row[1]                            
                if typ in NOUN:                    
                    if str.lower() in KEYWORDS:
                        print str, typ                        
    print KEYWORDS
    print NOUN
            #allStates.append( st )            
        #print allStates
        #stWithOtherAnimatsSensor = statesNumberOfAnimatsSensorAdd(allStates)
        #for s in stWithOtherAnimatsSensor:
        #    print s
        #harvestedFoodStates = findAllFoodHarvestedState(allStates)
    #return allStates,harvestedFoodStates    


#Main Function
if __name__ == '__main__':
    #print 'hello world'
    #extractKeywords()
    loadKeywords()
    print KEYWORDS
    initialStatesRead()
    
    #twitterCheck('UCLA')
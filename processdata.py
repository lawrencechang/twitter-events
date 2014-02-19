from twython import Twython
from twython.exceptions import TwythonError

APP_KEY = 'eiKbuTUzZ7G4cN1NrAcU6Q'
APP_SECRET = '06lT99eKgIke0ZHczBA2wiXawvNwEKBSGUm5wiELY'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

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


#Main Function
if __name__ == '__main__':
    #print 'hello world'
    extractKeywords()
    #twitterCheck('UCLA')
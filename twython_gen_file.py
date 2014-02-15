from twython import Twython

print 'Testing out twython.'

APP_KEY = 'deQC0dqQP46N0XT5hDHHsQ'
APP_SECRET = 'ucG01AX12ydT3eMYn7hNsBLwUj623DIgMs5wE5tVE'

twitter = Twython(APP_KEY, APP_SECRET);

# File set up
file = open('lakers_tweets.txt','w');

searchTerm = 'lakers'
lakersTweets = twitter.search(q=searchTerm,result_type='popular');
print 'Fetched ',len(lakersTweets['statuses']),' tweets.'
for i,tweet in enumerate(lakersTweets['statuses']):
    currentTweet = tweet['text'] + '\n';
    print i,'.',currentTweet;
    file.write(currentTweet.encode('ascii','ignore'));

#searchTerm = 'amanda knox';
#amandaTweets = twitter.search(q=searchTerm,result_type='popular');
#print 'Fetched ',len(amandaTweets['statuses']),' tweets.'
#for i,tweet in enumerate(amandaTweets['statuses']):
#    print i,'.',tweet['text'],'\n';



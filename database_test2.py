from Database.TwitterEventsAPI import TweetsDb;

db  = TweetsDb();

# Assume a db called hello.db has already been created (with the table in it too)

db.connect('hello.db');
print 'Connected to hello.db';

print 'Adding tweet 1 of 5';
db.addTweet(382939,'broncos','seattle seahawks',-1,-1);
print 'Adding tweet 2 of 5';
db.addTweet(382939,'broncos','seattle seahawks',-1,-1);
print 'Adding tweet 3 of 5';
db.addTweet(382939,'broncos','seattle seahawks',-1,-1);
print 'Adding tweet 4 of 5';
db.addTweet(382939,'broncos','seattle seahawks',-1,-1);
print 'Adding tweet 5 of 5';
db.addTweet(382939,'broncos','seattle seahawks',-1,-1);




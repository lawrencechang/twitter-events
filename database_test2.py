from Database.TwitterEventsAPI import TweetsDb;
import sqlite3 as lite;

db  = TweetsDb();

# Assume a db called hello.db has already been created (with the table in it too)

db.connect('hello.db');
print 'Connected to hello.db';

for i in range(0,5):
    print 'Adding tweet '+str(i)+' of 5';
    db.addTweet(400000+i,'broncos','seattle seahawks',-1,-1);

print 'Adding tweet about diff team';
db.addTweet(5000,'','dodgers',100,-2);

# look at the db so far
print 'looking at hello.db';
con2 = lite.connect('hello.db');
with con2:
    print 'picking all tweets';
    cur = con2.cursor();
    cur.execute('select * from Tweets');
    rows = cur.fetchall();
    for row in rows:
        print row;

    print 'picking row id 13';
    cur.execute('select * from Tweets where rowid = 13');
    rows = cur.fetchall();
    for row in rows:
        print row;
    
    print 'trying to test selecting a specific twitter id';
    cur.execute('select * from Tweets where tweetId = 400000');
    rows = cur.fetchall();
    for row in rows:
        print row;


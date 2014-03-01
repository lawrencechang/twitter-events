from Database.TwitterEventsAPI import TweetsDb;
import sqlite3 as lite;

db  = TweetsDb();

# Assume a db called hello.db has already been created (with the table in it too)

db.connect('hello.db');
print 'Connected to hello.db';

print 'Try getting a a specific tweet with tweetId 400000, which might actually be a few';
rows = db.getId(400000);
for row in rows:
    print row;

print 'Try getting tweets with a specific team name';
rows = db.getTeam('broncos');
for row in rows:
    print row;


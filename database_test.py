# create a dummy database
# add some dummy values
# retrieve some stuff

import sqlite3 as lite;

con = lite.connect('dummy.db');

with con:
    cur = con.cursor();

    cur.execute("drop table if exists Tweets");
    cur.execute("CREATE TABLE Tweets(Id INT, tweetId INT, Team1 TEXT, Team2 TEXT, Score1 INT, Score2 INT)");

    for index in range (0,3):
        command = "INSERT INTO Tweets Values(" + str(index) + ","+str(239020+index)+",'Lakers','',32,-1)";
        print command;
        cur.execute(command);

with con:
    cur = con.cursor();
    cur.execute("select * from Tweets where Id=1");

    rows = cur.fetchall();
    for row in rows:
        print row;

# test my API
#import TwitterEventsAPI as db;
from Database.TwitterEventsAPI import TweetsDb;

db = TweetsDb();

db.delete('hello.db');
db.create('hello.db');

db.connect('hello.db');

# look at the db so far
print 'looking at hello.db';
con2 = lite.connect('hello.db');
with con2:
    cur = con2.cursor();
    cur.execute('select * from Tweets');
    rows = cur.fetchall();
    for row in rows:
        print row;

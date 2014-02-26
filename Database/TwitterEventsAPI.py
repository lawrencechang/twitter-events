# File with methods for twitter events database usage

import sqlite3 as lite;

class TweetsDb:

    currentDb = '';

    # Constructor
    def __init__(self):
        currentDb = '';

    # Create an empty database
    # Will fail if a database of the given name already exists
    def create(self,name=''):
        if name == '':
            name = 'default.db';
        con = self.connect(name);

        with con:
            cur = con.cursor();
            cur.execute("create table Tweets(tweetId INT, Team1 TEXT, Team2 TEXT, Score1 INT, Score2 INT)");

    # Delete the Tweets table
    def delete(self,name=''):
        if name == '':
            name = 'default.db';
        con = self.connect(name);

        with con:
            cur = con.cursor();
            cur.execute("drop table if exists Tweets");

    # If the database you want already exists, simply connect to it
    def connect(self,name=''):
        if name == '':
            name = 'default.db';
        self.currentDb = name;
        con = lite.connect(self.currentDb);
        return con;

    def addTweet(self,tweetId,team1,team2,score1,score2):
        # Do some data type checking here
        # So far, it seems the tweet Id's are of type 'int'
        # In the future, it may become 'long'
        if (type(tweetId) is not int or
            type(team1) is not str or
            type(team2) is not str or
            type(score1) is not int or
            type(score2) is not int):
            print "Error in the type(s) of input";
            return;

        con = self.connect(self.currentDb);
        with con:
            cur = con.cursor();
            command = ("insert into Tweets Values("
                       ""+str(tweetId)+',\''+team1+'\',\''+team2+'\','+str(score1)+','+str(score2)+")");
            print command;
            cur.execute(command);

    def getId(self,tweetId):
        # Enforce tweetId is an integer
        if (type(tweetId) is not int):
            print "Tweet Id must be of integer type";
            return;
        con = self.connect(self.currentDb);
        with con:
            cur= con.cursor();
            command = ("select * from Tweets where tweetId="+str(tweetId));
            print command;
            cur.execute(command);

            return cur.fetchall();
        pass;

    def getTeam(self,teamName):
        # Enfore teamName is a string
        if (type(teamName) is not str):
            print "Team name must be of string type";
            return;
        con = self.connect(self.currentDb);
        with con:
            cur = con.cursor();
            command = ("select * from Tweets where "+
                       "Team1=\'"+teamName+"\'"+
                       " or "+
                       "Team2=\'"+teamName+"\'");
            print command;
            cur.execute(command);

            return cur.fetchall();
        pass;

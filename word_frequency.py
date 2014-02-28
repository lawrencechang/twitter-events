import  collections

# Create counter object, initialize to nothing
mycounter = collections.Counter();

# In a loop, read each line
#    Update counter with new line
with open('lakers_tweets.txt','r') as file:
    for line in file:
        mycounter.update(line.split());
file.closed

# Print counter results
print mycounter;

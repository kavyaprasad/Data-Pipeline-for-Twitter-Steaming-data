
#Import the necessary methods from tweepy library
import nltk
nltk.download('punkt')
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import mysql.connector
from mysql.connector import Error
from dateutil import parser
import time

# Enter Twitter API Keys
access_token = "enter access_token"
access_token_secret = "enter access_token_secret"
consumer_key = "enter consumer_key"
consumer_secret = "enter consumer_secret"
tracklist = ['#justinbieber']
tweetChecklist = [];
tweetCount = 0


def connect(created_at, tweet, username,location,retweet):
    """
    connect to MySQL database and insert twitter data
    """
    tweetCount = 0
    try:
        con = mysql.connector.connect(host = 'localhost',
        database='TwitterSchema', user='root', password = 'enter password', charset = 'utf8')
        #print("connected to database")
        tweetCount += 1
        print ("The No. of tweets consumed: %d " % (tweetCount) )
        

        if con.is_connected():
            """
            Insert twitter data
            """
            cursor = con.cursor()
            query = "INSERT INTO TwitterData (created_at, tweet, username,  location,retweet) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (created_at, tweet,username,location, retweet))
            con.commit()
            
            
    except Error as e:
        print(e)

    cursor.close()
    con.close()

    return


# Create the class that will handle the tweet stream
class StdOutListener(StreamListener):

    def on_connect(self):
        print("You are connected to the Twitter API")


    def on_error(self, status_code):
        if status_code != 200:
            print("error found")
            # returning false disconnects the stream
            return False
      
    def on_data(self,data):
        
        try:
            raw_data = json.loads(data)
            if 'text' in raw_data:
                 
                username = raw_data['user']['screen_name']
                created_at = str(parser.parse(raw_data['created_at'])).encode("utf-8")
                tweet = raw_data['text'].encode("utf-8")
                retweet = raw_data['retweet_count']
                location = raw_data['user']['location']
                
                tokens = nltk.word_tokenize(tweet) # Splitting the sentence into words
                banned_words = ['music','Music','MUSIC','#music','#MUSIC','#Music']
                BanWordCheck = bool(sum(map(lambda x: x in banned_words, tokens))) #Variable to track if the keyword 'Music' was found in the tweet
                if tweet not in tweetChecklist and BanWordCheck == False:
                        
                    tweetChecklist.append(tweet)
                    connect(created_at, tweet,username,location, retweet)  #insert data just collected into MySQL database
                    print("Tweet colleted at: {} ".format(str(created_at)))
                        
                else:
                    print("found a duplicate tweet / A word from banned words was found in the tweet: {}".format(str(tweet)))
                    pass
                
        except AttributeError as e:
            print(e)



if __name__ == '__main__':  
# Twitter authetication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=tracklist) #specifying the keywords we want to search on 
    

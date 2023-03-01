import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
from datetime import date


st.subheader("Scrape Tweets with any keywords or Hashtag")
start_date = st.text_input('Start Date in Format YYYY-MM-DD', '2020-01-01')
end_date = st.text_input('End Date in Format YYYY-MM-DD', '2023-01-01')
hashtag = st.text_input('Hashtag to be scraped', 'covid')
tweets_count = int(st.text_input('Number of Tweets Count', '100'))





# Creating an empty list
tweets_list = []
# Enabling the Checkbox only when the hashtag is entered
if hashtag:
    checkbox=st.checkbox("**Scrape Tweets**")
    
    if checkbox:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{hashtag} since:{start_date} until:{end_date}").get_items()):
            if i >= tweets_count:
                break
            tweets_list.append([tweet.date,
                                tweet.id,
                                tweet.url,
                                tweet.rawContent,
                                tweet.user.username,
                                tweet.replyCount,
                                tweet.retweetCount,
                                tweet.likeCount,
                                tweet.lang,
                                tweet.source
                               ])
    else:
        st.text("Nothing to search")
else:
    st.sidebar.checkbox("**Scrape Tweets**",disabled=True)
        
# Creating DataFrame with the scraped tweets
def data_frame(data):
    return pd.DataFrame(data, columns= ['datetime', 'user_id', 'url', 'tweet_content', 'user_name',
                                         'reply_count', 'retweet_count', 'like_count', 'language', 'source'])

# Converting DataFrame to CSV file
def convert_to_csv(c):
    return c.to_csv().encode('utf-8')

# Converting DataFrame to JSON file
def convert_to_json(j):
    return j.to_json(orient='index')

# Creating objects for dataframe and file conversion
df = data_frame(tweets_list)
csv = convert_to_csv(df)
json = convert_to_json(df)

st.text(df)

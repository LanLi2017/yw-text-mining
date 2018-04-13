import tweepy

consumer_key='HbNV8vnqt2VgvyC995CjKmuip'
consumer_secret='v48CskYdo7xNOay168qalR5aCpZR3FoP0iwwAkB9vjjNyEE0Ud'
access_token='968565850063147008-2iBlNabH0Db9hX8XZZt83hewdnZRIfC'
access_token_secret='fMsXgWbzwl7knKLaA7jkJNDPNpiPwNHGTmV2N6rXUW6rz'

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)
public_tweets=api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

user=api.get_user('twitter')
print(user.screen_name)
for friend in user.friends():
    print(friend.screen_name)

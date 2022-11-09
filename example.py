# loads PyTok and JSON module to parse JSON data.
import PyTok as pt
import json

user = 'reddit_a.i.t.a'

# loads user data in a JSON format and then is parsed by the JSON loads module.
user_data = json.loads(pt.full_scrape(user))

print('Name: @'+ user)
print('Followers:', user_data['Followers'])
print('Likes:', user_data['Likes'])
print('Video Views:', user_data['Video Views'])

hasht = 'fyp'

hashtag_data = json.loads(pt.get_hashtag(hasht, video_count=1, full_scrape=True))
user = hashtag_data['1']

# print data for first hashtag in list
print('Username: @'+ user['Username'])
print('Video Link:', user['Link'])
print('Description:', user['Description'])
print('Likes:', user['Likes'])
print('Comments:', user['Comments'])
print('Shares:', user['Shares'])
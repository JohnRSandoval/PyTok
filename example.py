# loads PyTok and JSON module to parse JSON data.
import PyTok as pt
import json

# loads user data in a JSON format and then is parsed by the JSON loads module.
user_data = json.loads(pt.full_scrape("reddit_a.i.t.a"))

print('Name: @reddit_a.i.t.a')
print('Followers:', user_data['Followers'])
print('Likes:', user_data['Likes'])
print('Video Views:', user_data['Video Views'])

print('Name: @reddit_a.i.t.a')
print('Followers:', pt.get_followers("reddit_a.i.t.a"))
print('Likes:', pt.get_likes("reddit_a.i.t.a"))
print('Video Views:', pt.get_video_views("reddit_a.i.t.a"))

# PyTok - Python 3 TikTok API Wrapper

PyTok is the latest python API wrapper for tiktok. More flexibility, more data, more enagement.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyTok.

```bash
pip install PyTok
```

## Usage

```python
import PyTok as pt
import json

# Full Scrape - Get all user data.

# returns '{"Followers": 3183, "Likes": "247200", "Video Views": 3079200}'
No_Comments = json.loads(pt.full_scrape('reddit_a.i.t.a', comments=False))

# returns full_scrape + comments + comment likes. 
# min_likes will default to 0 to show all comments. Comments with likes > or = to the min_likes will be returned.
With_Comments = pt.full_scrape('reddit_a.i.t.a', comments=True, min_likes=1)


#Individual Scrape - Get individual user data.

# returns 247300.
pt.get_likes("reddit_a.i.t.a")
No_Comments['Likes']

# returns 3183.
pt.get_followers('reddit_a.i.t.a')
No_Comments['Followers']

# returns 3079200.
pt.get_video_views('reddit_a.i.t.a')
No_Comments['Video Views']

## *COMMENTS CAN TAKE A LONG TIME TO LOAD DEPENDING ON # of VIDEOS*
# returns "Comments": {'Example Comment': 1}
pt.get_video_views('reddit_a.i.t.a')
With_Comments['Comments']

# Hashtag Scrape - Get hashtag data.

# reutrns 'Username, Video Link, Description' full_scrape returns [likes, comments, shares]
hashtag_data = json.loads(pt.get_hashtag('fyp', video_count=1, full_scrape=True))

# get the first dataset from the JSON object and set it to user
user = hashtag_data['1']

# print data for first hashtag in list
print('Username: @'+ user['Username'])
print('Video Link:', user['Link'])
print('Description:', user['Description'])
print('Likes:', user['Likes'])
print('Comments:', user['Comments'])
print('Shares:', user['Shares'])


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits
All rights reserved by John Sandoval. Creator of PyTok 2022.
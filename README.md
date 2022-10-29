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

#Full Scrape - Return all user data.

# returns '{"Followers": 3183, "Likes": "247200", "Video Views": 3079200}'
No_Comments = json.loads(pt.full_scrape('reddit_a.i.t.a', comments=False))

#*COMMENTS CAN TAKE A LONG TIME TO LOAD DEPENDING ON # of VIDEOS*
# returns full_scrape + comments + comment likes. 
#'{"Followers": 3183, "Likes": "247200", "Video Views": 3079200, "Comments": {'Example Comment': 1}}'
# min_likes will default to 0 to show all comments. Comments with likes > or = to the min_likes will return.
With_Comments = pt.full_scrape('reddit_a.i.t.a', comments=True, min_likes=1)


#Individual Scrape - Return individual user data.

# returns 247300.
pt.get_likes("reddit_a.i.t.a")
No_Comments['Likes']

# returns 3183.
pt.get_followers('reddit_a.i.t.a')
No_Comments['Followers']

# returns 3079200.
pt.get_video_views('reddit_a.i.t.a')
No_Comments['Video Views']

#*COMMENTS CAN TAKE A LONG TIME TO LOAD DEPENDING ON # of VIDEOS*
# returns "Comments": {'Example Comment': 1}
pt.get_video_views('reddit_a.i.t.a')
No_Comments['Comments']

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits
All rights reserved by John Sandoval. Creator of PyTok 2022.
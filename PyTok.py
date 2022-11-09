# imports
from selenium import webdriver
import time
import warnings
import json
from webdriver_manager.chrome import ChromeDriverManager

# ignore deprication warnings from selenium
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Chrome Arguments, initialize options and arguments
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--log-level=3')
#chrome_options.add_argument("--headless")

# load chrome using playwright
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
time.sleep(1)
driver.switch_to.window(driver.window_handles[0])

#function to convert string to int, multiples k by 1k, m by 1m
def convert_to_int(number):
    if 'K' in number:
        number = number.replace('K', '')
        number = int(float(number) * 1000)
    elif 'M' in number:
        number = number.replace('M', '')
        number = int(float(number) * 1000000)
    else:
        number = int(float(number))
    return number

# global variables
global_links = []

# format numbers with commas
def numformat(number):
    return format(int(number), ",")    

# returns all video links for a tiktok profile
def get_video_links(username, load_profile=True):
    global global_links
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    video_links = driver.find_elements_by_xpath('//a[contains(@href, "https://www.tiktok.com/@{}/video/")]'.format(username))
    for x in video_links:
        global_links.append(x.get_attribute('href'))
    return video_links

# returns all comments on a tiktok profile
def get_comments(username, load_profile=True, min_likes=0):
    global global_links
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    get_video_links(username, False)
    comment_dict = {}
    for link in global_links:
        driver.get(link)
        # implicility wait for page to load
        driver.implicitly_wait(2)
        scroll_to_bottom(80)
        comments = driver.find_elements_by_xpath('//p[@data-e2e="comment-level-1"]')
        comment_likes = driver.find_elements_by_xpath('//span[@data-e2e="comment-like-count"]')
        for i in range(len(comments)):
            if convert_to_int(comment_likes[i].text) >= min_likes:
                comment_dict[comments[i].text] = convert_to_int(comment_likes[i].text)
    return comment_dict

# returns total video views for a tiktok profile
def get_video_views(username, load_profile=True):
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    video_views = driver.find_elements_by_xpath('//strong[@data-e2e="video-views"]')
    total_views = 0
    for view in video_views:
        total_views += convert_to_int(view.text)
    return total_views


def scroll_to_bottom(scrolltime=0):
    scrolltime = round(scrolltime/15)
    if scrolltime > 0:
        for i in range(scrolltime):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

# loads a tiktok profile in selenium and scrolls to the bottom of the page to load all videos
def load_tiktok_profile(username):
    driver.get("https://www.tiktok.com/@{}?lang=en".format(username))
    driver.implicitly_wait(1)
    page_scroll()

# loads each video in the hashtag list and gets the likes, comments, and shares
def full_hashtag_getter_done():
    global global_links
    likes = []
    comments = []
    shares = []
    for link in global_links:
        driver.get(link)
        driver.implicitly_wait(2)
        likes.append(numformat(convert_to_int(driver.find_element_by_xpath('//strong[@data-e2e="like-count"]').text)))
        comments.append(numformat(convert_to_int(driver.find_element_by_xpath('//strong[@data-e2e="comment-count"]').text)))
        shares.append(numformat(convert_to_int(driver.find_element_by_xpath('//strong[@data-e2e="share-count"]').text)))
    return likes, comments, shares

# main get_hashtag function; returns all hashtag data, user, links, description, full_scrape[likes, comments, shares]
def get_hashtag(hashtag, video_count=15, full_scrape=False):
    global global_links
    links = load_hashtag(hashtag, video_count)
    usernames, description = load_hashtag_username_desc(video_count)
    likes, comments, shares = '', '', ''
    if full_scrape:
        global_links = links
        likes, comments, shares = full_hashtag_getter_done()
    fd = json.dumps(format_dict(usernames, links, description, likes, comments, shares))
    return fd


# returns username list for a hashtag search
def load_hashtag_username_desc(video_count=15):
    usernames = driver.find_elements_by_xpath('//h4[@data-e2e="challenge-item-username"]')
    desc = driver.find_elements_by_xpath('//a[contains(@title, "#")]')
    user_list = [] 
    desc_list = []
    for i in range(video_count):
        user_list.append(usernames[i].text)
        desc_list.append(desc[i].get_attribute('title'))
    return user_list, desc_list

# loads a hashtag in selenium and uses scroll to bottom to x# videos
def load_hashtag(hashtag, video_count):
    driver.get("https://www.tiktok.com/tag/{}".format(hashtag))
    driver.implicitly_wait(1.5)
    if round(video_count/15) > 0:
        scroll_to_bottom(video_count)
    video_links = driver.find_elements_by_xpath('//a[contains(@href, "video")]')
    video_list = []
    real_count = -1
    for i in range(video_count):
        real_count += 1
        if 'StyledLink' in video_links[real_count].get_attribute('class'):
            real_count += 1
        video_list.append(video_links[real_count].get_attribute('href'))
    return video_list

# Format Dictionary for JSON
def format_dict(usernames, links, desc, likes, comments, shares):
    fd = {}
    for i in range(len(usernames)):
        if likes != '' or comments != '' or shares != '':
            fd[i+1] = {"Username": usernames[i], "Link": links[i], 'Description': desc[i], 'Likes': likes[i], 'Comments': comments[i], 'Shares': shares[i]}
        else:
            fd[i+1] = {"Username": usernames[i], "Link": links[i], 'Description': desc[i]}
    return fd


# scrolls to the bottom of the tiktok profile page until all videos are loaded
def page_scroll():
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

# returns total followers for a tiktok profile
def get_followers(username, load_profile=True):
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    followers = driver.find_element_by_xpath('//strong[@data-e2e="followers-count"]').text
    return convert_to_int(followers)


# returns total likes for a tiktok profile
def get_likes(username, load_profile=True):
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    likes = driver.find_element_by_xpath('//strong[@data-e2e="likes-count"]').text
    return json.dumps(convert_to_int(likes))

# Main Scraping Function for TikTok Profile will return all data.
def full_scrape(username, comments=False, min_likes=0):
    load_tiktok_profile(username)
    dict= {}
    dict['Followers'] = get_followers(username, False)
    dict['Likes'] = get_likes(username, False)
    dict['Video Views'] = get_video_views(username, False) 
    if comments:
        comment_dict = get_comments(username, False, min_likes)
        dict["Comments"] = comment_dict
    return(json.dumps(dict))
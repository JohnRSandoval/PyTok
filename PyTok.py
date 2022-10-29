from pickle import TRUE
from selenium import webdriver
import time
import warnings
import json
from webdriver_manager.chrome import ChromeDriverManager
# ignore only deprication warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# add chrome options to the webdriver to mute the browser and launch with adblock.crx plugin enabled.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--log-level=3')
# add a chrome option to make the browser headless.
chrome_options.add_argument("--headless")
# load chrome using playwright
driver = webdriver.Chrome(ChromeDriverManager(version="106.0.5249.119").install(), options=chrome_options)
time.sleep(1)
driver.switch_to.window(driver.window_handles[0])

# create a function that takes a number as an input. If the number has a 'k' * 1000 or 'm' * 1000000, then convert the number to an integer.
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

global_links = []

# create a function titled formatter that takes a number as an input and returns the number as a string with commas. Cannot specify ',' with 's'.
def formatter(number):
    return f'{number:,}'    

def get_video_links(username, load_profile=True):
    global global_links
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    video_links = driver.find_elements_by_xpath('//a[contains(@href, "https://www.tiktok.com/@{}/video/")]'.format(username))
    for x in video_links:
        global_links.append(x.get_attribute('href'))
    return video_links

# create a function that opens each video link and creates a dictionary of the comments and the number of likes on a comment if the number of likes is over 5. To find the comments, use xpath to locate the p tags with the data-e2e="comment-level-1" attribute. To find the comment likes, use xpath to find the span tags with the data-e2e="comment-like-count" attribute.
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
        scroll_to_bottom()
        comments = driver.find_elements_by_xpath('//p[@data-e2e="comment-level-1"]')
        comment_likes = driver.find_elements_by_xpath('//span[@data-e2e="comment-like-count"]')
        for i in range(len(comments)):
            if convert_to_int(comment_likes[i].text) >= min_likes:
                comment_dict[comments[i].text] = convert_to_int(comment_likes[i].text)
    return comment_dict

# create a function that loads a tiktok profile page and returns the number of video views. Use xpath to locate the strong tags with the data-e2e"video-views" attribute. Sum the total number of views.
def get_video_views(username, load_profile=True):
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    video_views = driver.find_elements_by_xpath('//strong[@data-e2e="video-views"]')
    total_views = 0
    for view in video_views:
        total_views += convert_to_int(view.text)
    return total_views

# create a function that scrolls till it reaches the bottom of the page. If the page is inifinite scroll, then stop after 5 scrolls.+
def scrolling():
    scroll = 0
    while scroll < 5:
        scroll_to_bottom()
        scroll += 1


# create a function that scrolls and loops until it reaches the bottom of the page.
def scroll_to_bottom():
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        scroll = 0
        while(match==False):
            lastCount = lenOfPage
            time.sleep(.5)
            scroll += 1
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

# create a function that takes a tiktok username as an input and loads the tiktok profile page.
def load_tiktok_profile(username):
    driver.get("https://www.tiktok.com/@{}?lang=en".format(username))
    driver.implicitly_wait(1)
    scroll_to_bottom()

# create a function that loads a tiktok profile page and returns the number of followers. Use xpath with the data-e2e"followers-count" attribute.
def get_followers(username, load_profile=True):
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    followers = driver.find_element_by_xpath('//strong[@data-e2e="followers-count"]').text
    return convert_to_int(followers)

# create a function that takes a list and returns then as in a json format.
def list_to_json(list):
    return json.dumps(list)

# create a function that loads a tiktok profile page and returns the number of likes. Use xpath to find the strong tag with the data-e2e"likes-count" attribute.
def get_likes(username, load_profile=True):
    if load_profile or load_profile is None:
        load_tiktok_profile(username)
    likes = driver.find_element_by_xpath('//strong[@data-e2e="likes-count"]').text
    return list_to_json(convert_to_int(likes))

def full_scrape(username, comments=False, min_likes=0):
    load_tiktok_profile(username)
    dict= {}
    dict['Followers'] = get_followers(username, False)
    dict['Likes'] = get_likes(username, False)
    dict['Video Views'] = get_video_views(username, False) 
    if comments:
        comment_dict = get_comments(username, False, min_likes)
        dict["Comments"] = comment_dict
    return(list_to_json(dict))
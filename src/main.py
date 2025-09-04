from reddit_scraper import *
from reddit_story import *

for item in pick("relationship_advice"): # pick stories
    scrap(item["url"])
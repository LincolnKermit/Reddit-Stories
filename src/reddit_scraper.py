import time
from yars import YARS

# Initialize YARS scraper
miner = YARS()


def pick(subreddit, limit=10, category="top", time_filter="week"):
    """
    Fetch posts from a subreddit using YARS library.
    
    Args:
        subreddit: Name of the subreddit to fetch from
        limit: Number of posts to fetch
        category: Type of posts to fetch ("hot", "top", "new")
        time_filter: Time filter for posts ("day", "week", "month", "year", "all")
    
    Returns:
        List of posts with title and url fields
    """
    start_time = time.time()
    print(f"Fetching {limit} posts from r/{subreddit}...")
    
    # Fetch subreddit posts using YARS
    subreddit_posts = miner.fetch_subreddit_posts(
        subreddit, 
        limit=limit, 
        category=category, 
        time_filter=time_filter
    )
    
    # Transform posts to include full URL
    processed_posts = []
    for post in subreddit_posts:
        processed_post = {
            "title": post["title"],
            "url": f"https://www.reddit.com{post['permalink']}",
            "author": post["author"],
            "score": post["score"],
            "num_comments": post["num_comments"],
            "created_utc": post["created_utc"]
        }
        processed_posts.append(processed_post)
    print(f"Fetched {len(processed_posts)} posts in {round(time.time() - start_time, 2)} seconds")
    print(processed_posts)
    return processed_posts

# test
if __name__ == "__main__":
    pick("AmItheAsshole", limit=5, category="top", time_filter="week")
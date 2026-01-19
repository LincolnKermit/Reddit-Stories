import time
import re
from yars import YARS

# Initialize YARS scraper
miner = YARS()


def clean_reddit_text(text):
    """
    Clean Reddit post text by removing edits, special formatting, and problematic characters.
    
    Args:
        text: Raw Reddit post text
    
    Returns:
        Cleaned text suitable for TTS
    """
    if not text:
        return ""
    
    # First, split by common edit patterns and take only the first part (original post)
    # Match patterns like "edit:", "Edit:", "EDIT:", "UPDATE:", etc.
    edit_pattern = r'(?:\n\s*(?:edit|update|tldr|tl;dr)[\s:*]+.*)|(?:\n\s*[-—_=*]{2,}\s*\n)|(?:\n\s*\d+(?:st|nd|rd|th)?\s*edit[\s:]+.*)'
    
    # Split on edit patterns and take first part (original story)
    parts = re.split(edit_pattern, text, flags=re.IGNORECASE)
    text = parts[0] if parts else text
    
    # Remove lines with just separators
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip lines that are just separators
        if re.match(r'^[-_—=*]{2,}$', stripped):
            continue
        
        # Skip very short lines that are likely formatting
        if len(stripped) > 0:
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Replace smart quotes and special characters
    replacements = {
        ''': "'", ''': "'",
        '"': '"', '"': '"',
        '—': '-', '–': '-',
        '…': '...',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def scrap(url):
    """
    Scrape the text content from a Reddit post URL using YARS library.
    
    Args:
        url: Full Reddit post URL (e.g., "https://www.reddit.com/r/subreddit/comments/...")
    
    Returns:
        String containing the post body text, or None if scraping fails
    """
    start_time = time.time()
    
    # Extract permalink from URL (everything after reddit.com)
    if 'reddit.com' in url:
        permalink = url.split('reddit.com')[1]
    else:
        # If already a permalink, use as is
        permalink = url if url.startswith('/') else f'/{url}'
    
    # Use YARS to scrape post details
    post_details = miner.scrape_post_details(permalink)
    
    if post_details and 'body' in post_details:
        body_text = post_details['body']
        # Clean the text to remove edits and special characters
        cleaned_text = clean_reddit_text(body_text)
        print(f"Scraped text in {round(time.time() - start_time, 2)} seconds")
        return cleaned_text
    else:
        print("Post content not found")
        return None
        return None

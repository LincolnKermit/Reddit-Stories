import requests, time
from bs4 import BeautifulSoup



def pick(theme):
    start_time = time.time()
    url = f"https://www.reddit.com/r/{theme}/"
    headers = {"User-Agent": "Mozilla/5.0"}  # important, otherwise Reddit may block

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    links = soup.find_all("a", {"slot": "full-post-link"})

    for link in links:
        href = link.get("href")
        title = link.get_text(strip=True)
        print("URL:", "https://www.reddit.com" + href)
        print("Title:", title)
        print("-" * 50 + "\n")
    print(f"Picked {len(links)} stories from r/{theme} in {round(time.time() - start_time, 2)} seconds")
    # return the title also
    return [{"url": "https://www.reddit.com" + link.get("href"), "title": link.get_text(strip=True)} for link in links if link.get("href")]


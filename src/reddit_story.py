import requests
from bs4 import BeautifulSoup


def scrap(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # éviter le blocage

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Trouver le bloc principal du texte
    post_div = soup.find("div", {"property": "schema:articleBody"})

    if post_div:
        paragraphs = [p.get_text(strip=True) for p in post_div.find_all("p")]
        full_text = "\n\n".join(paragraphs)
        print(full_text)
        return full_text
    else:
        print("Post content not found")

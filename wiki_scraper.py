import random

import requests
from bs4 import BeautifulSoup


def crawl_wiki_article(url):
    response = requests.get(url=url)

    # Parse all the paragraphs (<p>) in the wiki page
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.findAll('p')
    print(paragraphs)

    # Parse all the links (<a>) in the wiki page
    links = soup.find(id="bodyContent").find_all("a")
    random.shuffle(links)

    # Go through all links of the wiki page
    for link in links:
        # Only treat links that are wiki articles
        if link['href'].find("/wiki/") == -1:
            continue

        # Use links to load further wiki pages
        print(link)


crawl_wiki_article("https://de.wikipedia.org/wiki/Quantenphysik")

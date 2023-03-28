import os
import random
import time

import requests
from bs4 import BeautifulSoup


def wait_random_time():
    # Waits 5 to 15 seconds for protect websites
    wait = random.randint(5, 15)
    time.sleep(wait)


def save_html_response_to_file(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the title in the wiki page (note the title class!)
    title_spans = soup.find_all('span', {'class': 'mw-page-title-main'})
    if len(title_spans) == 1:
        title = title_spans[0].text
    else:
        return

    # Save the file with title as filename
    filepath = "html/" + title + ".html"
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)
        print("HTML code saved to {0}.".format(title))


def filter_links(link_tags):
    links = []
    for link_tag in link_tags:
        # Get the link href
        link_url = link_tag['href']

        # Skip links that are no wiki articles
        if link_url.find("/wiki/") == -1:
            continue

        # Remove unwanted links, e.g. categories
        if "Kategorie:" in link_url:
            continue
        if "Kategorien:" in link_url:
            continue
        if "Category:" in link_url:
            continue
        if "Datei:" in link_url:
            continue
        if "Benutzer:" in link_url:
            continue

        # Remove duplicate links by only adding unique
        if link_url not in links:
            links.append(link_url)

    return links


def deep_crawl_wiki_article(url):
    # Ensure that a directory "html" is present
    directory = "html"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory 'html' was created as it was not present.")

    # Request wiki page
    print("Crawling website: {0}.".format(url))
    response = requests.get(url=url)

    # Save the originating wiki page in html-file
    save_html_response_to_file(response)

    # Parse all the links (<a>) in the wiki page and remove not wanted links
    soup = BeautifulSoup(response.content, 'html.parser')
    link_tags = soup.find(id="bodyContent").find_all("a")
    links = filter_links(link_tags)
    print("Found relevant links for website: {0}. Crawling links now.".format(len(links)))

    # Go through all links of the wiki page
    for link in links:
        # Build url for linked wiki page
        url = "https://de.wikipedia.org" + link

        # Request and save the linked wiki page (link)
        print("Crawling link website: {0}.".format(url))
        response = requests.get(url=url)
        save_html_response_to_file(response)

        # Wait to protect website
        wait_random_time()

    print("Finished crawling website: {0}.".format(url))

# !!! FOR EDUCATIONAL PURPOSES ONLY! DO NOT USE THE TOOL WITHOUT PERMISSION OR LIMITS !!!
deep_crawl_wiki_article("https://de.wikipedia.org/wiki/Quantenphysik")

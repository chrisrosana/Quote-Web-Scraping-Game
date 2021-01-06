import requests  # use for HTTP requests
from bs4 import BeautifulSoup  # use for web scraping
from time import sleep  # use to add delays to code to space my requests and not overload the server
from pprint import pprint

base_url = "http://quotes.toscrape.com"
url = "/page/1"

all_quotes = []

while url:
    # GET request
    res = requests.get(f"{base_url}{url}")  # append url to base_url
    pprint(f"{base_url}{url}")
    # Scraping time
    soup = BeautifulSoup(res.text, "html.parser")  # res.text turns it to HTML

    quotes = soup.find_all(class_="quote")
    # pprint(quotes)
    for quote in quotes:
        text = quote.find(class_="text").get_text()
        author = quote.find(class_="author").get_text()
        bio_link = quote.find("a")["href"]
        # append the text, author, link to all_quotes list
        all_quotes.append({
            "text": text,
            "author": author,
            "bio-link": bio_link
        })
    # find the next button
    next_button = soup.find(class_="next")
    # grab the url
    url = next_button.find("a")["href"] if next_button else None
    sleep(2)

pprint(all_quotes)
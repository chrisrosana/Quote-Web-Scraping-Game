from csv import DictWriter
import requests
from bs4 import BeautifulSoup  # use for web scraping

base_url = "http://quotes.toscrape.com"


# scrape quotes
def scrape_quotes():
    url = "/page/1"

    all_quotes = []

    while url:
        # GET request
        res = requests.get(f"{base_url}{url}")  # append url to base_url
        # pprint(f"{base_url}{url}") # this prints the link url
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
        # sleep(1)
    return all_quotes


# write csv file
def write_quotes(quotes):
    with open("quotes.csv", "w") as csv_file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)
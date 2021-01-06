import requests  # use for HTTP requests
from bs4 import BeautifulSoup  # use for web scraping
from time import sleep  # use to add delays to code to space my requests and not overload the server
from pprint import pprint
from random import choice

base_url = "http://quotes.toscrape.com"
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
    # sleep(2)

quote = choice(all_quotes)
print("Here's a quote: ")
print(quote['text'])
print(quote['author'])  # THIS is cheating lol

remaining_guesses = 4
guess = ''

while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
    guess = input(f"Who said this quote? Guess remaining: {remaining_guesses} \n")

    if guess.lower() == quote['author'].lower():
        print("CORRECT")
        break

    remaining_guesses -= 1

    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Here\'s a hint: the author is born in {birth_date} in {birth_place}")
    elif remaining_guesses == 2:
        print(f"Here\'s a hint: author\'s first name starts with: {quote['author'][0]}")
    elif remaining_guesses == 1:
        last_initial = quote['author'].split(' ')[1][0]
        print(f"Here\'s the last hint: author\'s last name starts with: {last_initial}")
    else:
        print(f"Sorry you ran out of guesses. Author is {quote['author']}")
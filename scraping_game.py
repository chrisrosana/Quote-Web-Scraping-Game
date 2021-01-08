import requests  # use for HTTP requests
from bs4 import BeautifulSoup  # use for web scraping
from time import sleep  # use to add delays to code to space my requests and not overload the server
from pprint import pprint
from random import choice
from csv import DictReader  # use for csv

base_url = "http://quotes.toscrape.com"


# read quotes in csv instead
def read_quotes(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        return list(csv_reader)


def start_game(quotes):
    quote = choice(quotes)
    print("Here's a quote: ")
    print(quote['text'])
    # print(quote['author'])  # THIS is cheating lol
    remaining_guesses = 4
    guess = ''
    playing = True

    while playing and guess.lower() != quote['author'].lower() and remaining_guesses > 0:
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

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input('Would you like to play again (y/n)?')

        if again.lower() in ('yes', 'y'):
            return start_game(quotes)
        else:
            print('OK GOODBYE!')


quotes = read_quotes('quotes.csv')
start_game(quotes)

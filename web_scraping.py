"""  code scaps a website https://www.gutenberg.org/ for 10 books and also extract 10 most frequent words in each book"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin

# Function to extract and process text from a book URL
def process_book(book_url):
    response = requests.get(book_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        book_text = soup.get_text()  # Get all the text from the book
        return book_text
    else:
        return None

# Send a GET request to the Project Gutenberg homepage
url = "https://www.gutenberg.org/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find book elements
    book_elements = soup.find_all('a', {'title': True, 'authors': True})

    # Limit the number of books to process
    num_books_to_process = 10
    books_data = []

    for book_element in book_elements[:num_books_to_process]:
        book_title = book_element['title']
        book_author = book_element['authors']
        book_link = urljoin(url, book_element['href'])

        # Process the book and get its text
        book_text = process_book(book_link)
        
        if book_text:
            # Split the text into words and count their frequencies
            words = book_text.split()
            word_counter = Counter(words)
            
            # Calculate the total number of words in the book
            total_words = len(words)
            
            books_data.append({
                'Title': book_title,
                'Author': book_author,
                'Link': book_link,
                'Word Frequencies': word_counter,
                'Total Words': total_words
            })

    # Sort the books by word frequency (descending order)
    books_data.sort(key=lambda x: sum(x['Word Frequencies'].values()), reverse=True)

    # Display the books ranked by word frequency
    for i, book_data in enumerate(books_data):
        print(f"Book {i + 1}:")
        print(f"Title: {book_data['Title']}")
        print(f"Author: {book_data['Author']}")
        print(f"Link: {book_data['Link']}")
        print(f"Total Words: {book_data['Total Words']}")
        print("Top 10 Most Frequent Words:")
        for word, frequency in book_data['Word Frequencies'].most_common(10):
            print(f"{word}: {frequency} times")
        print()

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

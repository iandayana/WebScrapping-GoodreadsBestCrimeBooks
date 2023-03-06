from html_docs import HTMLDocs
from bs4 import BeautifulSoup
import re
import pandas as pd


TITLE = "goodreads_crime_mystery_books"  # title for documents
URL = "https://www.goodreads.com/list/show/11.Best_Crime_Mystery_Books"
QUERYABLE_OBJECT = "?page="  # query string
MAX_PAGE = 69  # maximum number of pages

# PART 1
########
html_doc = HTMLDocs(URL, TITLE, QUERYABLE_OBJECT)

for i in range(1, MAX_PAGE+1):        # iterate from first page to the last page
    html_doc.save_doc(i)


# PART 2
# #######
books_dict = []
for i in range(1, MAX_PAGE+1):
    # Open the html document
    with open(f"{TITLE}_{i}.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # Locate the data we want to extract from the document
    rank = soup.find_all("td", {"class": "number"})
    title_tags = soup.find_all("a", {"class": "bookTitle"})
    author_names = soup.find_all("a", {"class": "authorName"})
    ratings = soup.find_all("span", {"class": "minirating"})
    n_ratings = soup.find_all("span", {"class": "minirating"})
    scores = soup.find_all(string=re.compile("score:"))
    n_voters = soup.find_all(id=re.compile("loading_link_"))

    # Extract the data
    for j in range(len(title_tags)):
        book_item = {
            "rank": int(rank[j].text.strip()),
            "title": title_tags[j].text.strip(),
            "author": author_names[j].text.strip(),
            "avg_rating": float(ratings[j].text.strip().split()[-6]),
            "n_rating": int(ratings[j].text.strip().split()[-2].replace(',', '')),
            "score": int(scores[j].text.strip().split()[-1].replace(',', '')),
            "n_voter": int(n_voters[j].text.strip().split()[0].replace(',', ''))
        }
        books_dict.append(book_item)


# PART 2
# #######
# Save dictionary as csv
books_df = pd.DataFrame(books_dict)
books_df.to_csv(f"{TITLE}.csv", index=False)
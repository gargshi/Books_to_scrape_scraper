import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

def create_cache(path):
    """Create a cache file with given path if it doesn't exist."""
    os.makedirs('cache', exist_ok=True)
    cache_file = os.path.join('cache', path)
    if not os.path.exists(cache_file):
        open(cache_file, 'w').close()
    return cache_file

def robots_allowed(url):
    """Check if crawling is allowed by robots.txt."""
    res = requests.get(url)
    if res.status_code != 200:
        return False
    meta = BeautifulSoup(res.text, 'html.parser').find(
        'meta', attrs={'name': 'robots'})
    content = meta.get('content') if meta else ''
    return not any(tag in content for tag in ['noindex', 'nofollow'])


def scrape_books(url, elem_class):
    """Scrape books from a given page."""
    res = requests.get(url)
    if res.status_code != 200:
        print(f'Failed to load: {url} ({res.status_code})')
        return []
    soup = BeautifulSoup(res.text, 'html.parser')
    books = soup.find_all('article', class_=elem_class)
    return [{
            'title': b.h3.a['title'],
            'link': b.h3.a['href'],
            'price': b.find('p', class_='price_color').text
            } for b in books]


def pageloop(base_url, elem_class, start, end):
    """Scrape books from a range of pages from a given base URL."""
    all_books = []
    for i in range(start, end + 1):
        print(f'Scraping Page {i}')
        url = f'{base_url}catalogue/page-{i}.html'
        all_books.extend(scrape_books(url, elem_class))
    print(f'Done scraping {end - start + 1} page(s)')
    return all_books


def main(url, elem_class, start, end, cache_name, clear_cache):
    """
    Main function to scrape books from a given URL.

    Parameters:
            url (str): URL of the page to scrape from.
            elem_class (str): Class name of the element containing books.
            start (int): Starting page number (inclusive) to scrape.
            end (int): Ending page number (inclusive) to scrape.
            cache_name (str): Name of the cache file.
            clear_cache (bool): Whether to clear cache before scraping.

    Returns:
            None
    """
    # Check if cache file needs to be cleared
    if clear_cache:
        print('Clearing cache...')
        os.remove(create_cache(cache_name))
        print('Cache cleared.')

    # Create cache file
    cache_file = create_cache(cache_name)

    # Check if cache file is empty
    if os.stat(cache_file).st_size == 0:
        print('Cache is empty. Starting scrape...')
        # Check if robots.txt allows crawling
        if robots_allowed(url):
            # Scrape books
            books = pageloop(url, elem_class, start, end)
            pd.DataFrame(books).to_csv(cache_file, index=False)
            print(f'Data cached to {cache_file}')
        else:
            print('Crawling not allowed by robots.txt.')


if __name__ == '__main__':
    main(
        url='https://books.toscrape.com/',
        elem_class='product_pod',
        start=1,
        end=6,
        cache_name='books.csv',
        clear_cache=True
    )
## 📚 Book Scraper (Books to Scrape)

A lightweight web scraper built in Python to extract book data from the website [Books to Scrape](https://books.toscrape.com).  
It features basic caching, robot exclusion checks, and paginated scraping.

---

### 🚀 Features

- ✅ Scrapes book **title**, **price**, and **URL**
- ✅ Supports scraping across multiple pages
- ✅ Caches results to CSV to avoid redundant scrapes
- ✅ Respects site policies via robot meta checks
- ✅ Structured, beginner-friendly code

---

### 📦 Dependencies

- `requests` – for HTTP requests  
- `BeautifulSoup` (bs4) – for parsing HTML  
- `pandas` – for structured data handling

Install them using:

```bash
pip install requests beautifulsoup4 pandas

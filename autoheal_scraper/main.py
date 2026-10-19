from fetcher import fetch_html
from parser import extract_price_basic
from config import ORIGINAL_URL, UPDATED_URL

def main():
    print(f"Fetching from {ORIGINAL_URL}")
    html = fetch_html(ORIGINAL_URL)
    price = extract_price_basic(html)
    
    print("Extracted:", price)

    print(f"Fetching from {UPDATED_URL}")
    html = fetch_html(UPDATED_URL)
    price = extract_price_basic(html)

    print("Extracted:", price)


if __name__ == '__main__':
    main()

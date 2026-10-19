from bs4 import BeautifulSoup
from utils import init_selectors, load_selectors, save_html_snapshot
from healer import heal_selector

def extract_price_basic(html: str):
    """Dynamic selector-based extraction"""

    soup = BeautifulSoup(html, "html.parser")

    init_selectors()
    selectors = load_selectors()

    # Try all selectors
    for sel in selectors:
        if sel["type"] == "css":
            el = soup.select_one(sel["value"])

            if el:
                print(f"Using selector: {sel['value']}")
                save_html_snapshot(html)
                return el.text.strip()

    # All selectors failed → trigger healing
    print("All selectors failed. Triggering LLM healing...")
    
    return heal_selector(html, selectors)
from bs4 import BeautifulSoup
from utils import add_selector, get_last_html, save_html_snapshot
from llm_client import call_llm

def parse_response(text):
    selector = None
    price = None

    for line in text.splitlines():
        if "selector:" in line:
            selector = line.split("selector:")[1].strip()
        if "price:" in line:
            price = line.split("price:")[1].strip()

    return selector, price

def heal_selector(new_html: str, selectors: list):
    old_html = get_last_html()

    prompt = f"""
    You are fixing a broken web scraper.

    The website updated its HTML and the old CSS selectors no longer work.
    Your job: find the NEW CSS selector that selects the price element in the NEW HTML.

    OLD SELECTORS (now broken):
    {selectors}

    HINT — the old selectors stopped matching because the HTML class/structure changed.
    Use the old selectors as a clue for what element to look for (a price display element).
    
    OLD HTML (for reference, but may be outdated):
    {old_html[:2000]}
    
    NEW HTML (the updated page — find the selector HERE):
    {new_html[:2000]}

    RULES:
    - Look ONLY in the NEW HTML above
    - The selector must actually exist in the NEW HTML
    - Do NOT guess or invent selectors
    - Return ONLY this line, nothing else:

    selector: <css_selector>
    """

    response = call_llm(prompt)
    
    selector, price = parse_response(response)

    # 🔥 VALIDATION STEP (CRITICAL)
    soup = BeautifulSoup(new_html, "html.parser")

    if selector:
        el = soup.select_one(selector)

        if el:
            real_price = el.text.strip()

            print(f"🧠 LLM suggested: {selector}")
            print(f"🔍 Verified price: {real_price}")

            # store selector only if valid
            add_selector({"type": "css", "value": selector})

            # save this working HTML for future reference
            save_html_snapshot(new_html)

            return real_price

        else:
            print("LLM selector invalid")

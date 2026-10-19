from pathlib import Path

import pytest

import healer
import parser
import utils


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OLD_SELECTOR = {"type": "css", "value": "div.offer-price"}
ORIGINAL_HTML = (PROJECT_ROOT / "templates" / "original.html").read_text()
UPDATED_TEMPLATE = (PROJECT_ROOT / "templates" / "updated.html").read_text()


@pytest.fixture
def isolated_scraper_db(tmp_path, monkeypatch):
    """Give each test independent selector and HTML snapshot state."""
    monkeypatch.setattr(utils, "DB_PATH", tmp_path / "scraper-test.db")
    utils.init_db()
    utils.save_selectors([OLD_SELECTOR])


@pytest.mark.parametrize(
    ("new_html", "new_selector"),
    [
        (UPDATED_TEMPLATE, "div.price-of-this-product"),
        ('<main><div class="sale-price">500 $</div></main>', "div.sale-price"),
        ('<section><span class="current-price">500 $</span></section>', "span.current-price"),
    ],
    ids=["provided-updated-template", "renamed-to-sale-price", "renamed-to-current-price"],
)
def test_simple_class_name_changes_are_healed(
    isolated_scraper_db, monkeypatch, new_html, new_selector
):
    utils.save_html_snapshot(ORIGINAL_HTML)
    monkeypatch.setattr(healer, "call_llm", lambda _prompt: f"selector: {new_selector}")

    result = parser.extract_price_basic(new_html)

    assert result == "500 $"
    assert utils.load_selectors()[0] == {"type": "css", "value": new_selector}
    assert utils.get_last_html() == new_html


def test_medium_nested_price_ignores_label_and_previous_price(
    isolated_scraper_db, monkeypatch
):
    old_html = '<div class="offer-price">$129.99</div>'
    new_html = """
    <article class="product-card">
      <h2>Studio Headphones</h2>
      <div class="purchase-panel">
        <span class="label">Current price</span>
        <span class="previous-price">Was $129.99</span>
        <div data-role="current-price"><span>$89.99</span><small> USD</small></div>
      </div>
    </article>
    """
    new_selector = ".product-card .purchase-panel [data-role='current-price']"
    utils.save_html_snapshot(old_html)
    monkeypatch.setattr(healer, "call_llm", lambda _prompt: f"selector: {new_selector}")

    result = parser.extract_price_basic(new_html)

    assert result == "$89.99 USD"
    assert utils.load_selectors()[0] == {"type": "css", "value": new_selector}
    assert utils.get_last_html() == new_html


def test_hard_multiple_products_selects_target_current_price(
    isolated_scraper_db, monkeypatch
):
    old_html = '<div class="offer-price">$199.99</div>'
    new_html = """
    <main>
      <article data-sku="headphones-basic">
        <span itemprop="price">$79.99</span>
        <span class="was-price">$99.99</span>
      </article>
      <article data-sku="headphones-pro">
        <span class="was-price">$249.99</span>
        <div class="pricing">
          <span itemprop="price">$179.99</span>
          <span class="currency">USD</span>
        </div>
      </article>
      <aside class="recommendation">
        <span itemprop="price">$59.99</span>
      </aside>
    </main>
    """
    new_selector = "article[data-sku='headphones-pro'] .pricing [itemprop='price']"
    utils.save_html_snapshot(old_html)
    monkeypatch.setattr(healer, "call_llm", lambda _prompt: f"selector: {new_selector}")

    result = parser.extract_price_basic(new_html)

    assert result == "$179.99"
    assert utils.load_selectors()[0] == {"type": "css", "value": new_selector}
    assert utils.get_last_html() == new_html


def test_invalid_llm_selector_does_not_replace_working_state(
    isolated_scraper_db, monkeypatch
):
    old_html = '<div class="offer-price">$500</div>'
    new_html = '<div class="new-price">$450</div>'
    utils.save_html_snapshot(old_html)
    monkeypatch.setattr(healer, "call_llm", lambda _prompt: "selector: .does-not-exist")

    result = parser.extract_price_basic(new_html)

    assert result is None
    assert utils.load_selectors() == [OLD_SELECTOR]
    assert utils.get_last_html() == old_html
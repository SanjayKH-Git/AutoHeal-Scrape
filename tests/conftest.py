import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRAPER_PACKAGE = PROJECT_ROOT / "autoheal_scraper"

# The scraper modules use script-style imports (for example, ``from utils import ...``).
sys.path.insert(0, str(SCRAPER_PACKAGE))
import os
from pathlib import Path

COACH_INDEX_SITEMAP = "https://www.coach.com/sitemap_index.xml"
COACH_PRODUCT_SITEMAP = "https://www.coach.com/sitemap_0-product.xml"
PRODUCT_NAME = "Slim Billfold Wallet In Signature Canvas"
LOCAL = bool(os.getenv("LOCAL", "0"))
BASE_DIR = Path(__file__).resolve().parent

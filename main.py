from fastapi import FastAPI
from typing import Literal
from dotenv import load_dotenv


from services.messenger import EmailMessenger, SMSMessenger
from services.crawlers import CoachProductSitemapCrawler
from consts import PRODUCT_NAME

load_dotenv()

app = FastAPI()

type TransmissionType = Literal["email"] | Literal["sms"]


@app.get("/{method}")
async def root(method: TransmissionType):
    """
    We should only send emails or SMS messages if the item is in stock.
    I will do every 2 hours to avoid rate limiting. We will decrease the time if coach trusts us.
    """
    if method not in ["email", "sms"]:
        return {"error": "Invalid transmission type. Use 'email' or 'sms'."}

    crawler = CoachProductSitemapCrawler()
    urls = crawler.search_urls(PRODUCT_NAME)
    if not urls:
        return {
            "message": f"There are no products with the name {PRODUCT_NAME} at the moment."
        }

    if method == "email":
        return {
            "message": "Email transmission selected",
            "urls": urls,
            "product_name": PRODUCT_NAME,
        }
    elif method == "sms":
        return {
            "message": "SMS transmission selected",
            "urls": urls,
            "product_name": PRODUCT_NAME,
        }

from fastapi import FastAPI
from typing import Literal

from services.messenger import EmailMessenger, SMSMessenger

app = FastAPI()


type TransmissionType = Literal["email"] | Literal["sms"]


@app.get("/{method}")
async def root(method: TransmissionType):
    """
    We should only send emails or SMS messages if the item is in stock.
    """
    if method == "email":
        return {"message": "Email transmission selected"}
    elif method == "sms":
        return {"message": "SMS transmission selected"}
    else:
        return {"error": "Invalid transmission type"}

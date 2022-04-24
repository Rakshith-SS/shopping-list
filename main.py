from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pytz


# Indian Timezone, to generate bill in Indian Timezone rather than UTC
IST = pytz.timezone('Asia/Kolkata')
app = FastAPI()


class Item(BaseModel):
    item: str
    item_category: str
    quantity: int
    price: int


class ItemList(BaseModel):
    itemsList: Optional[List[Item]]


@app.post("/")
def add_items(itemList: ItemList):
    purchased_items = []
    message = "Billed Successfully"
    invalid_categories = []
    for item in itemList.itemsList:
        if (item.item_category.lower() == "medicine" or
                item.item_category.lower() == "food"):
            tax_rate = 0.05
        elif (item.item_category.lower() == "clothes" and
                item.price < 1000):
            tax_rate = 0.05
        elif (item.item_category.lower() == "clothes" and
                item.price > 1000):
            # 12% tax
            tax_rate = 0.12
        elif (item.item_category.lower() == "cds" or
                item.item_category.lower() == "dvds" or
                item.item_category.lower() == "music"):
            # 3% tax
            tax_rate = 0.03
        elif item.item_category.lower() == "imported":
            # 18% tax
            tax_rate = 0.18
        elif item.item_category.lower() == "book":
            tax_rate = 0
        else:
            tax_rate = "category does not exist"

        """
            If a given category is not specified,
            then skip, that particular item
            instead of exiting the entire payload
        """
        if isinstance(tax_rate, str):
            invalid_categories.append(item.item_category)
        else:
            tax_price = item.price * tax_rate * item.quantity
            total_price = item.price * item.quantity + tax_price
            purchased_items.append({
                "item": item.item,
                "quantity": item.quantity,
                "tax_price": tax_price,
                "total_price": total_price
            })

    purchase_time = datetime.now(IST).strftime("%d %B %Y %H:%M:%S")
    # sort the purchased items by their name
    purchased_items = sorted(
        purchased_items, key=lambda item_name: item_name["item"]
    )

    grand_price = 0
    for item in purchased_items:
        grand_price += item["total_price"]

    """
        5% discount on purchases exceeding 2000
    """
    if grand_price > 2000:
        message = "Billed Successfully with a 5% discount"
        grand_price = grand_price + grand_price * 0.05

    if invalid_categories:
        return {
            "message": "Please include a valid category to generate a bill",
        }
    else:
        return {
            "message": message,
            "purchased_items": purchased_items,
            "purchased_time": purchase_time,
            "grand_price": grand_price
        }

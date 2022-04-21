from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

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
    # print(type(itemList.itemsList))
    print(type(itemList.itemsList))
    print(itemList.itemsList)
    purchased_items = []
    for item in itemList.itemsList:
        if item.item_category == "medicine" or item.item_category == "food":
            tax_rate = 0.05
        elif item.item_category == "clothes" and item.item_price < 1000:
            tax_rate = 0.05
        elif item.item_category == "clothes" and item.item_price > 1000:
            # 12% tax
            tax_rate = 0.12
        elif item.item_category == "cds" or item.item_category == "dvds":
            tax_rate = 0.03
        elif item.item_category == "imported":
            tax_rate == 0.18
        else:
            tax_rate = "category does not exist"

        tax_price = item.price * tax_rate * item.quantity
        total_price = item.price * item.quantity + tax_price
        purchased_items.append({
            "item": item.item,
            "quantity": item.quantity,
            "tax_price": tax_price,
            "total_price": total_price
        })
    purchase_time = datetime.now()
    return {
        "purchased_items": purchased_items,
        "purchased_time": purchase_time
    }

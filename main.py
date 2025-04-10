from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False

items = []

@app.get("/items")
async def root():
    return items

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")

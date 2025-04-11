from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import AfterValidator, BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False
    
def check_text(item: Item):
    if len(item.text) < 5:
        raise ValueError(f'Text is to short: {item.text.count()}')
    return item

items = []

@app.get("/items")
async def root():
    return items

@app.post("/items")
def create_item(item: Annotated[Item, AfterValidator(check_text)]):
    items.append(item)
    return items

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")

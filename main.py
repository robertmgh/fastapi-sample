from typing import Annotated, List
from fastapi import Body, Cookie, FastAPI, HTTPException
from pydantic import AfterValidator, BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False
    price: float = Field(gt=0, description="The price must be greater then zero")
    tags: List[str]
    
def check_text(item: Item):
    if len(item.text) < 5:
        raise ValueError(f'Text is to short: {len(item.text)}')
    return item

items = []

@app.get("/items")
async def root():
    return items

@app.post("/items", status_code=201)
def create_item(test: Annotated[str | None, Cookie()], item: Annotated[Item, AfterValidator(check_text), Body(example=[{
    "text": "test doc"
}])]):
    items.append(item)
    return {"test": test, **item.model_dump()}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")

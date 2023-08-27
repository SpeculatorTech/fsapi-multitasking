from fastapi import FastAPI, HTTPException
from typing import List
from uuid import uuid4

from schemas import Item, ItemCreate, ItemGet

import json
import uvicorn

app = FastAPI()

with open("data.json", "r") as f:
    data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items", response_model=List[ItemGet])
async def get_items():
    return data

@app.post("/item/create", response_model=ItemCreate)
async def create_items(item: Item):
    new_id = str(uuid4())
    new_item = {"id": new_id, **item.model_dump()}
    data.append(new_item)
    # Update data.json with new data
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    return new_item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id < 1 or item_id > len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    return data[item_id - 1]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 1 or item_id > len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    data[item_id - 1] = {"id": item_id, **item.__dict__()}
    # Update data.json with new data
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    return data[item_id - 1]

@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 1 or item_id > len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = data.pop(item_id - 1)
    # Update data.json with new data
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    return deleted_item

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

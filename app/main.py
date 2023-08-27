from fastapi import FastAPI, HTTPException
from typing import List
from uuid import uuid4, UUID

from schemas import Item, CreateItem, GetItem

import json
import uvicorn

app = FastAPI()

with open("app/database/data.json", "r") as f:
    data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items", response_model=List[GetItem])
async def get_items():
    return data

@app.post("/item/create", response_model=CreateItem)
async def create_items(item: Item):
    new_id = str(uuid4())
    new_item = {"id": new_id, **item.model_dump()}
    data.append(new_item)
    # Update data.json with new data
    with open("app/database/data.json", "w") as f:
        json.dump(data, f, indent=4)
    return new_item

@app.get("/item/get/{item_id}", response_model=GetItem)
async def get_item(item_id: UUID):
    for item in data:
        if item["id"] == str(item_id):
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/item/put/{item_id}", response_model=Item)
async def update_item(item_id: UUID, item: Item):
    for i, existing_item in enumerate(data):
        if existing_item["id"] == str(item_id):
            updated_item = {"id": str(item_id), **item.model_dump()}
            data[i] = updated_item
            with open("app/database/data.json", "w") as f:
                json.dump(data, f, indent=4)
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/delete/{item_id}", response_model=Item)
async def delete_item(item_id: UUID):
    for i, existing_item in enumerate(data):
        if existing_item["id"] == str(item_id):
            deleted_item = data.pop(i)
            with open("app/database/data.json", "w") as f:
                json.dump(data, f, indent=4)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

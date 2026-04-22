from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

app = FastAPI(title="Category and Product Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "bestdeal")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


def to_doc(doc):
    doc["id"] = str(doc.pop("_id"))
    return doc


class Category(BaseModel):
    name: str
    description: str = ""


class Product(BaseModel):
    name: str
    description: str = ""
    price: float
    category_id: str
    image: str = ""
    stock: int = 0


@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Categories ────────────────────────────────────────────────────────────────

@app.get("/categories")
async def get_categories():
    return [to_doc(c) for c in await db.categories.find().to_list(200)]


@app.post("/categories", status_code=201)
async def create_category(cat: Category):
    result = await db.categories.insert_one(cat.model_dump())
    return {"id": str(result.inserted_id)}


@app.delete("/categories/{id}")
async def delete_category(id: str):
    await db.categories.delete_one({"_id": ObjectId(id)})
    return {"deleted": id}


# ── Products ──────────────────────────────────────────────────────────────────

@app.get("/products")
async def get_products(category_id: str = None):
    query = {"category_id": category_id} if category_id else {}
    return [to_doc(p) for p in await db.products.find(query).to_list(500)]


@app.get("/products/{id}")
async def get_product(id: str):
    p = await db.products.find_one({"_id": ObjectId(id)})
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return to_doc(p)


@app.post("/products", status_code=201)
async def create_product(product: Product):
    result = await db.products.insert_one(product.model_dump())
    return {"id": str(result.inserted_id)}


@app.put("/products/{id}")
async def update_product(id: str, product: Product):
    await db.products.update_one({"_id": ObjectId(id)}, {"$set": product.model_dump()})
    return {"updated": id}


@app.delete("/products/{id}")
async def delete_product(id: str):
    await db.products.delete_one({"_id": ObjectId(id)})
    return {"deleted": id}

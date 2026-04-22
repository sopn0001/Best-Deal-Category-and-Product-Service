"""
Insert sample categories and products into MongoDB (uses pymongo only).

  python seed_data.py              # skip if categories already exist
  python seed_data.py --reset      # clear categories + products, then seed

Install once (same folder as requirements.txt):

  python -m pip install -r requirements.txt
  # or minimal seed only:
  python -m pip install pymongo

Env vars (same as the API):
  MONGO_URL  default mongodb://localhost:27017
  DB_NAME    default bestdeal

Product images use Unsplash (free to use under their license for demos).
"""

import argparse
import os

from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "bestdeal")

# Unsplash photo URLs chosen to match each product (w=800 for consistent sizing).
CATALOG = [
    {
        "name": "Electronics",
        "description": "Computers, audio, phones, and accessories",
        "products": [
            {
                "name": "Laptop 15\"",
                "description": "Everyday laptop for work and school",
                "price": 799.99,
                "stock": 12,
                "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80",
            },
            {
                "name": "Wireless Mouse",
                "description": "Ergonomic 2.4 GHz mouse",
                "price": 29.99,
                "stock": 40,
                "image": "https://images.unsplash.com/photo-1527814050087-379381547938?w=800&q=80",
            },
            {
                "name": "USB-C Hub",
                "description": "7-in-1 hub with HDMI and card reader",
                "price": 49.5,
                "stock": 25,
                "image": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=800&q=80",
            },
            {
                "name": "Wireless Headphones",
                "description": "Over-ear Bluetooth noise cancelling",
                "price": 199.0,
                "stock": 18,
                "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",
            },
            {
                "name": "Smartphone",
                "description": '6.1" OLED display, 128 GB',
                "price": 699.0,
                "stock": 22,
                "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80",
            },
        ],
    },
    {
        "name": "Home & Kitchen",
        "description": "Cookware, small appliances, and dining",
        "products": [
            {
                "name": "Stainless Cookware Set",
                "description": "10-piece pots and pans",
                "price": 129.0,
                "stock": 8,
                "image": "https://images.unsplash.com/photo-1584990349674-2e8cef0ec7d8?w=800&q=80",
            },
            {
                "name": "Coffee Maker",
                "description": "12-cup programmable drip brewer",
                "price": 89.99,
                "stock": 15,
                "image": "https://images.unsplash.com/photo-1517668808823-a9f702aaa580?w=800&q=80",
            },
            {
                "name": "Chef Knife Set",
                "description": "5-piece German steel",
                "price": 74.5,
                "stock": 20,
                "image": "https://images.unsplash.com/photo-1593618992138-23b7cb3f7e7c?w=800&q=80",
            },
            {
                "name": "Dinnerware Set",
                "description": "16-piece service for four",
                "price": 59.99,
                "stock": 14,
                "image": "https://images.unsplash.com/photo-1603199506016-b7a6975f7ff0?w=800&q=80",
            },
        ],
    },
    {
        "name": "Appliances",
        "description": "Large and countertop home appliances",
        "products": [
            {
                "name": "Microwave Oven",
                "description": '1.1 cu ft stainless',
                "price": 149.99,
                "stock": 6,
                "image": "https://images.unsplash.com/photo-1574269909862-fb54db887157?w=800&q=80",
            },
            {
                "name": "Blender",
                "description": "High-speed 1200W pitcher",
                "price": 79.0,
                "stock": 10,
                "image": "https://images.unsplash.com/photo-1570222094114-d054a877e053?w=800&q=80",
            },
            {
                "name": "Air Fryer",
                "description": "5.8 quart digital touchscreen",
                "price": 99.99,
                "stock": 14,
                "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800&q=80",
            },
            {
                "name": "Toaster Oven",
                "description": "Convection with air fry mode",
                "price": 129.0,
                "stock": 9,
                "image": "https://images.unsplash.com/photo-1585526171168-0de45d360057?w=800&q=80",
            },
        ],
    },
    {
        "name": "TV & Home Theater",
        "description": "Screens, soundbars, and streaming",
        "products": [
            {
                "name": "4K Smart TV 55\"",
                "description": "HDR10, built-in streaming apps",
                "price": 549.0,
                "stock": 5,
                "image": "https://images.unsplash.com/photo-1593359677879-a431ccf0d7b4?w=800&q=80",
            },
            {
                "name": "Soundbar",
                "description": "2.1 channel with wireless subwoofer",
                "price": 249.99,
                "stock": 11,
                "image": "https://images.unsplash.com/photo-1545459722-14000251b802?w=800&q=80",
            },
            {
                "name": "Streaming Stick 4K",
                "description": "Dolby Vision and voice remote",
                "price": 49.99,
                "stock": 45,
                "image": "https://images.unsplash.com/photo-1611162616305-69f92e4b65b0?w=800&q=80",
            },
        ],
    },
    {
        "name": "Office Supplies",
        "description": "Paper, pens, and desk essentials",
        "products": [
            {
                "name": "Desk Organizer",
                "description": "Mesh 6-compartment",
                "price": 24.99,
                "stock": 30,
                "image": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800&q=80",
            },
            {
                "name": "Notebook Pack",
                "description": "3 ruled notebooks, 100 pages each",
                "price": 12.5,
                "stock": 60,
                "image": "https://images.unsplash.com/photo-1517842645767-c639b8806036?w=800&q=80",
            },
            {
                "name": "Ballpoint Pens",
                "description": "Pack of 12, blue ink",
                "price": 6.99,
                "stock": 100,
                "image": "https://images.unsplash.com/photo-1585338448480-d62d0e6cb30c?w=800&q=80",
            },
        ],
    },
]


def main(reset: bool) -> None:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=8000)
    db = client[DB_NAME]

    cat_count = db.categories.count_documents({})
    prod_count = db.products.count_documents({})

    if not reset:
        # Old logic skipped whenever any category existed — if products were empty, nothing was ever inserted.
        if cat_count > 0 and prod_count > 0:
            print("Sample data already present (categories and products). Skipping.")
            client.close()
            return
        if cat_count > 0 and prod_count == 0:
            print("Repairing: categories exist but no products — clearing categories and seeding.")
            db.categories.delete_many({})
        elif prod_count > 0 and cat_count == 0:
            print("Repairing: orphan products — clearing products and seeding.")
            db.products.delete_many({})

    if reset:
        db.products.delete_many({})
        db.categories.delete_many({})

    for cat in CATALOG:
        cat_doc = {"name": cat["name"], "description": cat["description"]}
        cat_res = db.categories.insert_one(cat_doc)
        cid = str(cat_res.inserted_id)
        print(f"Category: {cat['name']} -> {cid}")

        for p in cat["products"]:
            doc = {
                "name": p["name"],
                "description": p["description"],
                "price": p["price"],
                "category_id": cid,
                "image": p["image"],
                "stock": p["stock"],
            }
            res = db.products.insert_one(doc)
            print(f"  Product: {p['name']} (${p['price']}) -> {res.inserted_id}\n           {p['image']}")

    print("\nDone. Open http://localhost:5001/docs or your Store Front to browse.")
    client.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Seed sample categories and products.")
    p.add_argument("--reset", action="store_true", help="Delete existing categories and products first")
    args = p.parse_args()
    main(args.reset)

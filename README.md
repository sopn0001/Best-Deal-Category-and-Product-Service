# Best Deal Store — Category & Product Service

**FastAPI** REST API for **categories** and **products** backed by **MongoDB** (Motor). Optional **seed** script and Docker entrypoint can load demo data on startup. Default API port **5001**.

## What this service does

This service owns the **product catalog**: hierarchical or flat **categories** and **products** (name, description, price, stock, image URL, `category_id`). Both the **Store Front** and **Store Admin** read and write catalog data through this API. It is stateless aside from MongoDB; there is no message queue. In demos, **seed data** fills Mongo with sample categories and products so UIs are not empty on first boot.

## HTTP API (base URL `http://<host>:5001`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Status plus Mongo counts: `categories`, `products`. |
| GET | `/docs` | Swagger UI (OpenAPI). |
| GET | `/redoc` | ReDoc. |
| GET | `/categories` | List categories (max 200). |
| POST | `/categories` | Create category JSON `{ "name", "description?" }` → **201** `{ "id" }`. |
| DELETE | `/categories/{id}` | Delete by Mongo ObjectId string. |
| GET | `/products` | List products (max 500); optional query `category_id=<id>`. |
| GET | `/products/{id}` | Single product; **404** if missing. |
| POST | `/products` | Create product (full `Product` model) → **201** `{ "id" }`. |
| PUT | `/products/{id}` | Replace fields with full product body. |
| DELETE | `/products/{id}` | Delete product. |

## Stack

- Python 3.11, FastAPI, Motor  
- OpenAPI docs: `/docs`, `/redoc`

## Run locally

```bash
pip install -r requirements.txt
export MONGO_URL=mongodb://localhost:27017
export DB_NAME=bestdeal
uvicorn main:app --host 0.0.0.0 --port 5001
```

Seed / reset sample data: `python seed_data.py` or `python seed_data.py --reset`

## Docker

```bash
docker build -t best-deal-category-and-product-service .
```


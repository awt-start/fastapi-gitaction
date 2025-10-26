from typing import Optional
from fastapi import FastAPI

app = FastAPI(title="FastAPI UV Demo", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Health check endpoint returning 200 OK."""
    return {"status": "ok"}


@app.get("/hello")
def hello(name: Optional[str] = None) -> dict:
    """Simple greeting endpoint.

    - If `name` is provided, greet by name.
    - Otherwise, default to "World".
    """
    target = name.strip() if name else "World"
    return {"message": f"Hello, {target}!"}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> dict:
    """Return information about a specific item by ID."""
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": "Demo item from FastAPI UV app",
    }
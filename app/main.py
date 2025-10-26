from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Path
import random
import uuid

app = FastAPI(title="FastAPI UV Demo", version="0.1.0")

# Pydantic models
class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    created_at: datetime
    is_available: bool

class Order(BaseModel):
    id: int
    user_id: int
    items: List[Item]
    total_amount: float
    status: str
    created_at: datetime
    shipping_address: str

class ProductReview(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int = Field(ge=1, le=5)
    comment: str
    created_at: datetime

class WeatherData(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str
    timestamp: datetime

# Mock data
users_db = [
    User(
        id=1,
        username="john_doe",
        email="john@example.com",
        full_name="John Doe",
        is_active=True,
        created_at=datetime(2023, 1, 15, 10, 30, 45),
        last_login=datetime(2023, 10, 20, 14, 22, 33)
    ),
    User(
        id=2,
        username="jane_smith",
        email="jane@example.com",
        full_name="Jane Smith",
        is_active=True,
        created_at=datetime(2023, 2, 20, 9, 15, 20),
        last_login=datetime(2023, 10, 22, 11, 45, 10)
    ),
    User(
        id=3,
        username="bob_wilson",
        email="bob@example.com",
        full_name="Bob Wilson",
        is_active=False,
        created_at=datetime(2023, 3, 10, 16, 45, 30)
    )
]

items_db = [
    Item(
        id=1,
        name="Laptop",
        description="High-performance laptop for work and gaming",
        price=1299.99,
        category="Electronics",
        created_at=datetime(2023, 1, 5, 12, 0, 0),
        is_available=True
    ),
    Item(
        id=2,
        name="Smartphone",
        description="Latest model smartphone with advanced features",
        price=899.99,
        category="Electronics",
        created_at=datetime(2023, 2, 10, 14, 30, 0),
        is_available=True
    ),
    Item(
        id=3,
        name="Coffee Maker",
        description="Automatic coffee maker with programmable timer",
        price=149.99,
        category="Home Appliances",
        created_at=datetime(2023, 3, 15, 11, 20, 0),
        is_available=False
    ),
    Item(
        id=4,
        name="Running Shoes",
        description="Comfortable running shoes for daily exercise",
        price=89.99,
        category="Sports",
        created_at=datetime(2023, 4, 20, 10, 15, 0),
        is_available=True
    )
]

orders_db = [
    Order(
        id=1,
        user_id=1,
        items=[items_db[0], items_db[1]],
        total_amount=2199.98,
        status="shipped",
        created_at=datetime(2023, 10, 15, 9, 30, 0),
        shipping_address="123 Main St, City, State 12345"
    ),
    Order(
        id=2,
        user_id=2,
        items=[items_db[3]],
        total_amount=89.99,
        status="delivered",
        created_at=datetime(2023, 10, 18, 14, 45, 0),
        shipping_address="456 Oak Ave, Town, State 67890"
    )
]

reviews_db = [
    ProductReview(
        id=1,
        product_id=1,
        user_id=1,
        rating=5,
        comment="Excellent laptop! Fast and reliable.",
        created_at=datetime(2023, 10, 16, 16, 20, 0)
    ),
    ProductReview(
        id=2,
        product_id=2,
        user_id=2,
        rating=4,
        comment="Great phone but battery could be better.",
        created_at=datetime(2023, 10, 19, 11, 30, 0)
    )
]

weather_data = [
    WeatherData(
        city="New York",
        temperature=22.5,
        humidity=65,
        description="Partly cloudy",
        timestamp=datetime(2023, 10, 26, 12, 0, 0)
    ),
    WeatherData(
        city="Los Angeles",
        temperature=28.0,
        humidity=45,
        description="Sunny",
        timestamp=datetime(2023, 10, 26, 12, 0, 0)
    ),
    WeatherData(
        city="Chicago",
        temperature=18.2,
        humidity=70,
        description="Rainy",
        timestamp=datetime(2023, 10, 26, 12, 0, 0)
    )
]

@app.get("/health")
def health() -> dict:
    """Health check endpoint returning 200 OK."""
    return {
        "status": "ok",
        "timestamp": datetime.now(),
        "version": "0.1.0",
        "service": "FastAPI UV Demo"
    }

@app.get("/hello")
def hello(name: Optional[str] = None) -> dict:
    """Simple greeting endpoint.

    - If `name` is provided, greet by name.
    - Otherwise, default to "World".
    """
    target = name.strip() if name else "World"
    return {"message": f"Hello, {target}!"}

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., ge=1, description="The ID of the item to get")) -> dict:
    """Return information about a specific item by ID."""
    item = next((item for item in items_db if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {
        "item_id": item.id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "created_at": item.created_at,
        "is_available": item.is_available,
        "additional_info": {
            "rating": random.uniform(3.0, 5.0),
            "reviews_count": random.randint(10, 100),
            "in_stock": random.randint(0, 50)
        }
    }

@app.get("/users", response_model=List[User])
def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return"),
    active_only: bool = Query(False, description="Filter to active users only")
) -> List[User]:
    """Get a list of users with pagination and filtering options."""
    filtered_users = users_db
    if active_only:
        filtered_users = [user for user in filtered_users if user.is_active]
    
    return filtered_users[skip:skip + limit]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int = Path(..., ge=1, description="The ID of the user to get")) -> User:
    """Get a specific user by ID."""
    user = next((user for user in users_db if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}/orders", response_model=List[Order])
def get_user_orders(user_id: int = Path(..., ge=1, description="The ID of the user to get orders for")) -> List[Order]:
    """Get all orders for a specific user."""
    user = next((user for user in users_db if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_orders = [order for order in orders_db if order.user_id == user_id]
    return user_orders

@app.get("/items", response_model=List[Item])
def list_items(
    category: Optional[str] = Query(None, description="Filter items by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    available_only: bool = Query(False, description="Filter to available items only"),
    sort_by: str = Query("id", enum=["id", "name", "price", "created_at"], description="Sort field"),
    sort_order: str = Query("asc", enum=["asc", "desc"], description="Sort order")
) -> List[Item]:
    """Get a list of items with filtering, sorting, and availability options."""
    filtered_items = items_db
    
    if category:
        filtered_items = [item for item in filtered_items if item.category.lower() == category.lower()]
    
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]
    
    if available_only:
        filtered_items = [item for item in filtered_items if item.is_available]
    
    # Sort items
    reverse = sort_order == "desc"
    if sort_by == "id":
        filtered_items.sort(key=lambda x: x.id, reverse=reverse)
    elif sort_by == "name":
        filtered_items.sort(key=lambda x: x.name, reverse=reverse)
    elif sort_by == "price":
        filtered_items.sort(key=lambda x: x.price, reverse=reverse)
    elif sort_by == "created_at":
        filtered_items.sort(key=lambda x: x.created_at, reverse=reverse)
    
    return filtered_items

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int = Path(..., ge=1, description="The ID of the order to get")) -> Order:
    """Get a specific order by ID."""
    order = next((order for order in orders_db if order.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/stats")
def get_stats() -> Dict[str, Any]:
    """Get application statistics."""
    total_users = len(users_db)
    active_users = len([user for user in users_db if user.is_active])
    total_items = len(items_db)
    available_items = len([item for item in items_db if item.is_available])
    total_orders = len(orders_db)
    total_revenue = sum(order.total_amount for order in orders_db)
    
    return {
        "timestamp": datetime.now(),
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": total_users - active_users
        },
        "items": {
            "total": total_items,
            "available": available_items,
            "unavailable": total_items - available_items
        },
        "orders": {
            "total": total_orders,
            "total_revenue": round(total_revenue, 2)
        },
        "categories": list(set(item.category for item in items_db)),
        "top_categories": {
            category: len([item for item in items_db if item.category == category])
            for category in set(item.category for item in items_db)
        }
    }

@app.get("/search")
def search_items(
    q: str = Query(..., min_length=1, description="Search query"),
    search_fields: List[str] = Query(["name", "description"], description="Fields to search in")
) -> Dict[str, Any]:
    """Search for items by name or description."""
    results = []
    q_lower = q.lower()
    
    for item in items_db:
        match = False
        if "name" in search_fields and q_lower in item.name.lower():
            match = True
        if "description" in search_fields and q_lower in item.description.lower():
            match = True
        
        if match:
            results.append(item)
    
    return {
        "query": q,
        "search_fields": search_fields,
        "results_count": len(results),
        "results": results
    }

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int = Path(..., ge=1, description="User ID to get recommendations for")) -> Dict[str, Any]:
    """Get personalized item recommendations for a user."""
    user = next((user for user in users_db if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Simple recommendation logic: return random available items
    recommended_items = [item for item in items_db if item.is_available]
    recommended_items = random.sample(recommended_items, min(5, len(recommended_items)))
    
    return {
        "user_id": user_id,
        "username": user.username,
        "recommendations": recommended_items,
        "algorithm": "random_available",
        "timestamp": datetime.now()
    }

@app.get("/weather")
def get_weather(city: Optional[str] = Query(None, description="City name to get weather for")) -> List[WeatherData]:
    """Get weather information for cities."""
    if city:
        weather = [w for w in weather_data if w.city.lower() == city.lower()]
        if not weather:
            raise HTTPException(status_code=404, detail=f"Weather data not found for city: {city}")
        return weather
    return weather_data

@app.get("/analytics")
def get_analytics() -> Dict[str, Any]:
    """Get detailed analytics about the application."""
    # Calculate price statistics
    prices = [item.price for item in items_db]
    avg_price = sum(prices) / len(prices) if prices else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    
    # Calculate order statistics
    order_totals = [order.total_amount for order in orders_db]
    avg_order_value = sum(order_totals) / len(order_totals) if order_totals else 0
    
    # Calculate user activity
    last_login_dates = [user.last_login for user in users_db if user.last_login]
    most_recent_login = max(last_login_dates) if last_login_dates else None
    
    return {
        "timestamp": datetime.now(),
        "item_analytics": {
            "total_items": len(items_db),
            "average_price": round(avg_price, 2),
            "min_price": min_price,
            "max_price": max_price,
            "price_distribution": {
                "under_100": len([p for p in prices if p < 100]),
                "100_to_500": len([p for p in prices if 100 <= p < 500]),
                "500_to_1000": len([p for p in prices if 500 <= p < 1000]),
                "over_1000": len([p for p in prices if p >= 1000])
            }
        },
        "order_analytics": {
            "total_orders": len(orders_db),
            "average_order_value": round(avg_order_value, 2),
            "total_revenue": round(sum(order_totals), 2)
        },
        "user_analytics": {
            "total_users": len(users_db),
            "active_users": len([u for u in users_db if u.is_active]),
            "most_recent_login": most_recent_login
        }
    }

@app.get("/dashboard")
def get_dashboard_data() -> Dict[str, Any]:
    """Get comprehensive dashboard data for admin view."""
    return {
        "timestamp": datetime.now(),
        "summary": {
            "users": len(users_db),
            "items": len(items_db),
            "orders": len(orders_db),
            "revenue": round(sum(order.total_amount for order in orders_db), 2)
        },
        "recent_activity": {
            "recent_orders": [
                {
                    "id": order.id,
                    "user_id": order.user_id,
                    "total": order.total_amount,
                    "status": order.status,
                    "date": order.created_at
                }
                for order in sorted(orders_db, key=lambda x: x.created_at, reverse=True)[:5]
            ],
            "recent_users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at
                }
                for user in sorted(users_db, key=lambda x: x.created_at, reverse=True)[:5]
            ]
        },
        "trends": {
            "daily_revenue": [
                {"date": "2023-10-24", "revenue": 1500.00},
                {"date": "2023-10-25", "revenue": 2300.50},
                {"date": "2023-10-26", "revenue": 1800.75}
            ],
            "popular_categories": [
                {"category": "Electronics", "count": 15},
                {"category": "Sports", "count": 8},
                {"category": "Home Appliances", "count": 5}
            ]
        }
    }
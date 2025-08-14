import json
import os
import time
from typing import Any

import requests

BASE = os.getenv("BASE_URL", "http://localhost:8000")


def pp(label: str, resp: requests.Response) -> None:
    print(f"\n== {label} ==")
    print(f"status={resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2, default=str))
    except Exception:
        print(resp.text)


def main() -> None:
    session = requests.Session()

    # Register unique user (ignore if email already used)
    email = f"alice_{int(time.time())}@example.com"
    password = "password123"
    r = session.post(
        f"{BASE}/auth/register",
        json={"email": email, "password": password, "full_name": "Alice"},
        timeout=10,
    )
    pp("register", r)

    # Login
    r = session.post(
        f"{BASE}/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    pp("login", r)
    data = r.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"login failed: {r.text}")
    auth = {"Authorization": f"Bearer {token}"}

    # Create category
    r = session.post(
        f"{BASE}/categories/",
        json={"name": "Electronics", "slug": f"electronics-{int(time.time())}"},
        timeout=10,
    )
    pp("create category", r)
    cat = r.json()
    category_id = cat.get("id")

    # Create product
    r = session.post(
        f"{BASE}/products/",
        json={
            "name": "Headphones",
            "slug": f"headphones-{int(time.time())}",
            "price": 49.99,
            "in_stock": True,
            "category_id": category_id,
        },
        timeout=10,
    )
    pp("create product", r)
    prod = r.json()

    # Add to cart
    r = session.post(
        f"{BASE}/cart/me/items",
        headers=auth,
        json={"product_id": prod.get("id"), "quantity": 2},
        timeout=10,
    )
    pp("cart after add", r)

    # Get cart
    r = session.get(f"{BASE}/cart/me", headers=auth, timeout=10)
    pp("cart get", r)

    # Place order
    r = session.post(f"{BASE}/orders/me", headers=auth, json={}, timeout=10)
    pp("place order", r)

    # List orders
    r = session.get(f"{BASE}/orders/me", headers=auth, timeout=10)
    pp("orders", r)


if __name__ == "__main__":
    main()
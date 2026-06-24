#!/usr/bin/env python3
"""
MongoDB initialization script with test data
This will be executed when the container starts
"""

from pymongo import MongoClient
from datetime import datetime
import time
import sys

def init_mongodb():
    """Initialize MongoDB with test databases and collections"""
    
    # Wait for MongoDB to be ready
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Connect to MongoDB (no auth)
            client = MongoClient('mongodb://localhost:27017/', 
                               serverSelectionTimeoutMS=2000)
            client.admin.command('ismaster')
            print("✓ Connected to MongoDB successfully")
            break
        except Exception as e:
            attempt += 1
            print(f"⏳ Waiting for MongoDB to be ready... ({attempt}/{max_attempts})")
            time.sleep(1)
    
    if attempt >= max_attempts:
        print("❌ Failed to connect to MongoDB")
        sys.exit(1)
    
    # ============ Database 1: testdb ============
    print("\n📦 Creating database: testdb")
    db = client.testdb
    
    # Create users collection
    print("  - Creating collection: users")
    db.users.drop()  # Remove if exists
    db.users.insert_many([
        {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "active": True,
            "created_at": datetime.now(),
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zip": "10001"
            }
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 25,
            "active": True,
            "created_at": datetime.now(),
            "address": {
                "street": "456 Oak Ave",
                "city": "Los Angeles",
                "zip": "90001"
            }
        },
        {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "age": 35,
            "active": False,
            "created_at": datetime.now(),
            "address": {
                "street": "789 Pine Rd",
                "city": "Chicago",
                "zip": "60601"
            }
        }
    ])
    print(f"    → Inserted {db.users.count_documents({})} users")
    
    # Create products collection
    print("  - Creating collection: products")
    db.products.drop()
    db.products.insert_many([
        {
            "name": "Laptop",
            "price": 999.99,
            "category": "electronics",
            "in_stock": True,
            "specs": {
                "ram": "16GB",
                "storage": "512GB SSD",
                "processor": "Intel i7"
            },
            "tags": ["computer", "work", "portable"]
        },
        {
            "name": "Mouse",
            "price": 29.99,
            "category": "electronics",
            "in_stock": True,
            "specs": {
                "type": "wireless",
                "dpi": 1600
            },
            "tags": ["computer", "accessory"]
        },
        {
            "name": "Desk",
            "price": 249.99,
            "category": "furniture",
            "in_stock": False,
            "specs": {
                "material": "wood",
                "dimensions": "60x30 inches"
            },
            "tags": ["office", "furniture"]
        }
    ])
    print(f"    → Inserted {db.products.count_documents({})} products")
    
    # Create orders collection
    print("  - Creating collection: orders")
    db.orders.drop()
    db.orders.insert_many([
        {
            "order_id": "ORD-001",
            "user_email": "john@example.com",
            "product": "Laptop",
            "quantity": 1,
            "total": 999.99,
            "status": "delivered",
            "order_date": datetime(2024, 1, 15),
            "payment_method": "credit_card"
        },
        {
            "order_id": "ORD-002",
            "user_email": "jane@example.com",
            "product": "Mouse",
            "quantity": 2,
            "total": 59.98,
            "status": "shipped",
            "order_date": datetime(2024, 2, 1),
            "payment_method": "paypal"
        },
        {
            "order_id": "ORD-003",
            "user_email": "bob@example.com",
            "product": "Desk",
            "quantity": 1,
            "total": 249.99,
            "status": "pending",
            "order_date": datetime.now(),
            "payment_method": "bank_transfer"
        }
    ])
    print(f"    → Inserted {db.orders.count_documents({})} orders")
    
    # Create indexes
    print("  - Creating indexes")
    db.users.create_index("email", unique=True)
    db.products.create_index([("category", 1), ("price", -1)])
    db.orders.create_index("order_id", unique=True)
    db.orders.create_index("user_email")
    print("    → Indexes created")
    
    # ============ Database 2: analytics_db ============
    print("\n📦 Creating database: analytics_db")
    db2 = client.analytics_db
    
    # Create visits collection
    print("  - Creating collection: visits")
    db2.visits.drop()
    db2.visits.insert_many([
        {
            "page": "/home",
            "visits": 1500,
            "unique_visitors": 850,
            "date": datetime.now(),
            "avg_time": 120  # seconds
        },
        {
            "page": "/products",
            "visits": 800,
            "unique_visitors": 450,
            "date": datetime.now(),
            "avg_time": 180
        },
        {
            "page": "/about",
            "visits": 300,
            "unique_visitors": 200,
            "date": datetime.now(),
            "avg_time": 90
        },
        {
            "page": "/contact",
            "visits": 150,
            "unique_visitors": 100,
            "date": datetime.now(),
            "avg_time": 60
        }
    ])
    print(f"    → Inserted {db2.visits.count_documents({})} visit records")
    
    # ============ Database 3: logs_db ============
    print("\n📦 Creating database: logs_db")
    db3 = client.logs_db
    
    # Create app_logs collection
    print("  - Creating collection: app_logs")
    db3.app_logs.drop()
    
    # Insert multiple log entries
    log_entries = []
    log_levels = ["info", "warning", "error", "debug"]
    
    for i in range(20):
        from random import choice
        log_entries.append({
            "level": choice(log_levels),
            "message": f"Log entry #{i+1}",
            "service": "mongodb",
            "timestamp": datetime.now(),
            "host": "mongodb-test"
        })
    
    db3.app_logs.insert_many(log_entries)
    print(f"    → Inserted {db3.app_logs.count_documents({})} log entries")
    
    # ============ Database 4: empty_db (for testing) ============
    print("\n📦 Creating database: empty_db")
    db4 = client.empty_db
    # Create an empty collection
    db4.create_collection("empty_collection")
    print("    → Created empty collection")
    
    # ============ Summary ============
    print("\n" + "="*50)
    print("✅ MongoDB test data initialized successfully!")
    print("="*50)
    print("\n📊 Databases created:")
    print("  • testdb")
    print("    - users (3 documents)")
    print("    - products (3 documents)") 
    print("    - orders (3 documents)")
    print("  • analytics_db")
    print("    - visits (4 documents)")
    print("  • logs_db")
    print("    - app_logs (20 documents)")
    print("  • empty_db")
    print("    - empty_collection (0 documents)")
    print("="*50)
    print("\n🔧 Connection string: mongodb://localhost:27017")
    print("🔐 Authentication: Disabled")
    print("="*50)
    
    client.close()

if __name__ == "__main__":
    init_mongodb()

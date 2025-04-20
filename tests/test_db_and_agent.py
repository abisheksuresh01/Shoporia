import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.db.models import User, Product, Order, OrderItem
from app.services.ai_service import AIService
from app.core.security import verify_password

def test_database_retrieval():
    """Test retrieving data from the database"""
    db = SessionLocal()
    try:
        # Test user retrieval
        print("\nTesting User Retrieval:")
        users = db.query(User).all()
        for user in users:
            print(f"User: {user.email} (Active: {user.is_active})")
            # Test password verification
            if user.email == "customer1@example.com":
                is_valid = verify_password("password123", user.hashed_password)
                print(f"Password verification for {user.email}: {'Success' if is_valid else 'Failed'}")

        # Test product retrieval
        print("\nTesting Product Retrieval:")
        products = db.query(Product).all()
        for product in products:
            print(f"Product: {product.name} - ${product.price} (Stock: {product.stock})")

        # Test order retrieval with items
        print("\nTesting Order Retrieval:")
        orders = db.query(Order).all()
        for order in orders:
            print(f"\nOrder for user {order.user_id}:")
            print(f"Status: {order.status}")
            print(f"Total Amount: ${order.total_amount}")
            print("Order Items:")
            for item in order.items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                print(f"  - {product.name} x{item.quantity} @ ${item.price}")

    finally:
        db.close()

async def test_agent_functionality():
    """Test the AI agent's functionality"""
    ai_service = AIService()
    
    # Test product information retrieval
    print("\nTesting Product Info Retrieval:")
    product_info = await ai_service.get_product_info(1)
    print(f"Product Info: {product_info}")

    # Test order status check
    print("\nTesting Order Status Check:")
    order_status = await ai_service.check_order_status("ORDER123")
    print(f"Order Status: {order_status}")

    # Test message processing
    print("\nTesting Message Processing:")
    test_messages = [
        "What's the status of my order?",
        "Tell me about the Smartphone X",
        "I want to return my Laptop Pro"
    ]
    
    for message in test_messages:
        print(f"\nCustomer Message: {message}")
        response = await ai_service.process_message(message, [])
        print(f"Agent Response: {response}")

if __name__ == "__main__":
    print("Testing Database Retrieval...")
    test_database_retrieval()
    
    print("\nTesting Agent Functionality...")
    import asyncio
    asyncio.run(test_agent_functionality()) 
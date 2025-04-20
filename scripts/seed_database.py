import os
import sys
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from app.db.session import SessionLocal
from app.db.models import User, Product, Order, OrderItem, Message, Conversation
from app.core.security import get_password_hash
from app.services.ai_service import AIService

def generate_order_number():
    """Generate a random order number"""
    ai_service = AIService()
    return ai_service.generate_order_number()

def seed_database(force_reseed=False):
    """Seed the database with test data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0 and not force_reseed:
            print("Database already seeded. Skipping.")
            return
        
        if force_reseed:
            print("Force reseeding database...")
            # Clear existing data
            db.query(OrderItem).delete()
            db.query(Order).delete()
            db.query(Product).delete()
            db.query(Message).delete()
            db.query(Conversation).delete()
            db.query(User).delete()
            db.commit()
            print("Existing data cleared.")
        
        print("Seeding database with test data...")
        
        # Create users
        users = [
            User(
                email="customer1@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="John Doe",
                is_active=True
            ),
            User(
                email="customer2@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="Jane Smith",
                is_active=True
            ),
            User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                is_active=True,
                is_superuser=True
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print(f"Created {len(users)} users")
        
        # Create products
        products = [
            Product(
                name="Smartphone X",
                description="Latest smartphone with advanced features",
                price=999.99,
                stock=50,
                category="Electronics"
            ),
            Product(
                name="Laptop Pro",
                description="High-performance laptop for professionals",
                price=1499.99,
                stock=30,
                category="Electronics"
            ),
            Product(
                name="Wireless Headphones",
                description="Noise-cancelling wireless headphones",
                price=199.99,
                stock=100,
                category="Audio"
            ),
            Product(
                name="Smart Watch",
                description="Fitness tracker and smartwatch",
                price=299.99,
                stock=75,
                category="Wearables"
            ),
            Product(
                name="Coffee Maker",
                description="Automatic coffee maker with timer",
                price=79.99,
                stock=40,
                category="Kitchen"
            )
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        print(f"Created {len(products)} products")
        
        # Create orders
        statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
        payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]
        
        # Get user IDs
        user_ids = [user.id for user in db.query(User).all()]
        
        # Create orders for each user
        for user_id in user_ids:
            # Create 1-3 orders per user
            for _ in range(random.randint(1, 3)):
                # Random order date within the last 30 days
                order_date = datetime.now() - timedelta(days=random.randint(0, 30))
                
                # Create order
                order = Order(
                    user_id=user_id,
                    order_number=generate_order_number(),
                    order_date=order_date,
                    status=random.choice(statuses),
                    total_amount=0,  # Will be calculated after adding items
                    payment_method=random.choice(payment_methods),
                    shipping_address="123 Main St, Anytown, USA"
                )
                
                db.add(order)
                db.flush()  # Get the order ID without committing
                
                # Add 1-3 items to the order
                order_total = 0
                for _ in range(random.randint(1, 3)):
                    product = random.choice(products)
                    quantity = random.randint(1, 3)
                    price = product.price
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        price=price
                    )
                    
                    db.add(order_item)
                    order_total += price * quantity
                
                # Update order total
                order.total_amount = order_total
        
        db.commit()
        print(f"Created orders for {len(user_ids)} users")
        
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Check if force reseed flag is provided
    force_reseed = "--force" in sys.argv
    seed_database(force_reseed) 
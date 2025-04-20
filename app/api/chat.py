from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.db.session import get_db
from app.services.ai_service import AIService
from app.db.models import Product, Order, User, OrderItem
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
ai_service = AIService()

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[Dict]

class ChatResponse(BaseModel):
    response: str
    debug_info: Dict

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    debug_info = {
        "database_query": None,
        "agent_processing": None
    }
    
    try:
        # Process the message with the AI service
        agent_response = await ai_service.process_message(
            request.message,
            request.conversation_history
        )
        
        # Extract action and data from agent response
        action = agent_response.get("action_needed")
        action_data = agent_response.get("action_data", {})
        
        # Handle different types of queries
        if action == "Look up product information":
            product_name = action_data.get("product")
            if product_name:
                product = db.query(Product).filter(Product.name == product_name).first()
                if product:
                    debug_info["database_query"] = {
                        "type": "product_lookup",
                        "product_name": product_name,
                        "result": {
                            "name": product.name,
                            "price": product.price,
                            "stock": product.stock,
                            "description": product.description
                        }
                    }
                    # Update agent response with actual product data
                    agent_response["response"] = f"The {product.name} is priced at ${product.price} and we have {product.stock} in stock. {product.description}"
        
        elif action == "Check order status":
            # In a real application, you would extract the order number from the message
            # For demo purposes, we'll just show the most recent order
            order = db.query(Order).order_by(Order.created_at.desc()).first()
            if order:
                debug_info["database_query"] = {
                    "type": "order_lookup",
                    "order_id": order.id,
                    "result": {
                        "status": order.status,
                        "total_amount": order.total_amount,
                        "items": [
                            {
                                "product_id": item.product_id,
                                "quantity": item.quantity,
                                "price": item.price
                            } for item in order.items
                        ]
                    }
                }
                # Update agent response with actual order data
                agent_response["response"] = f"Your order is currently {order.status}. The total amount is ${order.total_amount}."
        
        elif action == "Cancel order":
            # Extract order number from the message or conversation history
            order_number = action_data.get("order_number")
            if order_number:
                order = db.query(Order).filter(Order.order_number == order_number).first()
                if order:
                    # Update order status to Cancelled
                    order.status = "Cancelled"
                    db.commit()
                    
                    debug_info["database_query"] = {
                        "type": "order_cancellation",
                        "order_number": order_number,
                        "result": {
                            "status": "Cancelled",
                            "order_id": order.id
                        }
                    }
                    
                    agent_response["response"] = f"Your order {order_number} has been cancelled successfully."
                else:
                    agent_response["response"] = f"I couldn't find an order with the number {order_number}. Please check and try again."
            else:
                agent_response["response"] = "I need the order number to cancel your order. Please provide it."
        
        elif action == "Place order":
            # Extract order details from the message or conversation history
            product_name = action_data.get("product")
            quantity = action_data.get("quantity", 1)
            shipping_address = action_data.get("shipping_address")
            payment_method = action_data.get("payment_method", "Credit Card")
            
            if product_name and shipping_address:
                product = db.query(Product).filter(Product.name == product_name).first()
                if product:
                    # Check if cash on delivery is valid (under $100)
                    total_amount = product.price * quantity
                    if payment_method == "Cash on Delivery" and total_amount >= 100:
                        agent_response["response"] = "Cash on Delivery is only available for orders under $100. Your order total is ${:.2f}. Please choose a different payment method.".format(total_amount)
                    else:
                        # Generate order number
                        order_number = ai_service.generate_order_number()
                        
                        # Create new order
                        new_order = Order(
                            user_id=1,  # Default user for demo
                            order_number=order_number,
                            status="Pending",
                            total_amount=total_amount,
                            payment_method=payment_method,
                            shipping_address=shipping_address,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        db.add(new_order)
                        db.flush()  # Get the order ID without committing
                        
                        # Create order item
                        order_item = OrderItem(
                            order_id=new_order.id,
                            product_id=product.id,
                            quantity=quantity,
                            price=product.price
                        )
                        db.add(order_item)
                        
                        # Update product stock
                        product.stock -= quantity
                        
                        db.commit()
                        
                        debug_info["database_query"] = {
                            "type": "order_placement",
                            "order_number": order_number,
                            "result": {
                                "order_id": new_order.id,
                                "product": product_name,
                                "quantity": quantity,
                                "total_amount": total_amount,
                                "payment_method": payment_method,
                                "shipping_address": shipping_address
                            }
                        }
                        
                        agent_response["response"] = f"Your order has been placed successfully! Your order number is {order_number}. Total amount: ${total_amount:.2f}. Payment method: {payment_method}. Shipping address: {shipping_address}."
                else:
                    agent_response["response"] = f"I couldn't find a product named {product_name}. Please check the product name and try again."
            else:
                agent_response["response"] = "I need the product name and shipping address to place your order. Please provide them."
        
        debug_info["agent_processing"] = {
            "original_response": agent_response,
            "action_taken": action,
            "action_data": action_data
        }
        
        return ChatResponse(
            response=agent_response["response"],
            debug_info=debug_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
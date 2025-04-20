from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.services.ai_service import AIService
from app.schemas.chat import MessageCreate, MessageResponse, ConversationResponse
from app.db.models import Conversation, Message, User
from datetime import datetime

router = APIRouter()
ai_service = AIService()

@router.post("/conversations/", response_model=ConversationResponse)
async def create_conversation(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.post("/conversations/{conversation_id}/messages/", response_model=MessageResponse)
async def create_message(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """Send a message in a conversation"""
    # Get conversation history
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        content=message.content,
        is_from_user=True
    )
    db.add(user_message)
    
    # Get conversation history for context
    history = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(10).all()
    
    history_dict = [
        {
            "content": msg.content,
            "is_from_user": msg.is_from_user
        }
        for msg in reversed(history)
    ]
    
    # Get AI response
    ai_response = await ai_service.process_message(message.content, history_dict)
    
    # Save AI response
    ai_message = Message(
        conversation_id=conversation_id,
        content=ai_response["response"],
        is_from_user=False
    )
    db.add(ai_message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ai_message)
    
    return ai_message

@router.get("/conversations/{conversation_id}/messages/", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()
    return messages 
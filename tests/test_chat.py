from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_conversation(client):
    response = client.post("/api/v1/chat/conversations/", json={"user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["user_id"] == 1

def test_create_message(client):
    # First create a conversation
    conv_response = client.post("/api/v1/chat/conversations/", json={"user_id": 1})
    conversation_id = conv_response.json()["id"]
    
    # Then create a message
    response = client.post(
        f"/api/v1/chat/conversations/{conversation_id}/messages/",
        json={"content": "Hello, I need help with my order"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, I need help with my order"
    assert data["conversation_id"] == conversation_id
    assert data["is_from_user"] == True

def test_get_conversation_messages(client):
    # First create a conversation
    conv_response = client.post("/api/v1/chat/conversations/", json={"user_id": 1})
    conversation_id = conv_response.json()["id"]
    
    # Create a message
    client.post(
        f"/api/v1/chat/conversations/{conversation_id}/messages/",
        json={"content": "Hello, I need help with my order"}
    )
    
    # Get messages
    response = client.get(f"/api/v1/chat/conversations/{conversation_id}/messages/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["content"] == "Hello, I need help with my order" 
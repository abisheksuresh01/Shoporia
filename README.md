# E-commerce Customer Service Agent

An intelligent customer service agent for e-commerce platforms powered by Google's Gemini 2.0 Flash AI. This agent can handle customer inquiries, process orders, and provide support 24/7.

## Features

- Natural language processing for customer inquiries using Google's Gemini 2.0 Flash
- Order tracking and management
- Product information retrieval
- Return and refund processing
- Customer feedback analysis
- Multi-channel support (web, email, chat)
- Authentication and authorization
- Database integration for persistent storage

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_agent
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core functionality
│   ├── db/             # Database models and migrations
│   ├── services/       # Business logic
│   ├── schemas/        # Pydantic models
│   └── utils/          # Utility functions
├── examples/           # Example scripts
├── tests/              # Test files
├── alembic/            # Database migrations
├── .env                # Environment variables
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with:
```bash
pytest
```

## Demo

To run the Gemini demo script:
```bash
python examples/gemini_demo.py
``` 
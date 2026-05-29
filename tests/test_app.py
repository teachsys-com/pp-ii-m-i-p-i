import os
from sqlalchemy import text
from fastapi.testclient import TestClient

# Set environment to use SQLite for tests
os.environ["USE_SQLITE"] = "true"

from app.database import engine
from app.main import app
from app.load_data import parse_squad_answer

client = TestClient(app)


def test_db_connection():
    """
    Test 1: Verify the database engine connection works.
    This connects to the configured database (which defaults to SQLite in test environment).
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_questions():
    """
    Test 2: Verify the GET /questions API endpoint works and returns a JSON list.
    """
    # Trigger database tables creation
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    
    response = client.get("/questions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_parse_squad_answer():
    """
    Test 3: Test a different layer (Data Ingestion/Parsing layer helper).
    Verifies that the parse_squad_answer helper correctly extracts the first text string.
    """
    # Case 1: Standard dictionary with non-empty list
    mock_dict = {"text": ["Super Bowl 50", "Super Bowl L"], "answer_start": [177, 177]}
    assert parse_squad_answer(mock_dict) == "Super Bowl 50"

    # Case 2: Empty lists
    mock_empty = {"text": [], "answer_start": []}
    assert parse_squad_answer(mock_empty) == ""

    # Case 3: None/non-dictionary format fallback
    assert parse_squad_answer(None) == ""

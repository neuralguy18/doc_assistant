import pytest
from langgraph.graph import StateGraph

from src.state import AgentState
from src.graph import app  # your LangGraph runnable
from src.tools.tools import document_search_tool, document_reader_tool


def test_qa_e2e(monkeypatch):
    """
    End-to-end test for QA intent:
    - search tool must be called
    - document reader must be called
    - answer must come from retrieved doc
    """

    # Mock tools
    monkeypatch.setattr(document_search_tool, "run", lambda query: ["doc123"])
    monkeypatch.setattr(document_reader_tool, "run", lambda doc_id: {
        "id": doc_id,
        "content": "Interest rate is 7.5% annually."
    })

    # Initial graph state
    state = {
        "intent": {
            "intent_type": "qa",
            "input_text": "What is the interest rate?"
        },
        "conversation_history": [],
        "document_context": []
    }

    result = app.invoke(state)

    assert "7.5%" in result["response"]
    assert "Interest rate" in result["response"]

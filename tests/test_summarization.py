import pytest
from src.graph import app
from src.tools.tools import document_search_tool, document_reader_tool


def test_summarization_e2e(monkeypatch):
    """
    End-to-end test for summarization intent.
    Validates:
    - search tool is called first
    - reader tool is called for each doc
    - summarization LLM produces structured summary
    """

    # Mock search tool → return 2 doc IDs
    monkeypatch.setattr(document_search_tool, "run", lambda query: ["doc1", "doc2"])

    # Mock reader tool → return doc content
    monkeypatch.setattr(
        document_reader_tool,
        "run",
        lambda doc_id: {
            "id": doc_id,
            "content": f"{doc_id} contains financial information for 2024."
        }
    )

    # Mock summarization LLM → produce known output
    def mock_summarizer_call(prompt):
        return (
            "Summary:\n"
            "- doc1: contains financial information for 2024.\n"
            "- doc2: contains financial information for 2024.\n"
            "Key points extracted successfully."
        )

    monkeypatch.setattr("src.agents.summarization_agent.llm.invoke", mock_summarizer_call)

    state = {
        "intent": {"intent_type": "summarization", "input_text": "summarize the financial docs"},
        "conversation_history": [],
        "document_context": []
    }

    result = app.invoke(state)
    resp = result["response"]

    assert "Summary:" in resp
    assert "- doc1" in resp
    assert "- doc2" in resp
    assert "Key points" in resp

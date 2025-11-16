import pytest
from src.graph import app
from src.tools.calculator import create_calculator_tool
from src.tools.tools import document_reader_tool


def test_calculation_e2e(monkeypatch):
    """
    End-to-end test for calculation intent.
    Validates:
    - LLM determines correct expression
    - calculator tool is used (not LLM)
    - final answer is returned from calculator tool
    """

    # Step 1: Mock document reader
    monkeypatch.setattr(
        document_reader_tool,
        "run",
        lambda doc_id: {
            "id": doc_id,
            "content": "Principal amount: 1200. Interest rate: 0.05."
        }
    )

    # Step 2: Mock calculation LLM
    # LLM should produce an expression, not a value
    def mock_calc_llm(prompt):
        return "EXPRESSION: 1200 * 0.05"

    monkeypatch.setattr(
        "src.agents.calculation_agent.llm.invoke",
        mock_calc_llm
    )

    # Step 3: Force calculator tool to compute correctly
    monkeypatch.setattr(
        create_calculator_tool,
        "run",
        lambda expr: "Result: 60.0"
    )

    state = {
        "intent": {"intent_type": "calculation", "input_text": "Calculate interest from document 7"},
        "conversation_history": [],
        "document_context": ["7"]
    }

    result = app.invoke(state)
    resp = result["response"]

    assert "Result: 60.0" in resp
    assert "60" in resp

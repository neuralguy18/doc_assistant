Multi-Agent LangGraph Assistant With Memory, Tools, and Structured Output

This project implements a production-grade multi-agent assistant using LangGraph, LangChain, Pydantic structured outputs, and custom document + calculator tools.
The system routes user requests to specialized agents—Q&A, Summarization, or Calculation—based on LLM intent detection.
It also maintains persistent memory and conversation summaries using checkpointers.

1. System Architecture

The assistant follows a multi-agent graph design powered by LangGraph.

Why LangGraph?

LangGraph provides:

    - Deterministic routing using conditional edges

    - Persistent memory through checkpointers

    - Clear separation of agents

    - State-driven execution

Built-in support for multi-message histories

Graph Overview
┌─────────────────┐
│  classify_intent │
└─────────┬───────┘
          │
          ▼
 ┌──────────────┬──────────────────────┬──────────────────────┐
 │   qa_agent   │ summarization_agent  │ calculation_agent     │
 └──────────────┴──────────────────────┴──────────────────────┘
          │
          ▼
   ┌──────────────┐
   │ update_memory │
   └───────┬──────┘
           ▼
          END


2. Tools
2.1 Document Search Tool

Allows the assistant to:

    - Search documents by keyword

    - Filter by type

    - Filter by amount (over/under/between)

    - Parse natural-language amount queries

Used by:
Q&A agent, Summarization agent, Calculation agent

2.2 Calculator Tool

A safe arithmetic tool:

    - Accepts math expressions

    - Validates using regex

    - Uses sandboxed eval()

    - Returns Result: X

    - Logged through ToolLogger

Used exclusively by:
calculation_agent

3. Agents

Each agent uses a task-specific system prompt, tools, message history, and structured response schema.

3.1 classify_intent

Uses:

    - conversation history

    - latest user message

    - intent classification prompt

Routing:
    * qa → qa_agent

    * summarization → summarization_agent

    * calculation → calculation_agent

    * default → qa_agent

3.2 qa_agent

Retrieves:

    - system prompt (QA_SYSTEM_PROMPT)

    - chat history

    - user input

Uses tools:

    - document_search

    - possibly calculator

Returns AnswerResponse.

3.3 summarization_agent

Retrieves:

    - all relevant documents

    - summarizes using structured output

Uses:

    - document_search tool

Returns SummarizationResponse.

3.4 calculation_agent

Steps:

    1. Locates document containing numeric information

    2. Determines mathematical expression

    3. Uses calculator tool for all arithmetic

    4. Returns CalculationResponse


3.5 update_memory

Uses:

    - MEMORY_SUMMARY_PROMPT

    - messages history

Returns:

    - conversation_summary

    - active_documents

Provides continuity across turns.
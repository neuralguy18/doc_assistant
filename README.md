Multi-Agent LangGraph Assistant With Memory, Tools, and Structured Output

This project implements a production-grade multi-agent assistant using LangGraph, LangChain, Pydantic structured outputs, and custom document + calculator tools.
The system routes user requests to specialized agents—Q&A, Summarization, or Calculation—based on LLM intent detection.
It also maintains persistent memory and conversation summaries using checkpointers.

1. System Architecture

The assistant follows a multi-agent ggiraph design powered by LangGraph.

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


4. Example conversations :
a.  Input message : Multiply 7*890

    🤖 Assistant: The result of multiplying 7 by 890 is 6,230.

    INTENT: calculation

    TOOLS USED: calculator

    CONVERSATION SUMMARY: The user requested the multiplication of 7 by 890. The calculation was performed, resulting in 6,230.

b.  Input Message : Summarize doc_id INV-002
    Assistant: **Summary of Document INV-002:**

    - **Invoice Number:** 12346
    - **Date:** February 20, 2024
    - **Client:** TechStart Inc.
    - **Products and Services:**
    - Enterprise License (Annual): $50,000
    - Implementation Services: $15,000
    - Training Package: $5,000
    - **Financial Details:**
    - **Subtotal:** $70,000
    - **Discount:** 10% ($7,000)
    - **Tax:** 10% ($6,300)
    - **Total Due:** $69,300
    - **Payment Terms:** Net 45 days

    This invoice outlines the purchase of an enterprise license, implementation services, and a training package, with a total amount due of $69,300 after applying a discount and tax.

    INTENT: summarization

    TOOLS USED: calculator, document_reader

    CONVERSATION SUMMARY: The user requested a multiplication of 7 by 890, which resulted in 6,230. Later, the user asked for a summary of document INV-002, which is an invoice for TechStart Inc. dated February 20, 2024. The invoice includes charges for an Enterprise License, Implementation Services, and a Training Package, with a subtotal of $70,000. A 10% discount and a 10% tax were applied, resulting in a total due of $69,300, with payment terms of net 45 days.


c.  Input Message: What is the title of doc_id CLM-001?
    🤖 Assistant: The title of document CLM-001 is "INSURANCE CLAIM FORM."

    INTENT: qa

    TOOLS USED: calculator, document_reader, document_reader

    CONVERSATION SUMMARY: The user requested a multiplication calculation for 7*890, which resulted in 6,230. Later, the user asked for a summary of document INV-002, which is an invoice for TechStart Inc. dated February 20, 2024, with a total due of $69,300 after discounts and taxes. The invoice includes charges for an enterprise license, implementation services, and a training package. The user also inquired about the title of document CLM-001, which is an "INSURANCE CLAIM FORM" for a medical expense reimbursement claim by John Doe, totaling $2,450 and currently under review.


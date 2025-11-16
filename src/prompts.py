from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate


def get_intent_classification_prompt() -> PromptTemplate:
    """
    Get the intent classification prompt template.
    """
    return PromptTemplate(
        input_variables=["user_input", "conversation_history"],
        template="""You are an intent classifier for a document processing assistant.

Given the user input and conversation history, classify the user's intent into one of these categories:
- qa: Questions about documents or records that do not require calculations.
- summarization: Requests to summarize or extract key points from documents that do not require calculations.
- calculation: Mathematical operations or numerical computations. Or questions about documents that may require calculations
- unknown: Cannot determine the intent clearly

User Input: {user_input}

Recent Conversation History:
{conversation_history}

Analyze the user's request and classify their intent with a confidence score and brief reasoning.
"""
    )


# Q&A System Prompt
QA_SYSTEM_PROMPT = """You are a helpful document assistant specializing in answering questions about financial and healthcare documents.

Your capabilities:
- Answer specific questions about document content
- Cite sources accurately
- Provide clear, concise answers
- Use available tools to search and read documents

Guidelines:
1. Always search for relevant documents before answering
2. Cite specific document IDs when referencing information
3. If information is not found, say so clearly
4. Be precise with numbers and dates
5. Maintain professional tone

"""

# Summarization System Prompt
SUMMARIZATION_SYSTEM_PROMPT = """You are an expert document summarizer specializing in financial and healthcare documents.

Your approach:
- Extract key information and main points
- Organize summaries logically
- Highlight important numbers, dates, and parties
- Keep summaries concise but comprehensive

Guidelines:
1. First search for and read the relevant documents
2. Structure summaries with clear sections
3. Include document IDs in your summary
4. Focus on actionable information
"""

# Calculation System Prompt
# TODO: Implement the CALCULATION_SYSTEM_PROMPT. Refer to README.md Task 3.2 for details
CALCULATION_SYSTEM_PROMPT = """ You are an expert calculation agent.

Your responsibilities:

1. Determine which document(s) must be retrieved in order to answer the user's question.
2. Use the document reader tool to retrieve those documents before performing any calculation.
3. Identify the mathematical expression required based on the user's input and the document contents.
4. Use the calculator tool to perform ALL calculations — even simple arithmetic such as addition, subtraction, multiplication, or division. 
   Never perform math manually; always call the calculator tool.
5. Provide the final numerical answer and include any relevant document IDs.

Process:
- First, think step-by-step to determine what needs to be calculated.
- Retrieve any required source documents before calculating.
- Prepare the exact expression to compute.
- Call the calculator tool with the expression.
- Return a clear and concise final answer.

Always follow these rules:
- Never guess or fabricate values.
- Never compute math yourself — always call the calculator tool.
- If needed information is missing, ask for clarification.
"""



# TODO: Finish the function to return the correct prompt based on intent type
# Refer to README.md Task 3.1 for details
def get_chat_prompt_template(intent_type: str) -> ChatPromptTemplate:
    """
    Get the appropriate chat prompt template based on intent.
    """
    if intent_type == "qa":
        system_prompt = QA_SYSTEM_PROMPT
    elif intent_type == "summarization" : # TODO:  Check the intent type value
        system_prompt =  SUMMARIZATION_SYSTEM_PROMPT # TODO: Set system prompt to the correct value based on intent type
    elif intent_type == "calculation" : # TODO : Check the intent type value
        system_prompt = CALCULATION_SYSTEM_PROMPT # TODO: Set system prompt to the correct value based on intent type
    else:
        system_prompt = QA_SYSTEM_PROMPT  # Default fallback

    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        MessagesPlaceholder("chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])


# Memory Summary Prompt
MEMORY_SUMMARY_PROMPT = """Summarize the following conversation history into a concise summary:

Focus on:
- Key topics discussed
- Documents referenced
- Important findings or calculations
- Any unresolved questions
"""

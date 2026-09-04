# Agentic AI Operations Assistant

An AI-powered assistant designed to support business operations teams. It understands operational requests, investigates issues, retrieves relevant information, and interacts with business systems — autonomously and end-to-end.

Presented by **Nada Ayman**.

## Problem

Operations teams handle large amounts of data and repetitive requests. Information is often scattered across databases, documents, and business systems, and investigating an issue manually can be time-consuming and error-prone.

## Solution

The **Agentic AI Operations Assistant** autonomously investigates operational requests:

- Retrieves information from databases and internal documents
- Uses the appropriate tools to analyze the situation
- Provides a clear answer or takes an authorized action

It's built on **AI Agents**, **Retrieval-Augmented Generation (RAG)**, and a set of specialized tools that let it perform multi-step tasks rather than just answering one-off questions.

## Example Scenarios

| Scenario | Example Request |
|---|---|
| **Delayed Order** | "Why is order #4582 delayed, and what should we do?" |
| **Refund Request** | "Customer wants a refund for order #3910. Is the customer eligible?" |
| **Customer Complaint** | "This customer has complained three times. Should we escalate the case?" |

In each case, the assistant investigates the relevant records, reasons over the retrieved context, and returns a decision or recommended action.

## Project Structure

```
.
├── agent.py              # Core agent logic / orchestration
├── api.py                # API layer for serving the assistant
├── data/                 # Operational data (orders, customers, etc.)
├── frontend/             # User-facing interface
├── knowledge/            # Internal documents / knowledge base
├── rag/                  # Retrieval-Augmented Generation pipeline
├── tools/                # Specialized tools the agent can invoke
├── tests/                # Test suite
├── docker-compose.yml    # Container orchestration
├── requirements.txt      # Python dependencies
├── gemini_test.py        # Gemini model integration tests
├── llm_test.py           # General LLM tests
└── test_data.py          # Test data utilities
```

## How It Works

1. **Understand** — The assistant parses the operational request to identify intent (e.g., delayed order, refund, complaint).
2. **Retrieve** — Using RAG, it pulls relevant records from the database and knowledge base.
3. **Analyze** — The agent selects and uses the appropriate tools to reason about the situation.
4. **Act / Respond** — It returns a clear answer, or takes an authorized action on the business system.

## Getting Started

```bash
# Clone the repository
git clone https://github.com/nada1267/agentic-ai-operations-assistant.git
cd agentic-ai-operations-assistant

# Install dependencies
pip install -r requirements.txt

# Run with Docker
docker-compose up
```

## Tech Stack

- **Agentic AI** for multi-step task execution
- **RAG** for grounded, document/database-aware responses
- **LLMs** (tested against Gemini and others — see `gemini_test.py`, `llm_test.py`)
- **FastAPI-style backend** (`api.py`) and dedicated frontend

## License

_Add license information here._

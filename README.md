# SupportOps Copilot

SupportOps Copilot is an AI-powered customer support assistant built with Python, Flask, Retrieval-Augmented Generation (RAG), and Large Language Models.

The system automates customer support workflows by analyzing tickets, extracting customer information, consulting company knowledge bases, executing support tools, and drafting professional email responses.

---

## Features

- AI Ticket Classification
- Customer Information Extraction
- Order Lookup
- Refund Processing
- Human Approval Workflow
- Retrieval-Augmented Generation (RAG)
- Knowledge Base Integration
- Email Draft Generation
- Conversation Memory
- Support Agent Chat Interface
- Timeline Visualization
- Logging & Session Tracking

---

## System Architecture

```text
Customer Ticket
       ↓
Ticket Classification
       ↓
Information Extraction
       ↓
Execution Planning
       ↓
Tool Invocation
       ↓
RAG (if required)
       ↓
Email Generation
       ↓
Human Approval (optional)
       ↓
Final Response
```

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| HTML/CSS/JavaScript | Frontend |
| ChromaDB | Vector Database |
| Sentence Transformers | Embeddings |
| Google Gemini | LLM |
| RAG | Knowledge Retrieval |
| JSON | Mock Databases |

---

## Project Structure

```bash
support-ops-copilot/
│
├── app/
│   ├── services/
│   │   ├── agent.py
│   │   ├── ai_service.py
│   │   ├── rag_service.py
│   │   ├── retriever.py
│   │   ├── vector_store.py
│   │   └── ...
│
├── data/
│   ├── customers.json
│   ├── orders.json
│   └── sample_tickets.json
│
├── knowledge/
│   ├── refund_policy.txt
│   ├── shipping_policy.txt
│   ├── faq.txt
│   └── resolved_tickets.txt
│
├── logs/
│
├── ui/
│   ├── static/
│   └── templates/
│
├── web.py
└── README.md
```

---

## AI Capabilities

The system can:

- Classify support tickets
- Detect urgency levels
- Extract customer information
- Retrieve company policies using RAG
- Lookup order information
- Generate professional emails
- Maintain chat memory
- Request human approval for sensitive actions

---

## Knowledge Base

SupportOps Copilot uses Retrieval-Augmented Generation (RAG) to search company documents.

Current knowledge sources:

- FAQ
- Refund Policy
- Shipping Policy
- Resolved Support Tickets

Whenever the AI requires additional context, it retrieves the most relevant document chunks from ChromaDB before generating a response.

---

## Human-in-the-Loop Workflow

Certain actions require approval before execution:

- Refund Processing
- Order Cancellation
- Ticket Escalation
- Human Review

```text
AI Suggestion
      ↓
Approval Modal
      ↓
Approve / Reject
      ↓
Execute Action
```

---

## Example Ticket

```text
Hello,

My name is Ali Khan.

Order 78543 arrived with a cracked monitor.

I would like a replacement.

Regards.
```

### Output

```text
Category:
Shipping

Urgency:
Medium

Action:
Issue Refund

Knowledge Used:
refund_policy.txt

Generated Email:
Dear Ali Khan,

Thank you for contacting SupportOps...
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/support-ops-copilot.git
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

#### Mac/Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python web.py
```

Application will start at:

```text
http://127.0.0.1:5000
```

---

## Future Improvements

- Multi-Agent Architecture
- PostgreSQL Integration
- Real Email Sending
- Authentication & Roles
- Dashboard Analytics
- Ticket Assignment System
- LangGraph Integration
- Voice Support Assistant
- Docker Deployment
- Cloud Hosting

---

## Screenshots

Add screenshots of:

- Dashboard
- Ticket Analysis
- Knowledge Sources Used
- Human Approval Modal
- Support Agent Chat
- Logs Page

---

## Learning Outcomes

This project demonstrates:

- AI Agent Development
- RAG Implementation
- Prompt Engineering
- Human-in-the-Loop Systems
- Vector Databases
- LLM Integration
- Full Stack Development
- Workflow Automation

---

## Author

**Huzaifa Amir**

Final Year Project (FYP)

Computer Science

---

## License

This project is licensed under the MIT License.

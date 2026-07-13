class Prompts:

    @staticmethod
    def classify(ticket):

        return f"""
You are an expert customer support AI.

Classify this ticket.

Categories:
- Billing
- Technical
- Shipping
- Account
- General

Urgency:
- Low
- Medium
- High

Return ONLY JSON.

{{
    "category":"",
    "urgency":"",
    "reason":"",
    "confidence":0.9
}}

Ticket:

{ticket}
"""

    @staticmethod
    def extract(ticket):

        return f"""
Extract useful information.

Return ONLY JSON.

{{
    "customer_name":"",
    "order_id":"",
    "email":"",
    "issue":"",
    "confidence":0.9
}}

Ticket:

{ticket}
"""

    @staticmethod
    def draft(ticket):

        return f"""
Write a professional customer support email.

Return ONLY JSON.

{{
    "subject":"",
    "body":"",
    "confidence":0.9
}}

Ticket:

{ticket}
"""

    @staticmethod
    def rag(question, context):

        return f"""
You are a customer support assistant.

Answer ONLY using the provided knowledge.

If the answer cannot be found, say:

"I couldn't find that information in the knowledge base."

Knowledge:

{context}

Question:

{question}
"""

    @staticmethod
    def planner(ticket):

        return f"""
You are an intelligent AI Support Operations Agent.

Available tools:

- lookup_customer
- lookup_order_status
- issue_refund
- escalate_to_human
- close_ticket
- none

Knowledge Base:
Available through RAG.

Determine:

1. category
2. urgency
3. whether RAG is required
4. which tools should be executed (zero or more)
5. reason

Return ONLY JSON.

{{
    "category":"",
    "urgency":"",
    "use_rag":true,
    "tools":["none"],
    "reason":""
}}

Ticket:

{ticket}
"""
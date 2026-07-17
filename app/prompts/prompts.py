class Prompts:

    @staticmethod
    def classify(ticket):

        return f"""
You are an expert customer support AI.

Classify the customer ticket.

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

Return ONLY valid JSON.

{{
    "category":"",
    "urgency":"",
    "reason":"",
    "confidence":0.95
}}

Ticket:

{ticket}
"""

    @staticmethod
    def extract(ticket):

        return f"""
Extract useful information from the customer ticket.

Rules:

- If a value is missing, return an empty string.
- Never guess information.
- Return ONLY valid JSON.

{{
    "customer_name":"",
    "order_id":"",
    "email":"",
    "issue":"",
    "confidence":0.90
}}

Ticket:

{ticket}
"""

    @staticmethod
    def draft(ticket, tool_results="", context=""):

        return f"""
You are an experienced customer support representative.

Write a professional customer reply.

Use ONLY the information below.

=================================================
CUSTOMER TICKET
=================================================

{ticket}

=================================================
TOOL RESULTS
=================================================

{tool_results}

=================================================
KNOWLEDGE BASE
=================================================

{context}

Instructions:

• Never invent facts.
• Never mention AI, tools or internal systems.
• Mention order status if available.
• If refund succeeded, clearly tell the customer the refund has already been processed.
• If refund failed, explain the request requires manual review.
• Use the Knowledge Base only if relevant.
• Be polite and concise.
• Keep the email under 150 words.

Return ONLY valid JSON.

{{
    "subject":"",
    "body":"",
    "confidence":0.90
}}
"""

    @staticmethod
    def rag(question, context):

        return f"""
You are a customer support assistant.

Answer ONLY using the knowledge below.

If the answer is not explicitly present, respond exactly:

I couldn't find that information in the knowledge base.

Knowledge:

{context}

Question:

{question}
"""

    @staticmethod
    def planner(ticket):

        return f"""
You are an AI Support Operations Planner.

Your ONLY job is to decide:

1. Ticket category
2. Urgency
3. Whether RAG is required
4. Which tools should run
5. Reason

Available tools:

- lookup_customer
- lookup_order_status
- issue_refund
- escalate_to_human
- close_ticket
- none

Rules:

1. Use RAG ONLY for:
   - refund policy
   - shipping policy
   - FAQs
   - company documentation
   - account policy
   - product information

2. If tools can solve the problem,
   set use_rag to false.

3. Use the minimum number of tools.

4. Only use escalate_to_human when no self-service tool can solve the issue.
    Do not escalate routine technical questions if they can be handled with
    lookup tools or a normal reply.

Examples:

Refund request
→ lookup_order_status
→ issue_refund

Order status
→ lookup_order_status

Customer details
→ lookup_customer

Policy question
→ use_rag = true
→ tools = ["none"]

Technical issue that cannot be resolved with tools
→ escalate_to_human

Greeting
→ tools = ["none"]

Return ONLY valid JSON.

{{
    "category":"",
    "urgency":"",
    "use_rag":false,
    "tools":["none"],
    "reason":""
}}

Ticket:

{ticket}
"""
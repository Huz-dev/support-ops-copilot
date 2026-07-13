class Prompts:

    @staticmethod
    def classify(ticket: str):

        return f"""
You are an expert support engineer.

Classify the ticket.

Categories:

Billing
Technical
Shipping
Account
General

Urgency

Low
Medium
High

Return ONLY JSON.

{{
"category":"",
"urgency":"",
"reason":"",
"confidence":0
}}

Ticket

{ticket}
"""

    @staticmethod
    def extract(ticket: str):

        return f"""
Extract useful customer information.

Return ONLY JSON.

{{
"customer_name":"",
"email":"",
"order_id":"",
"issue":"",
"confidence":0
}}

Ticket

{ticket}
"""

    @staticmethod
    def draft(ticket: str):

        return f"""
Write a professional customer support email.

Return ONLY JSON.

{{
"subject":"",
"body":"",
"confidence":0
}}

Ticket

{ticket}
"""

    @staticmethod
    def rag(question, context):

        return f"""
Answer ONLY from the supplied context.

If the answer is missing say

"I couldn't find that information."

Context

{context}

Question

{question}
"""
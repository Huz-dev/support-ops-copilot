from app.services.ai_service import AIService
from app.services.rag_service import RAGService
from app.services.tool_service import ToolService
from app.services.memory import ConversationMemory
from app.services.logger_service import LoggerService

class SupportAgent:
    def __init__(self):
        self.ai = AIService()
        self.rag = RAGService()
        self.tools = ToolService()
        self.memory = ConversationMemory()
        self.logger = LoggerService()
        self.rag = RAGService()
        self.rag.ingest()
        if self.rag.vector_store.collection.count() == 0:
            self.rag.ingest()

    def execute_tools(
        self,
        tools,
        extraction,
        ticket,
    ):
        tool_results = []

        for tool in tools:
            if tool == "none":
                continue

            if tool == "lookup_customer":
                result = self.tools.execute(
                    tool,
                    order_id=extraction.get("order_id"),
                )

            elif tool == "lookup_order_status":
                result = self.tools.execute(
                    tool,
                    order_id=extraction.get("order_id"),
                )

            elif tool == "issue_refund":
                result = self.tools.execute(
                    tool,
                    order_id=extraction.get("order_id"),
                )

            elif tool == "escalate_to_human":
                result = self.tools.execute(
                    tool,
                    ticket=ticket,
                )

            elif tool == "close_ticket":
                result = self.tools.execute(
                    tool,
                    ticket=ticket,
                )

            else:
                result = {"error": f"Unknown tool {tool}"}

            tool_results.append(
                {
                    "tool": tool,
                    "result": result,
                }
            )

        return tool_results


    def process_ticket(self, ticket):
        rag = {
             "retrieved": []
            }
        self.memory.add("user", ticket)
        plan = self.ai.plan(ticket)
        print(plan)

        classification = self.ai.classify(ticket)

        extraction = self.ai.extract(ticket)
        if (
            extraction.get("order_id")
            and "lookup_order_status" in plan["tools"]
        ):

            order = self.tools.find_order(
            extraction["order_id"]
            )
            if not order:
                return {
                    "approval_required": True,
                    "approval_tool": "human_review",
                    "approval_reason":
                        "Order does not exist. Human review required.",
                    "ticket": ticket,
                    "plan": plan,
                    "classification": classification,
                    "extraction": extraction,
                }

        # Human review for low confidence
        if (
            classification["confidence"] < 0.80
            or extraction["confidence"] < 0.80
        ):
            return {
                "approval_required": True,
                "approval_tool": "human_review",
                "approval_reason":
                    "AI confidence below 80%. Human review required.",
                "ticket": ticket,
                "plan": plan,
                "classification": classification,
                "extraction": extraction,
            }

        # Check if approval is needed
        for tool in plan["tools"]:
            if tool in [
                "issue_refund",
                "cancel_order",
            ]:
                return {
                    "approval_required": True,
                    "approval_tool": tool,
                    "approval_reason": self.tools.get_approval_reason(
                        tool,
                        extraction,
                        ticket,
                    ),
                    "ticket": ticket,
                    "plan": plan,
                    "classification": classification,
                    "extraction": extraction,
                }
        # Execute remaining tools

        tool_results = self.execute_tools(
            plan["tools"],
            extraction,
            ticket,
        )

        context = ""

        if plan.get("use_rag"):
            rag = self.rag.ask(ticket)
            print("\nRAG RESULTS:")
            print(rag)
            print("\n")
            context = "\n\n".join([doc["document"] for doc in rag["retrieved"]])

        tool_summary = ""

        for item in tool_results:
            if item["tool"] == "lookup_customer":
                customer = item["result"]

                tool_summary += f"""
Customer Information:
- Name: {customer.get("customer", "Unknown")}
- Status: {customer.get("status", "Unknown")}
- Previous Orders: {customer.get("orders", "Unknown")}

"""

            elif item["tool"] == "lookup_order_status":
                order = item["result"]

                tool_summary += f"""
Order Status:
- Order ID: {order.get("order_id")}
- Status: {order.get("status")}
- Estimated Delivery: {order.get("estimated_delivery")}

"""

            elif item["tool"] == "issue_refund":
                refund = item["result"]

                if refund.get("success"):
                    tool_summary += f"""
Refund Status:
- SUCCESS
- Refund ID: {refund.get("refund_id")}

"""

                else:
                    tool_summary += f"""
Refund Status:
- FAILED
- Reason: {refund.get("message")}

"""

            elif item["tool"] == "escalate_to_human":
                tool_summary += """
Escalation:
- Ticket has been escalated to a human support representative.

"""

            elif item["tool"] == "close_ticket":
                tool_summary += """
Ticket Status:
- Ticket successfully closed.

"""

        email = self.ai.draft(
            ticket=ticket,
            tool_results=tool_summary,
            context=context,
        )

        self.memory.add(
            "assistant",
            f"Subject: {email['subject']}\n\n{email['body']}",
        )

        self.logger.save(
        ticket,
        plan,
        classification,
        extraction,
        tool_results,
        email,
        )

        return {
            "plan": plan,
            "classification": classification,
            "extraction": extraction,
            "tool_results": tool_results,
            "context": context,
            "email": email,
            "memory": self.memory.history(),
            "retrieved_docs": (
             rag["retrieved"]
             if plan.get("use_rag")
                else []
                ),
        }

    def complete_after_approval(
        self,
        ticket,
        plan,
        classification,
        extraction,
    ):

        tool_results = self.execute_tools(
            plan["tools"],
            extraction,
            ticket,
        )

        context = ""

        if plan.get("use_rag"):
            rag = self.rag.ask(ticket)

            context = "\n\n".join(
                doc["document"]
                for doc in rag["retrieved"]
            )

        tool_summary = ""

        for item in tool_results:
            if item["tool"] == "lookup_customer":
                customer = item["result"]

                tool_summary += f"""
Customer Information:
- Name: {customer.get("customer", "Unknown")}
- Status: {customer.get("status", "Unknown")}
- Previous Orders: {customer.get("orders", "Unknown")}

"""

            elif item["tool"] == "lookup_order_status":
                order = item["result"]

                tool_summary += f"""
Order Status:
- Order ID: {order.get("order_id")}
- Status: {order.get("status")}
- Estimated Delivery: {order.get("estimated_delivery")}

"""

            elif item["tool"] == "issue_refund":
                refund = item["result"]

                if refund.get("success"):
                    tool_summary += f"""
Refund Status:
- SUCCESS
- Refund ID: {refund.get("refund_id")}

"""

                else:
                    tool_summary += f"""
Refund Status:
- FAILED
- Reason: {refund.get("message")}

"""

        email = self.ai.draft(
            ticket=ticket,
            tool_results=tool_summary,
            context=context,
        )

        self.memory.add(
            "assistant",
            f"Subject: {email['subject']}\n\n{email['body']}",
        )

        self.logger.save(
        ticket,
        plan,
        classification,
        extraction,
        tool_results,
        email,
        )

        return {
            "plan": plan,
            "classification": classification,
            "extraction": extraction,
            "tool_results": tool_results,
            "context": context,
            "email": email,
            "memory": self.memory.history(),
            "retrieved_docs": (
            rag["retrieved"]
                if plan.get("use_rag")
                else []
                ),
        }


    

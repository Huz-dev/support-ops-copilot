from app.services.ai_service import AIService
from app.services.rag_service import RAGService
from app.services.tool_service import ToolService


class SupportAgent:

    def __init__(self):

        self.ai = AIService()
        self.rag = RAGService()
        self.tools = ToolService()

    def process_ticket(self, ticket):

        plan = self.ai.plan(ticket)

        classification = self.ai.classify(ticket)

        extraction = self.ai.extract(ticket)

        tool_results = []

        for tool in plan["tools"]:

            if tool == "none":
                continue

            if tool in [
                "lookup_customer",
                "lookup_order_status",
                "issue_refund",
            ]:

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

                result = {
                    "error": f"Unknown tool {tool}"
                }

            tool_results.append(
                {
                    "tool": tool,
                    "result": result,
                }
            )

        context = ""

        if plan.get("use_rag"):

            rag = self.rag.ask(ticket)

            context = rag["context"]

        email = self.ai.draft(ticket)

        return {
            "plan": plan,
            "classification": classification,
            "extraction": extraction,
            "tool_results": tool_results,
            "context": context,
            "email": email,
        }
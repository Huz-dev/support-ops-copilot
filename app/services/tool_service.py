from pathlib import Path
from datetime import datetime
import json
from pathlib import Path
from app.tools.customer_tools import CustomerTools
from app.tools.workflow_tools import WorkflowTools


class ToolService:

    def __init__(self):

        self.log_file = Path("logs/tool_calls.log")
        self.data_dir = Path("data")
        self.log_file.parent.mkdir(
            exist_ok=True
        )

        self.log_file.touch(
            exist_ok=True
        )

    def log(
        self,
        tool,
        status,
        details,
    ):

        with open(
            self.log_file,
            "a",
        ) as f:

            f.write(
                f"""
==================================================
{datetime.now()}

Tool:
{tool}

Status:
{status}

Details:
{details}
==================================================

"""
            )

    def approval(
    self,
    tool,
    reason,
):
        return True

    def execute(
        self,
        tool,
        **kwargs,
    ):

        if tool == "lookup_customer":

            result = CustomerTools.lookup_customer(
                kwargs["order_id"]
            )

            self.log(
                tool,
                "Executed",
                result,
            )

            return result

        if tool == "lookup_order_status":

            result = CustomerTools.lookup_order_status(
                kwargs["order_id"]
            )

            self.log(
                tool,
                "Executed",
                result,
            )

            return result

        if tool == "issue_refund":

            if not self.approval(
                tool,
                "Duplicate payment detected",
            ):

                self.log(
                    tool,
                    "Rejected",
                    kwargs,
                )

                return {
                    "success": False,
                    "message": "Refund cancelled by human."
                }

            result = WorkflowTools.issue_refund(
                kwargs["order_id"]
            )

            self.log(
                tool,
                "Approved",
                result,
            )

            return result

        if tool == "escalate_to_human":

            if not self.approval(
                tool,
                "Low confidence response",
            ):

                self.log(
                    tool,
                    "Rejected",
                    kwargs,
                )

                return {
                    "success": False,
                    "message": "Escalation cancelled."
                }

            result = WorkflowTools.escalate_to_human(
                kwargs["ticket"]
            )

            self.log(
                tool,
                "Approved",
                result,
            )

            return result

        if tool == "close_ticket":

            result = WorkflowTools.close_ticket(
                kwargs["ticket"]
            )

            self.log(
                tool,
                "Executed",
                result,
            )

            return result

        raise ValueError(
            f"Unknown tool: {tool}"
        )

    def get_approval_reason(self, tool, extraction=None, ticket=None):

        order_id = None
        if extraction and isinstance(extraction, dict):
            order_id = extraction.get("order_id")

        reasons = {
            "issue_refund": f"Refund requested for Order {order_id}.",
            "cancel_order": f"Cancellation requested for Order {order_id}.",
            "escalate_to_human": "Customer requested escalation.",
            "human_review": "AI confidence below 80%."
        }

        return reasons.get(tool, "Human approval required.")

    def load_orders(self):

        with open(
            self.data_dir / "orders.json",
            "r"
        ) as f:

            return json.load(f)
        

    def find_order(self, order_id):

        orders = self.load_orders()

        for order in orders:

            if order["order_id"] == order_id:

                return order

        return None
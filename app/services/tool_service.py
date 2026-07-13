from pathlib import Path
from datetime import datetime

from app.tools.customer_tools import CustomerTools
from app.tools.workflow_tools import WorkflowTools


class ToolService:

    def __init__(self):

        self.log_file = Path("logs/tool_calls.log")

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

        print("\n" + "=" * 60)
        print(" HUMAN APPROVAL REQUIRED ")
        print("=" * 60)

        print(f"\nTool   : {tool}")
        print(f"Reason : {reason}")

        choice = input(
            "\nApprove? (y/n): "
        ).lower()

        return choice == "y"

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
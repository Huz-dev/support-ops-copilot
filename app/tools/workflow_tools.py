import json
from pathlib import Path
from datetime import datetime


class WorkflowTools:

    @staticmethod
    def issue_refund(order_id):

        with open("data/orders.json") as f:
            orders = json.load(f)

        order = next(
            (
                o for o in orders
                if o["order_id"] == order_id
            ),
            None
        )

        if not order:

            return {
                "success": False,
                "message": "Order not found."
            }

        if not order["refund_eligible"]:

            return {
                "success": False,
                "message": "Order is not eligible for refund."
            }

        return {
            "success": True,
            "refund_id": f"RF-{order_id}",
            "processed_at": str(datetime.now())
        }

    @staticmethod
    def escalate_to_human(ticket):

        return {
            "success": True,
            "assigned_to": "Senior Support",
            "ticket": ticket
        }

    @staticmethod
    def close_ticket(ticket):

        return {
            "success": True,
            "ticket": ticket
        }
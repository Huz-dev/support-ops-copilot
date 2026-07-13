from datetime import datetime


class WorkflowTools:

    @staticmethod
    def issue_refund(order_id):

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
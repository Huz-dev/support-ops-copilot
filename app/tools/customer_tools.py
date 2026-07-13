from datetime import datetime


class CustomerTools:

    customers = {
        "92381": {
            "customer": "John Smith",
            "status": "Premium",
            "orders": 12
        },
        "48211": {
            "customer": "Sarah Lee",
            "status": "Standard",
            "orders": 3
        }
    }

    @classmethod
    def lookup_customer(cls, order_id):

        return cls.customers.get(
            order_id,
            {
                "customer": "Unknown",
                "status": "Unknown",
                "orders": 0
            }
        )

    @classmethod
    def lookup_order_status(cls, order_id):

        return {
            "order_id": order_id,
            "status": "Shipped",
            "estimated_delivery": "2 business days",
            "checked_at": str(datetime.now())
        }
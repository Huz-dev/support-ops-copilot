import json
from pathlib import Path
from datetime import datetime


class CustomerTools:

    @classmethod
    def load_orders(cls):

        with open(
            Path("data/orders.json"),
            "r"
        ) as f:

            return json.load(f)

    @classmethod
    def find_order(cls, order_id):

        orders = cls.load_orders()

        for order in orders:

            if order["order_id"] == order_id:

                return order

        return None

    @classmethod
    def lookup_customer(cls, order_id):

        order = cls.find_order(order_id)

        if not order:

            return {
                "customer": "Unknown",
                "status": "Unknown",
                "orders": 0
            }

        return {
            "customer": order["customer"],
            "status": "Found",
            "orders": "See customers.json"
        }

    @classmethod
    def lookup_order_status(cls, order_id):

        order = cls.find_order(order_id)

        if not order:

            return {
                "error": "Order not found"
            }

        return {
            "order_id": order["order_id"],
            "status": order["status"],
            "estimated_delivery":
                order["estimated_delivery"],
            "checked_at": str(datetime.now())
        }
import json
from pathlib import Path


class CompanyContext:

    @staticmethod
    def build():

        context = ""

        # Customers

        with open("data/customers.json") as f:

            context += "\nCUSTOMERS:\n"

            context += json.dumps(
                json.load(f),
                indent=2
            )

        # Orders

        with open("data/orders.json") as f:

            context += "\nORDERS:\n"

            context += json.dumps(
                json.load(f),
                indent=2
            )

        # Knowledge Base

        knowledge = Path(
            "app/knowledge"
        )

        for file in knowledge.glob(
            "*.txt"
        ):

            context += f"\n{file.name}\n"

            context += file.read_text()

        return context
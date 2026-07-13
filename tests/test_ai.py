from app.services.ai_service import AIService
from app.utils.validator import Validator

ticket = """
Hello,

I was charged twice for order #92381.

Please refund one payment.

Regards,

John Smith
"""

ai = AIService()

classification = Validator.classification(
    ai.classify(ticket)
)

extraction = Validator.extraction(
    ai.extract(ticket)
)

email = Validator.email(
    ai.draft(ticket)
)

print("=" * 80)
print("SUPPORT OPS COPILOT")
print("=" * 80)

print("\nCLASSIFICATION")
print(classification.model_dump())

print("\nEXTRACTION")
print(extraction.model_dump())

print("\nEMAIL")
print(email.model_dump())
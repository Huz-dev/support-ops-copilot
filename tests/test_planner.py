from pprint import pprint

from app.services.ai_service import AIService

ticket = """
Hello,

I was charged twice for order 92381.

Also I still haven't received the package.

Can you refund me and tell me where it is?

Thanks,
John
"""

ai = AIService()

result = ai.plan(ticket)

print("=" * 70)
print("AI PLAN")
print("=" * 70)

pprint(result)
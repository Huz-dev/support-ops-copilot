from pprint import pprint

from app.services.agent import SupportAgent


ticket = """
Hello,

I was charged twice for order 92381.

Please refund me.

Thanks,

John Smith
"""


agent = SupportAgent()

result = agent.process_ticket(ticket)


print("=" * 60)
print("PLAN")
print("=" * 60)
pprint(result["plan"])

print()

print("=" * 60)
print("CLASSIFICATION")
print("=" * 60)
pprint(result["classification"])

print()

print("=" * 60)
print("EXTRACTION")
print("=" * 60)
pprint(result["extraction"])

print()

print("=" * 60)
print("TOOL RESULTS")
print("=" * 60)
pprint(result["tool_results"])

print()

if result["context"]:
    print("=" * 60)
    print("RAG CONTEXT")
    print("=" * 60)
    print(result["context"])
    print()

print("=" * 60)
print("EMAIL")
print("=" * 60)
pprint(result["email"])

print()
print("=" * 60)
print("MEMORY")
print("=" * 60)

for m in result["memory"]:
    print(f'{m["role"]}:')
    print(m["content"])
    print()
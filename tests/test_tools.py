from app.services.tool_service import ToolService

tool = ToolService()

print("=" * 60)
print("LOOKUP CUSTOMER")
print("=" * 60)

print(
    tool.execute(
        "lookup_customer",
        order_id="92381",
    )
)

print("\n")

print("=" * 60)
print("ORDER STATUS")
print("=" * 60)

print(
    tool.execute(
        "lookup_order_status",
        order_id="92381",
    )
)

print("\n")

print("=" * 60)
print("REFUND")
print("=" * 60)

print(
    tool.execute(
        "issue_refund",
        order_id="92381",
    )
)
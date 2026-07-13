from app.services.rag_service import RAGService

rag = RAGService()

print("=" * 70)
print("SUPPORT OPS COPILOT")
print("=" * 70)

print("\nBuilding Knowledge Base...")
rag.ingest()
print("Knowledge Base Ready!\n")

while True:

    question = input("Ask a question (or type exit): ")

    if question.lower() == "exit":
        break

    result = rag.ask(question)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(result["answer"])

    print("\nSources Used")

    used = set()

    for doc in result["retrieved"]:

        if doc["source"] not in used:
            print(f"• {doc['source']}")
            used.add(doc["source"])

    print("\n")
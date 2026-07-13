from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk_documents(self, documents):

        chunks = []

        for document in documents:

            pieces = self.splitter.split_text(
                document["text"]
            )

            for index, piece in enumerate(pieces):

                chunks.append(
                    {
                        "id": f"{document['source']}_{index}",
                        "source": document["source"],
                        "chunk_index": index,
                        "text": piece,
                    }
                )

        return chunks
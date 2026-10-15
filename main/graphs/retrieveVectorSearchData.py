from langchain_core.tools import tool

from supplyChainBot.main.supplyChainRagCall import supplyChainRagCall

@tool
def getVectorStoreData(query: str) -> str:
    """Function used to retrieve raw excerpts with source metadata"""
    ragResponse = supplyChainRagCall(query)
    formatted_chunks = []

    if not ragResponse:
        return "There is no relevant information reagarding your query in the knowledge base."

    else:

        for i,doc in enumerate(ragResponse, start=1):
            
            metadata = doc.metadata
            doc_id = metadata.get("doc_id", "N/A")
            status = metadata.get("status", "N/A")
            version = metadata.get("version", "N/A")
            source_file = metadata.get("source_file", "N/A")

            chunk_block = (
                f"======Source Chunk {i} ========\n"
                f"Document ID: {doc_id} | Document Status: {status} | "
                f"version: {version} | Source File: {source_file} \n"
                f"Chunk Content: {doc.page_content.strip()}"

            )

            formatted_chunks.append(chunk_block)

        return "\n\n".join(formatted_chunks)

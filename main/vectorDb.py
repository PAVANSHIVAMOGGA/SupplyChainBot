import logging

import chromadb
from langchain_chroma import Chroma


class VectorDb:

    def __init__(self, collection_name, persistant_directory, embeddings):
        self.vectorDb = Chroma(collection_name=collection_name,
                               embedding_function=embeddings,
                               persist_directory=persistant_directory)


    def addToVectorDb(self, ids, metadata, content):

        logging.info("Storing the Chunks to Vector DB: START")
        self.vectorDb.add_texts(
            metadatas=metadata,
            texts=content,
            ids=ids
        )
        logging.info("Storing the Chunks to Vector DB: END")

    def queryToVectorDb(self,query,n_results):

        logging.info("Querying the Chunks to Vector DB: START")
        result = self.vectorDb.similarity_search(
            query=query,
            k=n_results
        )
        logging.info("Querying the Chunks to Vector DB: END")

        #print(result[:300])
        return result
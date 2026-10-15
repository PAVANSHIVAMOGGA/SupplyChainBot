

import logging

from supplyChainBot.main import llmConnect
from supplyChainBot.main.chunking import buildChunkId, loadAndChunkFile
from supplyChainBot.main.config import COLLECTION_NAME, DIR_PATH, EMBEDDINGS, PERSISTANT_DIRECTORY
from supplyChainBot.main.vectorDb import VectorDb

from cachetools.func import ttl_cache

@ttl_cache(maxsize=256, ttl=24 * 12 * 12)
def supplyChainRagCall(query):

    logging.info("Getting the files for chunking")
    markdown_files = sorted(DIR_PATH.glob("*.md"))

    #Prepare the chunks to load for vector DB
    doc_contents, doc_metadata, doc_ids = [], [], []
    for filepath in markdown_files:
        chunks = loadAndChunkFile(filepath= filepath)

        #Build the ids for the vector DB
        for i, (content, metadata) in enumerate(chunks):
            chunk_id = buildChunkId(doc_metadata= metadata, chunk_index=i)
            doc_contents.append(content)
            doc_metadata.append(metadata)
            doc_ids.append(chunk_id)

    logging.info("Chunking done with chunk size: {len(doc_contents)}")

    vectorDb  = VectorDb(collection_name=COLLECTION_NAME,
                         persistant_directory=PERSISTANT_DIRECTORY,
                         embeddings=EMBEDDINGS)

    vectorDb.addToVectorDb(ids=doc_ids,
                           metadata=doc_metadata,
                           content=doc_contents)

    

    ragQueryResponse = vectorDb.queryToVectorDb(query=query,
                             n_results=3)

    

    return ragQueryResponse


import logging
import datetime
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

import frontmatter

from supplyChainBot.main.config import CHUNK_OVERLAP, CHUNK_SIZE, HEADERS_TO_SPLIT_ON


########################
#Chroma DB only accepts str, int, float, bool, SparseVector, list, or None
#Convert the other data types like Date to ISO string format to load into vector DB
########################
def fixLoadFormatIssue(metadata: dict):

    cleanedData = {}

    for key, value in metadata.items():
        
        if value is None or isinstance(value, (int, str, float, bool)):
            cleanedData[key] = value
        elif isinstance(value, (list, tuple)):
            cleanedData[key] = ",".join(str(data) for data in value)
        elif isinstance(value, (datetime.date, datetime.datetime)):
            cleanedData[key] = value.isoformat()
        else:
            cleanedData[key] = str(value)
    return cleanedData

def loadAndChunkFile(filepath: Path):

    logging.info("Chunking the files : START")

    post = frontmatter.load(filepath)
    document_metadata = fixLoadFormatIssue(dict(post.metadata)) #YAML fomatter dictionary
    document_metadata["source_file"] = filepath.name

    #Split the file according to headers and extract the contents
    header_splitter = MarkdownHeaderTextSplitter(
                        headers_to_split_on=HEADERS_TO_SPLIT_ON
                        )
    header_section = header_splitter.split_text(post.content)

    subject_splitter = RecursiveCharacterTextSplitter(
                            chunk_size = CHUNK_SIZE,
                            chunk_overlap = CHUNK_OVERLAP,
                            separators=["/n/n", "/n"]
                        )

    chunks = []

    for section in header_section:

        #Extract content from section
        section_content = section.page_content.strip()

        #Validate if the contents are available in this section
        if not section_content:
            continue

        section_metadata = {**document_metadata, **section.metadata}

        #Validate the size of section content 
        if (len(section_content) <= CHUNK_SIZE):
            chunks.append((section_content, section_metadata))
        else:
            sub_chunks = subject_splitter.split_text(section_content)
            for sub_content in sub_chunks:
                chunks.append((sub_content, section_metadata))

    logging.info("Chunking the files : END")

    return chunks


def buildChunkId(doc_metadata: dict, chunk_index: int) -> str:

    logging.info("Generating the IDs for the chunks : START")

    doc_id = doc_metadata.get("doc_id", doc_metadata.get("source_file", "unknown"))
    version = doc_metadata.get("version","0")
    h2 = doc_metadata.get("h2", doc_metadata.get("h1", "secction"))
    h2_slug = str(h2).lower().replace(" ", "_")[:40]

    logging.info("Generating the IDs for the chunks : END")

    return f"{doc_id}::{version}::{h2_slug}::{chunk_index}"
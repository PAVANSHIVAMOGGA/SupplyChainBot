# --------------------------------------------------------------------------
# Define all the constants, env vars
# --------------------------------------------------------------------------
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import logging

logging.basicConfig(level="INFO")


load_dotenv()

import os

SCRIPT_DIR = Path(__file__).parent 

# The parent directory of your script's folder (e.g., .../supplyChainBot)
PARENT_DIR = SCRIPT_DIR.parent

# The path to the documents directory
DIR_PATH = PARENT_DIR / "documents"
#Desine source path and directory path
#doc_path = "../documents/EncyclopediaofMedicine.pdf"
PERSISTANT_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "SupplyChainDocs"

#Define Chunk size and overlap details
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

#Define embedding model config details
EMBEDDINGS = OpenAIEmbeddings(api_key=os.getenv("OPEN_AI_API_KEY"),
                                                model="text-embedding-3-small")
llm = ChatOpenAI(api_key=os.getenv("OPEN_AI_API_KEY"), 
                 model="gpt-4.1-mini")

# Split on H1/H2 headers — the documents are structured in this way
HEADERS_TO_SPLIT_ON = [
    ("#", "h1"),
    ("##", "h2"),
]
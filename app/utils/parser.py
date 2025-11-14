# In app/utils/parser.py

from llama_parse import LlamaParse
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from docx import Document
import os
from dotenv import load_dotenv

load_dotenv()

LLAMA_PARSE_API_KEY = os.environ.get("LLAMA_PARSE_API_KEY")

from llama_cloud_services import LlamaParse

parser = LlamaParse(
    api_key=LLAMA_PARSE_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    num_workers=4,       # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="en",       # optionally define a language, default=en
)

class Parser:
    def __init__(self, filename):
        self.file_extension = filename.split('.')[-1].lower()

    # chunking the raw text into smaller parts for vectorestore ingestion
    def chunk_text(self, text: str):

        text_splitter = SentenceSplitter(
            chunk_size=1000,
            chunk_overlap=20,
        )
        chunks = text_splitter.split_text(text)
        print(f"Successfully created {len(chunks)} chunks.")
        return chunks

    async def text(self, file_path: str):
        text_content = ""
        try:
            documents = parser.parse(file_path)
            text_content = documents.get_markdown_documents()
            print(text_content[0].text)
            # print(f"Parsed {len(text_content)} documents from PDF.")                
            return text_content
            
        except Exception as e:
            # Re-raise the exception to be caught by the FastAPI endpoint
            raise e
        


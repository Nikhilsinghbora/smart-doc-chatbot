# In app/utils/parser.py

from llama_parse import LlamaParse
from docx import Document
import os
from dotenv import load_dotenv

load_dotenv()

LLAMA_PARSE_API_KEY = os.environ.get("LLAMA_PARSE_API_KEY")

class Parser:
    def __init__(self, filename):
        self.file_extension = filename.split('.')[-1].lower()

    def chunk_text(self, text: str):
        text_splitter = SentenceSplitter(
            chunk_size=1000,
            chunk_overlap=20,
        )
        chunks = text_splitter.split_text(text)
        print(f"Successfully created {len(chunks)} chunks.")
        return chunks
    
    # ✅ FIX: The method now accepts a file_path string
    async def text(self, file_path: str):
        text_content = ""
        try:
            if self.file_extension == 'pdf':
                if not LLAMA_PARSE_API_KEY:
                    raise ValueError("LLAMA_PARSE_API_KEY environment variable is not set.")
                
                parser = LlamaParse(
                    api_key=LLAMA_PARSE_API_KEY,
                    result_type="markdown",
                    verbose=True
                )
                
                # ✅ FIX: Use the full file_path for parsing
                documents = await parser.aload_data(file_path)
                text_content = documents[0].text if documents else ""

            elif self.file_extension == 'docx':
                # ✅ FIX: python-docx opens the file directly from its path
                doc = Document(file_path)
                text_content = "\n".join([p.text for p in doc.paragraphs])

            elif self.file_extension == "txt":
                # ✅ FIX: Read the text file from its path
                with open(file_path, "r", encoding="utf-8") as f:
                    text_content = f.read()
            else:
                raise ValueError(f"Unsupported file extension: {self.file_extension}")
                
            return text_content
            
        except Exception as e:
            # Re-raise the exception to be caught by the FastAPI endpoint
            raise e
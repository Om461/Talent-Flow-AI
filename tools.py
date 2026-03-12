import os
import PyPDF2
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class ReadPDFDirectoryInput(BaseModel):
    directory_path: str = Field(..., description="The exact path to the directory containing PDF resumes.")

class ReadPDFDirectoryTool(BaseTool):
    name: str = "Read PDF Directory"
    description: str = "Reads all PDF resumes from a given directory path and extracts their text. Useful for iterating through a folder of resumes."
    args_schema: type[BaseModel] = ReadPDFDirectoryInput
    
    def _run(self, directory_path: str) -> str:
        if not os.path.exists(directory_path):
            return f"Error: Directory '{directory_path}' not found."
            
        texts = []
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                try:
                    with open(file_path, 'rb') as f:
                        pdf = PyPDF2.PdfReader(f)
                        text = "".join(page.extract_text() or "" for page in pdf.pages)
                        texts.append(f"--- Resume File: {filename} ---\n{text}\n")
                except Exception as e:
                    texts.append(f"Error reading {filename}: {str(e)}")
                    
        if not texts:
            return "No PDF files found in the directory."
        
        return "\n".join(texts)

# In your FastAPI router file (e.g., routers/upload.py)

from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.utils.parser import Parser # Make sure this import path is correct

router = APIRouter()

# Define the directory where files will be saved
upload_dir = os.path.join(os.getcwd(), "uploads")
os.makedirs(upload_dir, exist_ok=True)


@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    allowed_content_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="File type not supported. Only PDF and DOCX files are allowed.",
        )

    # This creates the full, correct path to the saved file
    file_path = os.path.join(upload_dir, file.filename)
    print(file_path)
    
    try:
        # Save the uploaded file to the server
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Initialize the parser
        parser = Parser(file.filename)
        
        # ✅ FIX: Pass the full file_path to the text method
        parsed_text = await parser.text(file_path)
        
        # Optionally remove the file after parsing
        os.remove(file_path)

        return {
            "filename": file.filename, 
            "content": parsed_text,
            "message": "File parsed successfully."
        }

    except Exception as e:
        # If the file exists, clean it up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
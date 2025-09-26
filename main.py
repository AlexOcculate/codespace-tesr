from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from typing import List
import uuid
from datetime import datetime

app = FastAPI(title="File Upload Server", version="1.0.0")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the server.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    # Generate a unique filename to avoid conflicts
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save the uploaded file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "saved_as": unique_filename,
            "size": len(content)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

@app.get("/list")
async def list_files():
    """
    List all uploaded files.
    """
    try:
        files = []
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return {
            "files": files,
            "total_count": len(files)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list files: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint with basic information.
    """
    return {
        "message": "File Upload Server",
        "endpoints": {
            "upload": "POST /upload - Upload a file",
            "list": "GET /list - List all uploaded files"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
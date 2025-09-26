# codespace-tesr

A FastAPI web server for file uploads with two main endpoints:
- `POST /upload` - Upload multipart files
- `GET /list` - List all uploaded files

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`.

## API Endpoints

### POST /upload
Upload a file using multipart/form-data.

**Example:**
```bash
curl -X POST -F "file=@path/to/your/file.txt" http://localhost:8000/upload
```

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "file.txt",
  "saved_as": "uuid-filename.txt",
  "size": 1024
}
```

### GET /list
List all uploaded files with metadata.

**Example:**
```bash
curl http://localhost:8000/list
```

**Response:**
```json
{
  "files": [
    {
      "filename": "uuid-filename.txt",
      "size": 1024,
      "uploaded_at": "2025-09-26T12:37:47.782471"
    }
  ],
  "total_count": 1
}
```

### GET /
Get server information and available endpoints.

## Features

- Secure file uploads with UUID-based filenames to prevent conflicts
- File metadata tracking (size, upload timestamp)
- Error handling for invalid requests
- Files stored in `uploads/` directory (automatically created)
- Support for any file type
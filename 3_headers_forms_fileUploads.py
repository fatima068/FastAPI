from fastapi import FastAPI, Header, Form, File, UploadFile, HTTPException
# uv add python-multipart - required for form data and file uploads
app = FastAPI()


# 1. HEADERS: additional information sent along with an HTTP request outside the request body
app.get("/documents")
def get_documents(api_key: str = Header(...)): #Header() tells FastAPI to look for the api key value in the http headers and ... means the feld is required 
    # FastAPI automatically converts api_key to the header name api-key & reads the API key from the request header.
    if api_key != "secret123":
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return {"documents": ["Python", "FastAPI"]}


# 2. FORM: another way of sending data in an HTTP request body
#JSON sends structured objects, form data sends key-value pairs.
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    # Form() tells FastAPI to receive these values from data, ... means values are required 
    #cannot combine form() fields and json/pydantic body in the same endpoint 
    return {
        "message": "Login successful",
        "username": username
    }


# 3. FILE UPLOAD: UploadFile() and File() to receive uploaded files.
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename     # Original name of the uploaded file
    content_type = file.content_type    # Type of file (e.g. application/pdf)
    contents = await file.read()    # Read the actual file contents as bytes
    #await becos file read is i/o bound op 

    return {
        "filename": filename,
        "content_type": content_type,
        "size": len(contents)
    }


# 4. FILE + FORM DATA TOGETHER: important for RAG applications
@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), title: str = Form(...), source: str = Form(None)):
    # File and metadata are received in the same request.
    contents = await file.read()

    return {
        "filename": file.filename,
        "title": title,
        "source": source,
        "size": len(contents)
    }
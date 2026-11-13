#types of errors: http exception, validation errors (handled automatically)
#also study custom error responses


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Response model
class Document(BaseModel):
    id: int
    title: str
    content: str

# Request model
class DocumentCreate(BaseModel):
    title: str
    content: str
    pages: int

# Fake database
documents = {
    1: {"id": 1, "title": "Python", "content": "Learning Python"},
    2: {"id": 2, "title": "FastAPI", "content": "Learning FastAPI"}
}

# HTTP Exception: 
@app.get("/documents/{document_id}", response_model=Document)
def get_document(document_id: int):
    if document_id not in documents:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return documents[document_id]
#however in this, the detail isnt informative enough for the frontend to know what exactly happened and we want it 
# to receive something more informative so the frontend can check error_code and decide what to do instead of 
# trying to interpret a plain text message. So it is done like this: 

@app.get("/documents/{document_id}", response_model=Document)
def get_document(document_id: int):
    if document_id not in documents:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "DOCUMENT_NOT_FOUND",
                "message": "The requested document does not exist",
                "document_id": document_id
            }
        )
    return documents[document_id]

# 2. AUTOMATIC VALIDATION ERRORS (422)
@app.post("/documents", response_model=Document)
def create_document(data: DocumentCreate):
    new_document = {
        "id": 3,
        "title": data.title,
        "content": data.content
    }
    return new_document


# 3. CUSTOM / STRUCTURED ERROR RESPONSE
@app.get("/documents/custom/{document_id}", response_model=Document)
def get_document_custom(document_id: int):

    if document_id not in documents:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "DOCUMENT_NOT_FOUND",
                "message": "The requested document does not exist",
                "document_id": document_id
            }
        )

    return documents[document_id]


# 4. BUSINESS RULE ERROR (400)
@app.post("/documents/check", response_model=Document)
def check_document(data: DocumentCreate):
    if data.pages <= 0:
        raise HTTPException(
            status_code=400,
            detail="Document must have at least one page"
        )

    return {
        "id": 3,
        "title": data.title,
        "content": data.content
    }

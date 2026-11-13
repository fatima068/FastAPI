#yield splits a dependency in to two phases: 
# before yield part runs before the endpoint (like a setup)
# after yield code runs after end point finishes (solving the problem of cleanup)

# yield pauses the function instead of ending it.
# After the endpoint finishes, FastAPI resumes the dependency function and executes the code after yield.


from fastapi import FastAPI, Depends, HTTPException
import httpx

app = FastAPI()

# 1. FAKE DATABASE
documents = {
    1: {"id": 1, "title": "Python"},
    2: {"id": 2, "title": "FastAPI"}
}


# Simulating a database session
class Database:
    def get_document(self, document_id: int):
        return documents.get(document_id)
    
    def close(self):
        print("Database connection closed!")


# 2. YIELD DEPENDENCY: DATABASE SESSION
def get_db():
    # SETUP: Open database session
    db = Database()
    print("Database connection opened!")
    try:
        # Pass database session to endpoint
        yield db
    finally:
        # CLEANUP: Always close database session
        db.close()


# 3. ENDPOINT USING DATABASE DEPENDENCY
@app.get("/documents/{document_id}")
def get_document(document_id: int, db: Database = Depends(get_db)):
    # Use the injected database session
    document = db.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    return document


# 4. YIELD DEPENDENCY: ASYNC HTTP CLIENT
async def get_http_client():
    # SETUP: Create asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        try:
            # Pass client to endpoint
            yield client
        finally:
            # CLEANUP happens when the context exits
            print("HTTP client dependency finished!")


# 5. ENDPOINT USING HTTP CLIENT
@app.get("/external")
async def get_external_data(client: httpx.AsyncClient = Depends(get_http_client)):
    # Use injected HTTP client to make an external request
    response = await client.get("https://api.github.com")
    return {
        "status_code": response.status_code,
        "data": response.json()
    }

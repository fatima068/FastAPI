# A dependency is simply a regular Python function that provides something your endpoint needs
from fastapi import FastAPI, Depends, Header, HTTPException
import os

app = FastAPI()

# 1. CONFIGURATION
EXPECTED_API_KEY = os.getenv("API_KEY", "secret123") #loading from env variables 
# 2. FAKE DATABASE
documents = {
    1: {"id": 1, "title": "Python"},
    2: {"id": 2, "title": "FastAPI"}
}


# 3. DEPENDENCY: API KEY AUTHENTICATION : multiple functions need this, so build it once then do dependency injection 
def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    if api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key


# 4. DEPENDENCY: DATABASE ACCESS
def get_database():
    return documents

# 5. DEPENDENCY: LLM CLIENT
class FakeLLMClient:
    def generate(self, prompt: str):
        return f"AI response to: {prompt}"
#above were the three dependencies for this example program

def get_llm_client():
    # Simulating an initialized LLM client.
    # In a real application, this could return an OpenAI client or another model client.
    return FakeLLMClient()


# 6. ENDPOINT 1: GET DOCUMENTS
@app.get("/documents")
def get_documents(api_key: str = Depends(verify_api_key), db: dict = Depends(get_database)): #can pass the func without () in depends 
    return {
        "documents": list(db.values())
    }


# 7. ENDPOINT 2: ASK AI
@app.get("/ask")
def ask_ai(prompt: str, api_key: str = Depends(verify_api_key), db: dict = Depends(get_database),
           llm: FakeLLMClient = Depends(get_llm_client)):
    
    # Endpoint can directly use its injected dependencies.
    response = llm.generate(prompt)
    return {
        "prompt": prompt,
        "response": response,
        "available_documents": len(db)
    }

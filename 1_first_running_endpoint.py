from fastapi import FastAPI #importing the FastAPI class from the fastapi lib
from pydantic import BaseModel

app = FastAPI() #creating obj of FastAPI class

# GET request 
@app.get("/") #.get is the http method GET, "/" is the url 
#"When sends a GET request to the root URL /, execute the function immediately below this decorator
def read_root():
    return {"message" : "hello"} #returning the response 

# to run: uv run uvicorn main:app --reload 
# main = your Python file (main.py).
# app = the FastAPI application object inside that file.
# --reload = automatically restarts the server when you change your code.



#path parameter & query parameter: 
# you need your routes to accept dynamic values (eg fetching documents by id) and these are two ways to do it




# POST request
@app.post("/greet") #registers a post endpoint at /greet 
def greet(data: dict): # data parameter receives the JSON data sent in the HTTP request body by client
    #FastAPI automatically rds JSON from req body, conv to dict, passes that dic to func as param
    # So internally, your function receives: data = {"name": "Fatima"}
    # And you can access it using: 
    name = data["name"]
    return {"message": f"Hello {name}!"}


#use pydantic response and request models used to define what goes in/comes out of api     

# defining the request model: 
class User(BaseModel):
    name : str
    age: int
    email : str

@app.post("/users")
def create_user(user : User): #using the defined model in endpoint - do not accept a random dictionary now 
    return {
        "name" : user.name,
        "age" : user.age,
        "email" : user.email
    }

# same way for response model: 
class UserResponse(BaseModel):
        name: str
        age: int
        email: str

@app.get("/users", response_model=UserResponse) # specifying the response model here (unlike request, where it is specified in the parameter)
def get_user():
     return {
          "name" : "fatima", 
          "age" : 21,
          "email" : "wasimfatima4@gmail.com",
          "password" : "daydreaming"
     } #returning all the data but the response model trims out the password 



# 1. Client sends a POST request
# {
#   "name": "Fatima",
#   "age": 20
# }

# 2. FastAPI validates incoming JSON via the Request Model 
# 3. Your Python function executes
# 4. FastAPI validates and filters output, using the response model to determine which fields to return.
# 5. Client receives the response


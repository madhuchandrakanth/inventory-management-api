# 1. Import the FastAPI class from the fastapi package. 
# This class provides all the core functionality for routing and data validation.
from fastapi import FastAPI

# 2. Create an instance of the FastAPI application.
# The 'app' variable is the actual application object that handles incoming web requests.
app = FastAPI()

# 3. Define a "Route" or "Endpoint". 
# The @app.get("/") decorator tells FastAPI that any HTTP GET requests sent to the 
# root URL (like http://localhost:8000/) should be handled by the function below it.
@app.get("/")
def read_root():
    # FastAPI automatically converts Python dictionaries into JSON format 
    # when returning this response back to the client's browser or app.
    return {"Hello": "World"}

# 4. Start the development server.
# This block ensures the server only starts if you run this script directly 
# (e.g., by typing 'python main.py' in the terminal).
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run starts the web server which listens for traffic. 
    # We use "127.0.0.1" (localhost) so it runs safely on your local machine, on port 8000.
    uvicorn.run(app, host="127.0.0.1", port=8000)
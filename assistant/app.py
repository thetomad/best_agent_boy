"""
FastAPI app for AI Assistant development.

"""
from fastapi import FastAPI


app = FastAPI()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("assistant.app:app", host="0.0.0.0", port=8000, reload=True, server_header=False)



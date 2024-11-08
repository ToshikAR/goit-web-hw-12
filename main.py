from fastapi import FastAPI, Depends, HTTPException
import uvicorn

from src.app_contacts import routes_contacts
from src.app_index import routes_index
from src.app_users import routes_auth


app = FastAPI(title="Contact Application")
app.include_router(routes_index.router)
app.include_router(routes_auth.router, prefix="/api")
app.include_router(routes_contacts.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "REST APP v1.0"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

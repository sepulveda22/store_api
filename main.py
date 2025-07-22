from fastapi import FastAPI
from routes import auth, user, products
from database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(products.router)

@app.get("/")
async def read_root():
    return {"message": "Bienvenidos a mi API."}
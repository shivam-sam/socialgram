from fastapi import FastAPI
from .database import Base, engine
from .api import router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Social Media App",
    description="App to share updates about life socially",
    version="0.1"
)
app.include_router(router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, )

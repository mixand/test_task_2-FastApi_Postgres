import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import database
from routers import router_data
from data_env import name_application, version_application, main_url

app = FastAPI(
    title=name_application,
    version=version_application,
    swagger_ui_parameters={
        "url": f"{main_url}/openapi.json",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "requestSnippetsEnabled": True,

    },
    servers=[
        {"url": main_url},
    ]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router_data.router)


@app.get('/ping', response_model=str, include_in_schema=False)
def ping_api():
    return 'pong'


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8094,
        reload=True
    )

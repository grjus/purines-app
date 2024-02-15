"""Fast api"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from model.db_init import drop_and_initilize_database
from routes import purine

app = FastAPI()


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(purine.router)


@app.get("/health-check")
async def health_check():
    return {"msg": "I am alive"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, _: RequestValidationError):
    return templates.TemplateResponse(request,"modal/add-product-error.html", status_code=422)


if __name__ == "__main__":
    drop_and_initilize_database()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

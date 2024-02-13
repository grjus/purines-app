"""Fast api"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles


import uvicorn

from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


from model.db_init import drop_and_initilize_database

from routes import purine


app = FastAPI()


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(purine.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return HTMLResponse(
        content="""<div class="alert alert-danger" role="alert">
  Error adding product. Verify your input data.
</div>"""
    )


if __name__ == "__main__":
    drop_and_initilize_database()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

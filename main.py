import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from model.repository import PurinesRepository
from service.purine_service import PurineService

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    repository = PurinesRepository()
    data = PurineService(repository).get_all_purines()
    return templates.TemplateResponse(
        "index.html", {"request": request, "purines": data}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

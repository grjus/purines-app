from typing import Annotated, Any, Optional
import uvicorn
import yaml
import json
from fastapi import FastAPI, Form, Header
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from model.db_init import DbInitialization

from model.repository import PurinesRepository
from service.purine_service import PurineService


app = FastAPI()


templates = Jinja2Templates(directory="templates")


with open("./settings.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
    db_path = config.get("sql").get("db_path", "./data.db")
    drop_db = config.get("sql").get("drop_db", False)
    if not db_path:
        raise ValueError("Error finding database")


@app.get("/", response_class=HTMLResponse)
async def purine_table(
    request: Request, hx_request: Annotated[list[str] | None, Header()] = None
):

    query = request.query_params.get("search")
    # repository = PurinesRepository()
    # service = PurineService(repository)
    # data = service.get_all_purines_matching_query(query)
    # context = {"request": request, "purines": data}
    # if hx_request:
    #     return templates.TemplateResponse("purines-rows.html", context)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/show-modal", response_class=HTMLResponse)
async def show_modal(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("add-product-modal.html", context)


@app.post("/add-product")
async def add_product(name: Annotated[str, Form()], value: Annotated[str, Form()]):
    def is_int(number: Any) -> bool:
        try:
            int(number) == number
        except (TypeError, ValueError):
            return False

    if not name or not value or not is_int(value):
        return HTMLResponse(
            status_code=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"movieListChanged": None, "error": "Error addin info"}
                )
            },
        )

    return templates.TemplateResponse("add-product-modal.html")


if __name__ == "__main__":
    if drop_db:
        DbInitialization(db_path).init()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

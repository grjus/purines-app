"""Fast api"""

from fastapi.staticfiles import StaticFiles
from loguru import logger
from typing import Optional

from pydantic import BaseModel, ValidationError, validator
import uvicorn
import yaml
from fastapi import FastAPI, Form, Header
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from model.db_init import DbInitialization
from model.purine_repository import PurineFilter
from service.purine_group_service import PurineGroupService
from service.purine_service import PurineService


app = FastAPI()


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


with open("./settings.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
    db_path = config.get("sql").get("db_path", "./data.db")
    drop_db = config.get("sql").get("drop_db", False)
    if not db_path:
        raise ValueError("Error finding database")


@app.get("/", response_class=HTMLResponse)
async def purine_table(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request:
        service = PurineService()
        query = request.query_params
        search = query.get("search")
        product_group = query.get("product-group")
        show_high = query.get("show-high")
        if show_high == "undefined":
            show_high = None
        context = {
            "request": request,
            "purines": service.get_all_purines_matching_query(
                PurineFilter(
                    search,
                    product_group,
                    bool(show_high),
                )
            ),
        }
        return templates.TemplateResponse("purines-rows.html", context)
    service = PurineService()
    service_group = PurineGroupService()
    context = {
        "request": request,
        "purines": service.get_all_purines(),
        "purine_group": service_group.get_all_purine_groups(),
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/template/create-purine-modal")
async def get_create_purine_modal(request: Request):
    service_group = PurineGroupService()
    context = {
        "request": request,
        "purine_group": service_group.get_all_purine_groups(),
    }
    return templates.TemplateResponse("create-product-modal.html", context=context)


class AddProductCommand(BaseModel):
    name: str
    value: int
    group_uuid: str

    @validator("group_uuid")
    def check_group_exist(cls, value):
        purine_group = PurineGroupService().find(value)
        if not purine_group:
            raise ValueError(f"Purine {value} does not exist")
        return value


@app.post("/api/add-product")
async def create_product(request:Request,
    name: str = Form(...), value: int = Form(...), product_group: str = Form(...)
):
    logger.debug(name, value, product_group)
    if(request.sta)
    try:
        add_product_command = AddProductCommand(
            name=name,
            value=value,
            group_uuid=product_group,
        )
        PurineService().add_product(
            add_product_command.name,
            add_product_command.value,
            add_product_command.group_uuid,
        )

        return HTMLResponse(
            content="""<div class="alert alert-primary" role="alert">New product created</div>"""
        )
    except ValidationError as e:
        return HTMLResponse(
            content=f"""<div class="alert alert-primary" role="alert">Error creating product {e}</div>"""
        )


if __name__ == "__main__":
    if drop_db:
        DbInitialization(db_path).init()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

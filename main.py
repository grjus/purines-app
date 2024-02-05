from typing import Optional
import uvicorn
import yaml
from fastapi import FastAPI, Header
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from model.db_init import DbInitialization
from model.purine_repository import PurineFilter
from service.purine_group_service import PurineGroupService
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
async def purine_table(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request:
        service = PurineService()
        query = request.query_params
        print(f"Keys: {query.keys()}")
        context = {
            "request": request,
            "purines": service.get_all_purines_matching_query(
                PurineFilter(
                    query.get("search"),
                    query.get("product-group"),
                    bool(query.get("show-high")),
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


if __name__ == "__main__":
    if drop_db:
        DbInitialization(db_path).init()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

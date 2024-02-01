from typing import Optional
import uvicorn
import yaml
from fastapi import FastAPI, Header
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
async def purine_table(request: Request, hx_request: Optional[str] = Header(None)):

    query = request.query_params.get("search")
    repository = PurinesRepository()
    service = PurineService(repository)
    data = service.get_all_purines_matching_query(query)
    context = {"request": request, "purines": data}
    if hx_request:
        return templates.TemplateResponse("purines-rows.html", context)
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    DbInitialization(db_path, drop_db).initialize_db().populate_mock_data()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

""" Purine table route"""

from email import message
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import ValidationError

from di.providers import Providers
from exception import EntityNotFoundException
from model.purine_repository import PurineFilter
from service.command import AddProductCommand
from service.purine_group_service import PurineGroupService
from service.purine_service import PurineService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def purine_table(
    request: Request,
    hx_request: Optional[str] = Header(None),
    purine_service: PurineService = Depends(Providers.get_purine_service),
    group_service: PurineGroupService = Depends(Providers.get_group_service),
):
    if hx_request:
        query = request.query_params
        search = query.get("search")
        product_group = query.get("product-group")
        show_high = query.get("show-high")
        if show_high == "undefined":
            show_high = None
        context = {
            "purines": purine_service.get_all_purines_matching_query(
                PurineFilter(
                    search,
                    product_group,
                    bool(show_high),
                )
            ),
        }
        return templates.TemplateResponse(request, "purines-rows.html", context)

    context = {
        "purines": purine_service.get_all_purines(),
        "purine_group": group_service.get_all_purine_groups(),
    }
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/template/create-purine-modal")
async def get_create_purine_modal(
    request: Request,
    group_service: PurineGroupService = Depends(Providers.get_group_service),
):
    context = {
        "purine_group": group_service.get_all_purine_groups(),
    }
    return templates.TemplateResponse(
        request, "modal/create-product-modal.html", context=context
    )


@router.post("/api/add-product")
async def create_product(
    request: Request,
    name: str = Form(...),
    value: int = Form(...),
    product_group: str = Form(...),
    purine_service: PurineService = Depends(Providers.get_purine_service),
):
    logger.debug(name, value, product_group)
    try:
        add_product_command = AddProductCommand(
            name=name,
            value=value,
            group_uuid=product_group,
        )
        purine_service.add_product(add_product_command)

        return templates.TemplateResponse(request, "modal/add-product-success.html")

    except ValidationError as e:
        logger.error(f"Failed to add product: {e}")


@router.post("/api/delete-product/{product_uuid}")
async def delete_product(
    request: Request,
    product_uuid: str,
    service: PurineService = Depends(Providers.get_purine_service),
):
    try:

        service.delete_product(product_uuid)
        form = await request.form()
        logger.info(form.items())
        search = str(form.get("search"))
        product_group = str(form.get("product-group"))
        show_high = form.get("show-high")
        if show_high == "undefined":
            show_high = None
        logger.info(f"Some information: {search},{product_group},{bool(show_high)}")
        purines = service.get_all_purines_matching_query(
            PurineFilter(search, product_group, bool(show_high))
        )
        context = {"purines": purines}
        return templates.TemplateResponse(request, "purines-rows.html", context=context)
    except EntityNotFoundException as e:
        logger.error(f"Failed to delete product: {product_uuid}", e)
        raise HTTPException(detail=e.message, status_code=404)

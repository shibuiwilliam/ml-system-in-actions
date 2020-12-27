from fastapi import APIRouter, Body, BackgroundTasks
import logging
import aiohttp
import asyncio
from typing import Dict, Any
from pydantic import BaseModel
import uuid

from src.api_composition_proxy.configurations import ServiceConfigurations
from src.api_composition_proxy import helpers
from src.jobs import store_data_job
from src.helper import get_job_id

logger = logging.getLogger(__name__)

router = APIRouter()


class Data(BaseModel):
    data: Any = None
    ab_test: str = "default"


async def _get_redirect(session, url: str, alias: str) -> Dict[str, Any]:
    async with session.get(url) as response:
        response_json = await response.json()
        resp = {alias: {"response": response_json, "status_code": response.status}}
        logger.info(f"response: {resp}")
        return resp


@router.get("/{redirect_path:path}")
async def get_redirect(redirect_path: str) -> Dict[str, Any]:
    logger.info(f"GET redirect abtest to: /{redirect_path}")
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
        tasks = [
            asyncio.ensure_future(
                _get_redirect(session, helpers.customized_redirect_builder(k, v, redirect_path, ServiceConfigurations.customized_redirect_map), k)
            )
            for k, v in ServiceConfigurations.urls.items()
        ]
        responses = await asyncio.gather(*tasks)
        logger.info(f"responses: {responses}")
        return responses


async def _post_redirect(session, url: str, data: Dict[Any, Any], alias: str) -> Dict[str, Any]:
    async with session.post(url, json=data) as response:
        response_json = await response.json()
        resp = {alias: {"response": response_json, "status_code": response.status}}
        logger.info(f"response: {resp}")
        return resp


@router.post("/{redirect_path:path}")
async def post_redirect(redirect_path: str, data: Data, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    data.data["job_id"] = get_job_id()
    logger.info(f'POST redirect abtest to: /{redirect_path} as {data.data["job_id"]} with group {data.ab_test}')

    if data.ab_test.upper() in ServiceConfigurations.ab_test_group.keys():
        group_alias = ServiceConfigurations.ab_test_group[data.ab_test.upper()]
        customized_redirect_map = {group_alias: ServiceConfigurations.customized_redirect_map[group_alias]}
    else:
        customized_redirect_map = ServiceConfigurations.customized_redirect_map

    if ServiceConfigurations.enqueue:
        store_data_job._save_data_job(data.data, data.data["job_id"], background_tasks, True)
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
        tasks = [
            asyncio.ensure_future(_post_redirect(session, helpers.customized_redirect_builder(k, v, redirect_path, customized_redirect_map), data.data, k))
            for k, v in ServiceConfigurations.urls.items()
            if k in customized_redirect_map.keys()
        ]
        responses = await asyncio.gather(*tasks)
        logger.info(f"responses: {responses}")
        return responses

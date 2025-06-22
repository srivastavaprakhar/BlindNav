from fastapi import APIRouter, Query
from services.parser import extract_elements
from services.interpreter import generate_description
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/describe")
async def describe_page(url: str = Query(..., description="URL of the webpage")):
    try:
        logger.info(f"Fetching and describing URL: {url}")
        elements = extract_elements(url)
        description = generate_description(elements)
        return {"success": True, "description": description}
    except Exception as e:
        logger.exception("Error while processing request")
        return {"success": False, "error": str(e)}

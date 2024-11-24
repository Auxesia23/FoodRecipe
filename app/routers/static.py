from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..routers.meals import UPLOAD_DIR

router = APIRouter(tags=["Static"])

@router.get("/static/images/{filename}")
async def get_image(filename: str):
    """
    Retrieve an image by its filename.
    """
    file_path = UPLOAD_DIR / filename

    # Check if the file exists
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image as a file response
    return FileResponse(file_path)

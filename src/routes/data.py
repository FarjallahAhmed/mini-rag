from fastapi import APIRouter,UploadFile, Depends, status
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from fastapi.responses import JSONResponse
import aiofiles
from models import ResponseSignal
import logging


logger = logging.getLogger("uvicorn.error")
router_data = APIRouter(
    prefix="/api/v1/data",
    tags=["data","api_v1"]

)

@router_data.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings : Settings = Depends(get_settings)):


    data_controller = DataController()
    is_valid, result = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result
            }
        )
    project_dir = ProjectController().get_project_path(project_id=project_id)

    file_path = data_controller.generate_unique_filename(org_file_name=file.filename,project_id=project_id)

    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={
                "signal" : ResponseSignal.FILE_UPLOAD_ERROR.value
            }
        )

    return JSONResponse(
        content={
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value
        }
    )

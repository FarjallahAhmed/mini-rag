from fastapi import APIRouter,UploadFile, Depends
import os
from helpers.config import get_settings, Settings
from controllers import DataController

router_data = APIRouter(
    prefix="/api/v1/data",
    tags=["data","api_v1"]

)

@router_data.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings : Settings = Depends(get_settings)):
    is_valid = DataController().validate_uploaded_file(file=file)

    return is_valid
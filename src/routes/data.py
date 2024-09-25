from fastapi import APIRouter,UploadFile, Depends, status, Request
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from fastapi.responses import JSONResponse
import aiofiles
from models import ResponseSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
import logging
from .schemes.data import ProcessRequest
from models.db_schemes import DataChunk

logger = logging.getLogger("uvicorn.error")
router_data = APIRouter(
    prefix="/api/v1/data",
    tags=["data","api_v1"]

)

@router_data.post("/upload/{project_id}")
async def upload_data(request: Request,project_id: str, file: UploadFile, app_settings : Settings = Depends(get_settings)):

    project_model = ProjectModel(request.app.db_client)

    project = await project_model.get_or_create_project(project_id=project_id)

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

    file_path,file_id = data_controller.generate_unique_filename(org_file_name=file.filename,project_id=project_id)

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
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
            "project_id": str(project.id)
        }
    )

@router_data.post("/process/{project_id}")
async def process(project_id,process_request: ProcessRequest,request: Request):

    process = ProcessController(project_id=project_id)
    file_content = process.get_file_content(file_id=process_request.file_id)

    project_model = ProjectModel(request.app.db_client)

    project = await project_model.get_or_create_project(project_id=project_id)
    
    file_chunks = process.process_file_content(
        file_content=file_content,
        file_id=process_request.file_id,
        chunk_size=process_request.chunk_size,
        overlap_size=process_request.overlap_size
        )
    
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )
    
    file_chunk_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_object_id=project.id
        )
        for i,chunk in enumerate(file_chunks)
    ]

    chunk_model = ChunkModel(request.app.db_client)

    no_recodrs = await chunk_model.insert_many_chunks(chunks=file_chunk_records)
    
    return JSONResponse(
        status_code= status.HTTP_201_CREATED,
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunk": no_recodrs
        }
    )

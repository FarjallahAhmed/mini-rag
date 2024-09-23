from helpers.config import Settings
from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnums import DataBaseEnum
class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object) -> None:
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self,project: Project):

        result = await self.collection.insert_one(project.model_dump())
        project._id = result.inserted_id

        return project
    

    async def get_or_create_project(self,project_id: str):

        record = await self.collection.find_one({
            "project_id":project_id
        })

        if record is None:
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)
            return project
        
        return Project(**record)
    
    async def get_all_projects(self,page: int = 0,page_size: int = 10):

        total_documents= self.collection.count_documents({})

        total_pages = total_documents // page_size

        if total_documents % page_size > 0:
            total_pages = total_pages + 1 

        cursor = self.collection.find().skip((page-1) * page_size).limit(page_size)

        projects =[]
        async for document in cursor:
            projects.append(
                Project(**document)
            )

        return projects, total_pages
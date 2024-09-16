from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re 
import os
class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_uploaded_file(self,file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.FILE_SIZE_EXCEEDED.value
        return True,ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filename(self,org_file_name: str,project_id:str):

        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_filename = self.get_clean_file_name(org_file_name=org_file_name)

        new_file_path = os.path.join(
            project_path,
            random_filename + "_" +cleaned_filename
        )
        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_filename + "_" +cleaned_filename
            )

        return new_file_path

    def get_clean_file_name(self, org_file_name: str):

        cleaned_filename = re.sub(r'[^\w.]','',org_file_name.strip())

        cleaned_filename = cleaned_filename.replace(" ","_")

        return cleaned_filename
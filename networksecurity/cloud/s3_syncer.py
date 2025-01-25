import os

class S3Sync:
    def sync_folder_to_s3(self, folder:str, s3_url:str):
        os.system(f"aws s3 sync {folder} {s3_url}")
        
    def sync_file_to_s3(self, file:str, s3_url:str):
        os.system(f"aws s3 cp {file} {s3_url}")
    
    def sync_folder_from_s3(self, s3_url:str, folder:str):
        os.system(f"aws s3 sync {s3_url} {folder}")
        
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from fastapi import UploadFile
from .interface import FileRepository
from PIL import Image
from eventer.core.config import settings
import time
import os


class MinioRepository(FileRepository):
    def __init__(self, client: Minio, bucket: str) -> None:
        self.client = client
        self.bucket = bucket
        self._ensure_bucket_exists()
        
    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            raise RuntimeError(f"Bucket error: {e}")

    async def upload(self, event_id: int, file: UploadFile):
        try:
            if file is None:
                raise ValueError("No file provided")

            file_content = await file.read()

            with Image.open(BytesIO(file_content)) as img:
                img = img.convert("RGB") 

                output = BytesIO()
                img.save(output, format="WEBP", quality=90)
                output.seek(0) 
                
            file_extension = file.filename.rsplit('.', 1)
            new_filename = f"{int(time.time())}.webp"
            object_name = f"events/{event_id}/{new_filename}"

            self.client.put_object(
                bucket_name=self.bucket,
                object_name=object_name,
                data=output,
                length=output.getbuffer().nbytes,
                content_type="image/webp",
            )

            return object_name

        except S3Error as e:
            raise FileExistsError(f"File {file.filename} already exists: {str(e)}")

        except Exception as e:
            raise ValueError(f"Image upload failed: {str(e)}")

    def download(self, filename: str) -> BytesIO:
        try:
            response = self.client.get_object(self.bucket, filename)
            return BytesIO(response.read())
        except S3Error:
            raise FileNotFoundError(f"File {filename} not found")
        finally:
            response.close()
            response.release_conn()

    def delete(self, filename: str):
        try:
            self.client.remove_object(self.bucket, filename)
        except S3Error as e:
            raise FileNotFoundError(f"File {filename} not found")


def get_minio_repo() -> MinioRepository:
    return MinioRepository(
        client=Minio(
            endpoint=settings.minio_cfg.endpoint,
            access_key=settings.minio_cfg.access_key,
            secret_key=settings.minio_cfg.secret_key,
            secure=settings.minio_cfg.secure,
        ),
        bucket=settings.minio_cfg.bucket,
    )

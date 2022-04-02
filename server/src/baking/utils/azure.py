import os
import uuid
from azure.storage.blob import BlobServiceClient
from baking.config import settings
from baking.models import FileUploadData
from fastapi.logger import logger


blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
    settings.azure_storage_connection_string)

IMAGES_CONTAINER = "images"




def upload_image_to_blob(file_name: str, file_content: bytes) -> FileUploadData:
    try:
        filename = str(uuid.uuid4()) + os.path.splitext(file_name)[1]
        blob_client = blob_service_client.get_blob_client(
            container=IMAGES_CONTAINER, blob=filename)
        blob_client.upload_blob(file_content)

        f = FileUploadData(url=blob_client.url, identidier=filename)
        return f
    except Exception as e:
        logger.error(e)
        raise e


def delete_image_from_blob(identidier: str):
    if identidier is None or identidier == "":
        return None

    try:
        blob_client = blob_service_client.get_blob_client(
            container=IMAGES_CONTAINER, blob=identidier)
        blob_client.delete_blob()
    except Exception as e:
        logger.error(e)
        raise 
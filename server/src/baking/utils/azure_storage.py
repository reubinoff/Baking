from functools import lru_cache
import os
import uuid
from baking.config import settings
from baking.models import FileUploadData
from fastapi.logger import logger
from azure.storage.blob import BlobServiceClient




IMAGES_CONTAINER = "images"

@lru_cache
def _get_blob_client():
    if settings.azure_storage_connection_string is None or settings.azure_storage_connection_string == "":
        return FakeAzureStorageClient()
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string)
    return blob_service_client


def upload_image_to_blob(file_name: str, file_content: bytes) -> FileUploadData:
    try:
        filename = str(uuid.uuid4()) + os.path.splitext(file_name)[1]
        blob_client = _get_blob_client().get_blob_client(
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
        blob_client = _get_blob_client().get_blob_client(
            container=IMAGES_CONTAINER, blob=identidier)
        blob_client.delete_blob()
    except Exception as e:
        logger.error(e)
        raise 

def delete_all_images_from_blob():
    try:
        blob_client = _get_blob_client()
        container_client = blob_client.get_container_client(IMAGES_CONTAINER)
        blobs = container_client.list_blobs()
        for blob in blobs:
            container_client.delete_blob(blob.name)
    except Exception as e:
        logger.error(e)
        raise
###################################################################################################

class FakeAzureBlobClient:
    def upload_blob(self, file_content):
        pass

    def delete_blob(self):
        pass
class FakeAzureStorageClient:
    def get_blob_client(self, container, blob):
        return FakeAzureBlobClient()

###################################################################################################

if __name__ == "__main__":
    delete_all_images_from_blob()
    with open("/tmp/t.jpeg", "rb") as f:
        a = upload_image_to_blob("test.jpeg", f.read())
        print(a)


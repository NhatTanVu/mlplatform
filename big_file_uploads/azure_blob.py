from datetime import datetime, timedelta, timezone
from django.conf import settings
from azure.storage.blob import generate_blob_sas, BlobSasPermissions


def generate_upload_sas(blob_name):
    sas = generate_blob_sas(
        account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
        container_name=settings.AZURE_STORAGE_CONTAINER,
        blob_name=blob_name,
        account_key=settings.AZURE_STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(write=True, create=True),
        expiry=datetime.now(timezone.utc) + timedelta(minutes=15),
    )

    return f"{settings.AZURE_STORAGE_ACCOUNT_URL}/{settings.AZURE_STORAGE_CONTAINER}/{blob_name}?{sas}"
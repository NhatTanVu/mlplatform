import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import SlideUpload
from .azure_blob import generate_upload_sas


@login_required
@require_POST
def request_upload_url(request):
    data = json.loads(request.body)
    filename = data["filename"]
    file_size = data["file_size"]

    blob_name = f"user_{request.user.id}/{filename}"

    upload_url = generate_upload_sas(blob_name)

    blob_url = (
        f"{settings.AZURE_STORAGE_ACCOUNT_URL}/"
        f"{settings.AZURE_STORAGE_CONTAINER}/"
        f"{blob_name}"
    )

    SlideUpload.objects.create(
        user=request.user,
        original_filename=filename,
        blob_name=blob_name,
        blob_url=blob_url,
        file_size=file_size,
        status="INIT",
    )

    return JsonResponse({
        "upload_url": upload_url,
        "blob_name": blob_name,
        "blob_url": blob_url,
    })


@login_required
@require_POST
def confirm_upload(request):
    data = json.loads(request.body)
    blob_name = data["blob_name"]

    upload = SlideUpload.objects.get(
        user=request.user,
        blob_name=blob_name
    )

    upload.status = "UPLOADED"
    upload.save()

    return JsonResponse({
        "ok": True, 
        "blob_url": upload.blob_url
    })


@login_required
def upload_page(request):
    return render(request, "upload.html")
"""
utils/storage.py — Upload files to AWS S3 or fall back to local Django media storage.
"""
import os
import uuid
import shutil
from django.conf import settings

USE_S3 = all([
    settings.AWS_ACCESS_KEY_ID,
    settings.AWS_SECRET_ACCESS_KEY,
    settings.S3_BUCKET_NAME,
])


def upload_file(local_path: str, prefix: str = "videos") -> str:
    filename = f"{prefix}/{uuid.uuid4().hex}_{os.path.basename(local_path)}"

    if USE_S3:
        import boto3
        from botocore.exceptions import NoCredentialsError, ClientError

        bucket = settings.S3_BUCKET_NAME
        region = settings.AWS_REGION
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=region,
        )
        try:
            s3.upload_file(
                local_path, bucket, filename,
                ExtraArgs={"ContentType": "video/mp4"},
            )
            return f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"
        except (NoCredentialsError, ClientError) as e:
            print(f"[S3] Upload failed: {e}. Using local fallback.")

    # Local fallback — serve via Django MEDIA_URL
    dest_dir = os.path.join(settings.MEDIA_ROOT, prefix)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(local_path))
    shutil.copy2(local_path, dest)
    return f"{settings.MEDIA_URL}{prefix}/{os.path.basename(local_path)}"

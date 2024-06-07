# supabase_client.py

from supabase import create_client, Client
from django.conf import settings

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY
bucket: str = settings.SUPABASE_BUCKET

supabase: Client = create_client(url, key)

def upload_file(file_path, file_name):
    with open(file_path, "rb") as f:
        res = supabase.storage.from_(bucket).upload(file_name, f)
    return res

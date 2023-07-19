import mimetypes
import os
import posixpath
import tempfile
import threading
from datetime import datetime
from datetime import timedelta
from tempfile import SpooledTemporaryFile
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit

import pytz
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import SuspiciousOperation
from django.core.files.base import File
from django.utils.deconstruct import deconstructible
from django.core.files.storage import Storage
# from django.utils.encoding import filepath_to_uri


# from backend.database import supabase
import supabase

from backend.settings import *

@deconstructible
class SupabaseStorageFile(File):
    def __init__(self, name, mode, storage, buffer_size=None):
        if 'r' in mode and 'w' in mode:
            raise ValueError("Can't combine 'r' and 'w' in mode.")
        self._storage = storage
        self.name = name
        self._mode = mode
        self._force_mode = (lambda b: b) if 'b' in mode else (lambda b: b.decode())
        self._file = None
        self.buffer_size = buffer_size or 5242880

    @property
    def size(self):
        return self._storage.size(self.name)

    @property
    def closed(self):
        return not self._file or self._file.closed

    def _get_file(self):
        if self._file is None:
            self._file = SpooledTemporaryFile(
                max_size=self._storage.max_memory_size,
                suffix='.SupabaseStorageFile',
                dir=self._storage.file_upload_temp_dir
            )
            if 'r' in self._mode:
                self._is_dirty = False
                self._storage.client.storage().download(self.name, file=self._file)
                self._file.seek(0)
        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)

    def read(self, *args, **kwargs):
        if 'r' not in self._mode:
            raise AttributeError("File was not opened in read mode.")
        return self._force_mode(super().read(*args, **kwargs))

    def readline(self, *args, **kwargs):
        if 'r' not in self._mode:
            raise AttributeError("File was not opened in read mode.")
        return self._force_mode(super().readline(*args, **kwargs))

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was not opened in write mode.")
        if self._file is None:
            self._file = SpooledTemporaryFile(
                max_size=self._storage.max_memory_size,
                suffix='.SupabaseStorageFile',
                dir=self._storage.file_upload_temp_dir
            )
        bstr = content.encode() if isinstance(content, str) else content
        return self._file.write(bstr)

    def close(self):
        if self._file is not None:
            self._file.seek(0)
            self._storage.client.storage().upload(self.name, file=self._file)
            self._file.close()
            self._file = None


@deconstructible
class SupabaseStorage(Storage):
    default_content_type = 'application/octet-stream'

    def __init__(self, **settings):
        self.client = supabase.create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
        self.bucket_name = SUPABASE_BUCKET_NAME
        # self.file_upload_temp_dir = settings.get('file_upload_temp_dir')
        # self.default_acl = settings.get('default_acl')
        # self.max_memory_size = settings.get('max_memory_size')

    def _normalize_name(self, name):
        return name.lstrip('/')

    def _open(self, name, mode='rb'):
        name = self._normalize_name(name)
        return SupabaseStorageFile(name, mode, self)

    def _save(self, name, content):
        name = self._normalize_name(name)
        file_data = content.read()
        # self.client.storage().upload(name, file_data)
        # with open(content, 'rb+') as f:
        #     res = supabase.storage.from_(self.bucket_name).upload(name, f)
        # self.client.storage.get_bucket('Socialite').list()
        self.client.storage.from_(str(self.bucket_name)).upload(name, file_data)
        return name

    def delete(self, name):
        name = self._normalize_name(name)
        self.client.storage().remove(name)

    def exists(self, name):
        name = self._normalize_name(name)
        response = self.client.storage().list(name)
        return len(response.get('files', [])) > 0

    def listdir(self, name):
        name = self._normalize_name(name)
        response = self.client.storage().list(name)
        directories = []
        files = []
        for file_data in response.get('files', []):
            if file_data['name'].endswith('/'):
                directories.append(file_data['name'].strip('/'))
            else:
                files.append(file_data['name'].strip('/'))
        return directories, files

    def size(self, name):
        name = self._normalize_name(name)
        response = self.client.storage().get_metadata(name)
        return response['size']

    def get_modified_time(self, name):
        name = self._normalize_name(name)
        response = self.client.storage().get_metadata(name)
        modified_at = datetime.fromtimestamp(response['last_modified'] / 1000, pytz.UTC)
        return modified_at

    def url(self, name, parameters=None, expire=None, http_method=None):
        name = self._normalize_name(name)
        url = self.client.storage.from_(self.bucket_name).create_signed_url(name, expire=expire)
        return url

    def get_available_name(self, name, max_length=None):
        return name


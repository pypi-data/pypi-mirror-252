# python-file-storage

A Python package that exposes a consistent API for working with different
storage backends.

WARNING: This is still under active development.


## Why does this package exist?

I needed something that does not depend on Django but exposes a similar
interface to Django's base storage in `django.core.files.storage.base.Storage`.
So, if you're using Django: use Django and [django-storages][2] instead.
Currently, this package only does the bare minimum that I need it for so
if you're looking for something more full-featured perhaps look at the
[cloudstorage][3] package.


## Available backends

- Filesystem.
- Amazon S3.


## Quickstart

1. Install the package:
   ```
   pip install python-file-storage
   ```

1. Add your configuration. Set the following as environment variables or add
   them to a `.env` file in the root of your project:

   ```python
   DEFAULT_STORAGE_BACKEND = storage.backends.s3.S3Storage
   S3_BUCKET_NAME = my-bucket-name
   S3_ENDPOINT_URL = example.com # Optional
   S3_ACCESS_KEY_ID = 123
   S3_SECRET_ACCESS_KEY = 123
   ```

   Currently, using more than one storage backend at a time is unsupported.

1. Import `default_storage` and start using the package:

   ```python
   from storage import default_storage

   default_storage.save('example.txt', 'Content')
   file = default_storage.open('example.txt', 'Content')
   ```


## Compatibility

- Python 3.8+
- Django is unsupported.


## Versioning

This project follows [semantic versioning][1] (SemVer).




[//]: # (Links)

[1]: https://semver.org/
[2]: https://github.com/jschneier/django-storages
[3]: https://github.com/scottwernervt/cloudstorage

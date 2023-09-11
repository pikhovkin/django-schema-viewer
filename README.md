# django-schema-viewer

[![GitHub Actions](https://github.com/pikhovkin/django-schema-viewer/workflows/build/badge.svg)](https://github.com/pikhovkin/django-schema-viewer/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/django-schema-viewer.svg)](https://pypi.org/project/django-schema-viewer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-schema-viewer.svg)](https://pypi.org/project/django-schema-viewer)
[![PyPI - License](https://img.shields.io/pypi/l/django-schema-viewer.svg)](./LICENSE)

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Visualizes the DB schema based on Django models.

![django-schema-viewer screen](docs/screenview.png)

### Installation

```console
pip install django-schema-viewer
```

### Usage

1. Install the package

2. Add `schema_viewer` to your `INSTALLED_APPS` settings like this:

```python
INSTALLED_APPS = [
    ...,
    'schema_viewer',
    ...,
]
```

3. Add `schema_viewer.urls` to main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('schema-viewer', include('schema_viewer.urls')),
    ...,
]
```

4. Run the project

```console
python manange.py runserver
```

5. Go to http://127.0.0.1:8000/schema-viewer/

### Optional settings

```python
SCHEMA_VIEWER = {
    'apps': [
        'contenttypes',
        'my_app',
    ],
    'exclude': {
        'auth': ['User'],
        'my_app': ['SomeModel'],
    },
}
```

## License

MIT

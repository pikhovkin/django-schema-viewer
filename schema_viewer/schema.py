from collections.abc import Iterator
from typing import Any, cast

from django import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import connection, models


def get_app_models() -> Iterator[tuple[apps.AppConfig, type[models.Model]]]:
    for app in apps.apps.get_app_configs():
        for model in app.get_models():
            yield app, model


def get_app_name(model: type[models.Model]) -> str:
    app_label = model._meta.app_label
    try:
        return apps.apps.get_app_config(app_label).name
    except LookupError:
        return model.__module__


def get_model_id(model: type[models.Model]) -> str:
    return f"{model.__module__}.{model.__name__}"


def is_model_subclass(obj: type[models.Model]) -> bool:
    if obj is models.Model:
        return False
    return issubclass(obj, models.Model)


def _make_resource(app: apps.AppConfig, model: type[models.Model], app_names: list, excludes: dict) -> list[dict]:
    if app_names and app.name not in app_names:
        return []
    elif model._meta.proxy or model._meta.abstract:
        return []
    elif app.name in excludes and model.__name__.lower() in excludes[app.name]:
        return []

    resources: list[dict] = [
        {
            'name': model._meta.db_table,
            'title': f'{app.name}.{model.__name__}',
            'description': model._meta.verbose_name,
            'schema': {
                'fields': [],
                'primaryKey': [],
                'foreignKeys': [],
            },
        }
    ]
    schema_fields: list = resources[-1]['schema']['fields']
    schema_primary_key: list = resources[-1]['schema']['primaryKey']
    schema_foreign_keys: list = resources[-1]['schema']['foreignKeys']

    for field in model._meta.get_fields():
        if isinstance(field, GenericForeignKey):
            continue
        elif not field.concrete:
            continue
        elif field.many_to_many:
            if not field.auto_created and isinstance(field.remote_field, models.ManyToManyRel):
                m2m_model = field.remote_field.through
                if m2m_model is not None and m2m_model._meta.auto_created:
                    resources.extend(_make_resource(m2m_model._meta.app_config, m2m_model, app_names, excludes))
            continue
        elif field.model is not model:
            continue

        field_name: str = field.attname
        db_type: str | None = field.db_type(connection)
        if db_type is None:
            continue

        schema_fields.append(
            {
                'name': field_name,
                'title': getattr(field, 'verbose_name', ''),
                'description': getattr(field, 'verbose_name', ''),
                'type': db_type,
                'constraints': {
                    'required': not field.null,
                    'unique': field.unique,
                },
            }
        )
        if field.is_relation:
            rel_model = cast(type[models.Model], field.related_model)
            if rel_model is None:
                continue
            rel_model_app_name = get_app_name(rel_model)
            if app_names and rel_model_app_name not in app_names:
                continue
            if rel_model_app_name in excludes and rel_model.__name__.lower() in excludes[rel_model_app_name]:
                continue

            rel_field = rel_model._meta.pk
            if rel_field is None:
                continue

            schema_foreign_keys.append(
                {
                    'fields': field_name,
                    'reference': {
                        'resource': rel_model._meta.db_table,
                        'fields': [
                            rel_field.attname,
                        ],
                    },
                }
            )
        elif field.primary_key:
            schema_primary_key.append(field_name)

    return resources


def get_schema(conf: dict | None = None) -> dict:
    if not conf:
        conf = getattr(settings, 'SCHEMA_VIEWER', {}) or {}

    app_names = conf.get('apps', []) or []
    excludes = conf.get('exclude', {}) or {}

    json_table_schema: dict[str, Any] = {
        'resources': [],
        'name': '',
    }

    resources = json_table_schema['resources']
    for app, model in get_app_models():
        resources.extend(_make_resource(app, model, app_names, excludes))

    return json_table_schema

from django.db import models
from psqlextra.models import PostgresPartitionedModel, PostgresModel
from psqlextra.models.partitioned import ModelBase, PostgresPartitionedModelMeta


def get_addition_fields(attrs):
    new_attrs = {}
    for obj_name, obj in attrs.items():
        if isinstance(obj, models.ForeignKey):
            model = obj.remote_field.model
            if issubclass(model, PostgresPartitionedModel):
                field_name = model._partitioning_meta.key[0]
                field_obj = getattr(model, field_name).field
                _, _, ar, kw = field_obj.deconstruct()
                # kw['null'] = True
                new_attrs[f"{obj_name}_{field_name}"] = field_obj.__class__(*ar, **kw)
    return new_attrs


class FkPostgresPartitionedModelMeta(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        return super().__new__(cls, name, bases, {**attrs, **get_addition_fields(attrs)}, **kwargs)


class FkPostgresPartitionedModel(
    PostgresModel, metaclass=FkPostgresPartitionedModelMeta
):
    class Meta:
        abstract = True
        base_manager_name = "objects"


class FkFullPostgresPartitionedModelMeta(PostgresPartitionedModelMeta):
    def __new__(cls, name, bases, attrs, **kwargs):
        return super().__new__(cls, name, bases, {**attrs, **get_addition_fields(attrs)}, **kwargs)


class FkFullPostgresPartitionedModel(
    PostgresModel, metaclass=FkFullPostgresPartitionedModelMeta
):
    class Meta:
        abstract = True
        base_manager_name = "objects"

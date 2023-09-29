from sqlalchemy import inspect


def to_dict(obj):
    mapper_class = inspect(obj.__class__)
    columns = [column.key for column in mapper_class.columns]
    return {column: getattr(obj, column) for column in columns}

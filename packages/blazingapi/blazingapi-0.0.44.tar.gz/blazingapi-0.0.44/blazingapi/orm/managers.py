from blazingapi.orm.query import QuerySet


class Manager:

    def __init__(self, model):
        self.model = model
        self.cache = {}

    def all(self):
        return QuerySet(self.model).all()

    def filter(self, *args, **kwargs):
        return QuerySet(self.model).filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        return QuerySet(self.model).filter(*args, **kwargs).get()

    def get_foreign_key_reference_with_cache(self, fk):
        """
        Should be used only internally to retrieve a model instance from a foreign key reference.

        This prevents multiple queries for the same foreign key reference.
        """
        if fk in self.cache:
            return self.cache[fk]

        obj = QuerySet(self.model).filter(id=fk).get()
        self.cache[fk] = obj
        return obj


class RelatedModelManager:

    def __init__(self, model, foreign_instance, column_name):
        self.model = model
        self.foreign_instance = foreign_instance
        self.column_name = column_name

    def all(self):
        return QuerySet(self.model).filter(**{f"{self.column_name}": self.foreign_instance.id})

    def filter(self, *args, **kwargs):
        return self.all().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.all().filter(*args, **kwargs).get()

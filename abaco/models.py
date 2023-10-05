from abaco.database import get_db, get_table


class Model:
    id: int | None = None
    table_name: str

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def __get_db(self):
        return get_table(self.table_name, get_db())

    def as_dict(self):
        return self.__dict__

    def save(self):
        if self.id is None:
            self.id = self.__get_db().insert(self.__dict__)
        else:
            self.__get_db().update(self.__dict__, doc_ids=[self.id])
        return self.id

    def delete(self):
        return self.__get_db().remove(doc_ids=[self.id])[0]

    def find(self, id: int):
        data = self.__get_db().get(doc_id=id)
        if data is None:
            return None
        self.id = id
        for attr in data.keys():
            self.__setattr__(attr, data[attr])
        return self

    def all(self):
        results = []
        for row in self.__get_db().all():
            row['id'] = row.doc_id
            results.append(row)
        return results


class UserConfig(Model):
    name: str
    language: str
    currency: str

    def __init__(
        self,
        name: str | None = None,
        language: str | None = None,
        currency: str | None = None,
    ):
        super().__init__(table_name='user_config')
        self.name = name
        self.language = language
        self.currency = currency

    def save(self):
        if self.name is None:
            return None
        if self.language is None:
            return None
        if self.currency is None:
            return None
        return super().save()

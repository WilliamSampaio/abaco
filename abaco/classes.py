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


class UserConfig(Model):
    name: str
    language: str
    currency: str

    def __init__(self, name: str, language: str, currency: str):
        super().__init__(table_name='user_config')
        self.name = name
        self.language = language
        self.currency = currency

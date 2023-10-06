from datetime import datetime
from typing import Any

from abaco.database import get_db, get_table


class Model:
    id: int | None = None
    table_name: str

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def __get_db(self):
        return get_table(self.table_name, get_db())

    def as_dict(self):
        data = self.__dict__.copy()
        if 'id' in data:
            data.pop('id')
        data.pop('table_name')
        return data

    def save(self):
        if self.id is None:
            self.id = self.__get_db().insert(self.as_dict())
        else:
            self.__get_db().update(self.as_dict(), doc_ids=[self.id])[0]
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

    def all(self, where: tuple[str, Any] | None = None):
        results = []
        for row in self.__get_db().all():
            if where is not None:
                if row[where[0]] == where[1]:
                    row['id'] = row.doc_id
                    results.append(row)
            else:
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


class FixedDiscount(Model):
    description: str | None
    calculated_in: str | None
    value: float | None
    deleted: bool | None

    def __init__(
        self,
        description: str | None = None,
        calculated_in: str | None = None,
        value: float | None = None,
    ) -> None:
        super().__init__(table_name='fixed_discounts')
        self.description = description
        self.calculated_in = calculated_in
        self.value = value
        self.deleted = False

    def save(self):
        if self.description is None:
            return None
        if self.calculated_in is None or self.calculated_in not in [
            'porcentage',
            'value',
        ]:
            return None
        if self.value is None:
            return None
        if self.deleted is None:
            self.deleted = False
        return super().save()

    def available(self):
        return self.all(('deleted', False))


class Transaction(Model):
    description: str | None
    date: str | None
    value: float | None
    expense: bool | None
    fixed_discounts_ids: list[int] | None

    def __init__(
        self,
        description: str | None = None,
        date: str | None = None,
        value: float | None = None,
        expense: bool | None = None,
        fixed_discounts_ids: list[int] | None = None,
    ) -> None:
        super().__init__(table_name='transactions')
        self.description = description
        self.date = date
        self.value = value
        self.expense = expense
        self.fixed_discounts_ids = fixed_discounts_ids

    def save(self):
        if self.description is None or self.description == '':
            return None
        try:
            datetime.strptime(self.date, '%Y-%m-%d')
        except ValueError:
            return None
        if self.value is None or self.value < 0.01:
            return None
        if self.expense is None or not isinstance(self.expense, bool):
            return None
        if self.fixed_discounts_ids is None:
            return None
        if not isinstance(self.fixed_discounts_ids, list):
            return None
        return super().save()

    def between(self, initial_date: str, final_date: str):
        try:
            initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
            final_date = datetime.strptime(final_date, '%Y-%m-%d')
        except ValueError:
            return False
        results = []
        for transaction in self.all():
            t_date = datetime.strptime(transaction['date'], '%Y-%m-%d').date()
            if t_date >= initial_date.date() and t_date <= final_date.date():
                results.append(transaction)
        return results

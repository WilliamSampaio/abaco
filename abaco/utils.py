import json
import os
import random
from datetime import datetime, timedelta
from math import ceil

from faker import Faker

from abaco.constants import BASE_DIR_TEMP
from abaco.models import FixedDiscount, Transaction, UserConfig


def validate_json(json_string: str):
    try:
        json.loads(json_string)
    except:
        return False
    return True


def purge_temp_files():
    if os.path.exists(BASE_DIR_TEMP):
        for file in os.listdir(BASE_DIR_TEMP):
            os.remove(os.path.join(BASE_DIR_TEMP, file))


def populate_fake_db():
    try:
        fake = Faker('en_US')
        user_config = UserConfig(fake.name(), 'en_US', 'USD', False)
        if user_config.save() is None:
            return False
        for _ in range(10):
            fixed_discount = FixedDiscount(
                fake.sentence(),
                random.choice(['porcentage', 'value']),
                round(random.uniform(0.1, 10.0), 2),
            )
            if fixed_discount.save() is None:
                return False
        today = datetime.today()
        current_date = today - timedelta(days=90)
        while current_date <= today:
            for _ in range(7, 15):
                transaction = Transaction(
                    fake.sentence(),
                    current_date.strftime('%Y-%m-%d'),
                    round(random.uniform(10.0, 9999.99), 2),
                    random.choice([True, False]),
                    [random.randint(1, 10)],
                )
                if transaction.save() is None:
                    return False
            current_date = current_date + timedelta(days=1)
    except:
        return False
    return True

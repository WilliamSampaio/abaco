import os

APP_NAME = 'Abaco'

COUNTRIES = [
    {'locale': 'en_US', 'emoji': '🇺🇸', 'country': 'English (US)'},
    {'locale': 'pt_BR', 'emoji': '🇧🇷', 'country': 'Portuguese (BR)'},
]

CURRENCIES = [
    {
        'code_iso_4217': 'USD',
        'emoji': '🇺🇸',
        'currency': 'United States dollar',
    },
    {'code_iso_4217': 'BRL', 'emoji': '🇧🇷', 'currency': 'Brazilian real'},
]

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR_TEMP = os.path.join(BASE_DIR, 'static', 'temp')

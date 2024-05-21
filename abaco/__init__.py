from .config import settings
from .database import get_database_uri
from .pages.wallets import page_wallets


def create_app():

    page_wallets()

    import streamlit as st

    st.write(get_database_uri())

    st.write(settings)

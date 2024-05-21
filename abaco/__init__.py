from .config import settings
from .database import get_database_uri


def create_app():

    import streamlit as st

    st.write(get_database_uri())

    st.write(settings)

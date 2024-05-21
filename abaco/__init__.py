from .config import settings


def create_app():

    import streamlit as st

    st.write(settings)

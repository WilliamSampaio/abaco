from .config import settings
from .pages import dashboard, negociacoes, wallets


def create_app():

    import streamlit as st

    page_names_to_funcs = {}

    if 'wallet' not in st.session_state:

        st.set_page_config(
            page_title=settings.APP_NAME,
            page_icon=':abacus:',
            layout='centered',
        )

        wallets.page_wallets()
    else:

        st.set_page_config(
            page_title=settings.APP_NAME, page_icon=':abacus:', layout='wide'
        )

        page_names_to_funcs[dashboard.title] = dashboard.page_dashboard
        page_names_to_funcs[negociacoes.title] = negociacoes.page_negociacoes

        demo_name = st.sidebar.selectbox('Menu', page_names_to_funcs.keys())

        def logout():
            if 'wallet' in st.session_state:
                st.session_state.pop('wallet')

        if 'wallet' in st.session_state:
            st.sidebar.button(
                'Sair da carteira', 'btn_logout', on_click=logout
            )

        page_names_to_funcs[demo_name]()

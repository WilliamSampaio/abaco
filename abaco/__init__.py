from .pages.wallets import page_wallets


def create_app():

    import streamlit as st

    # st.write(get_database_uri())
    # st.write(settings)

    def mapping_demo():
        import streamlit as st

        st.write('# Page 2')

    def plotting_demo():
        import streamlit as st

        st.write('# Page 3')

    def data_frame_demo():
        import streamlit as st

        st.write('# Page 4')

    page_names_to_funcs = {}

    if 'wallet' not in st.session_state:

        page_wallets()
    else:

        page_names_to_funcs['Plotting Demo'] = plotting_demo
        page_names_to_funcs['Mapping Demo'] = mapping_demo
        page_names_to_funcs['DataFrame Demo'] = data_frame_demo

        demo_name = st.sidebar.selectbox('Menu', page_names_to_funcs.keys())

        def logout():
            if 'wallet' in st.session_state:
                st.session_state.pop('wallet')

        if 'wallet' in st.session_state:
            st.sidebar.button(
                'Sair da carteira', 'btn_logout', on_click=logout
            )

        page_names_to_funcs[demo_name]()

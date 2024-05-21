from .pages.wallets import page_wallets


def create_app():

    import streamlit as st

    if 'logged' not in st.session_state:
        st.session_state.logged = False

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

    page_names_to_funcs = {
        'Wallets': page_wallets,
        'Plotting Demo': plotting_demo,
        'Mapping Demo': mapping_demo,
        'DataFrame Demo': data_frame_demo,
    }

    demo_name = st.sidebar.selectbox(
        'Menu',
        page_names_to_funcs.keys(),
        disabled=True if st.session_state.logged is False else False,
    )

    page_names_to_funcs[demo_name]()

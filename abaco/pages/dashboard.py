title = 'Dashboard'


def page_dashboard():

    import streamlit as st

    st.write('# ' + title)
    st.divider()

    st.write(st.session_state.wallet)

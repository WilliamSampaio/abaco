from abaco.dataframes import load_posicoes_df

title = 'Dashboard'


def page_dashboard():

    import streamlit as st

    st.write('# ' + title)
    st.divider()

    row = st.columns([1, 0.5])

    row[0].success('oi')
    row[1].error('oi')

    st.dataframe(load_posicoes_df())

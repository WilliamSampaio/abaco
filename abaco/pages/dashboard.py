import pandas as pd

from abaco.database import Session
from abaco.models import Negociacoes

title = 'Dashboard'


def page_dashboard():

    session = Session()

    import streamlit as st

    def patrimonio_dataframe():
        dataset = []
        negociacoes = (
            session.query(Negociacoes).order_by(Negociacoes.data_pregao).all()
        )
        if len(negociacoes) > 0:
            negociacoes.reverse()
            for negociacao in negociacoes:
                dataset.append(negociacao.to_dict())

        df = pd.DataFrame(dataset)

        # st.write(df)

        # df = df.groupby(['data_pregao', 'movimentacao'])['valor_total'].sum()

        # st.write(df)

        return df

    st.write('# ' + title)
    st.divider()

    row = st.columns([1, 0.5])

    row[0].success('oi')
    row[1].error('oi')

    st.dataframe(patrimonio_dataframe())

from abaco.database import Session
from abaco.functions import render_ticker_links
from abaco.models import Negociacoes

title = 'Negociações'


def page_negociacoes():

    session = Session()

    import streamlit as st

    def load_negociacoes():
        dataset = []
        negociacoes = (
            session.query(Negociacoes).order_by(Negociacoes.data_pregao).all()
        )
        if len(negociacoes) > 0:
            negociacoes.reverse()
            for negociacao in negociacoes:
                data = negociacao.__dict__
                dataset.append(
                    {
                        'Movimentação': data['movimentacao'].name,
                        'Ticker': data['ticker'],
                        'Quantidade': data['quantidade'],
                        'Preço Unitário': data['preco_unitario'],
                        'Valor Total': data['valor_total'],
                        'N° Nota': data['nota'],
                        'Data Pregão': data['data_pregao'].strftime(
                            '%d/%m/%Y'
                        ),
                        'Observação': data['observacao'],
                        'Consultar': render_ticker_links(data['ticker']),
                    }
                )
        return dataset

    st.write('# ' + title)
    st.divider()

    btn_add_negociacao = st.button('Cadastrar Negociação')
    if btn_add_negociacao:
        with st.form('add_negociacao'):
            st.write('## Cadastrar Nova Negociação')

    df = load_negociacoes()

    st.table(df)

    # st.write(load_negociacoes())

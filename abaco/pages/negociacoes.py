from datetime import date

import pandas as pd

from abaco.database import Session
from abaco.functions import render_ticker_links
from abaco.models import MovimentacaoEnum, Negociacoes

title = 'Negociações'


def page_negociacoes():

    session = Session()

    import streamlit as st

    def set_message(alert_func, message):
        st.session_state.message = {
            'func': alert_func,
            'text': message,
        }

    def echo_message():
        if 'message' in st.session_state:
            st.session_state.message['func'](st.session_state.message['text'])
            st.session_state.pop('message')

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

    # btn_add_negociacao = st.button('Cadastrar Negociação')
    # if btn_add_negociacao:

    if 'itens_df' not in st.session_state:
        st.session_state.itens_df = []
    if 'nota' not in st.session_state:
        st.session_state.nota = ''
    if 'data_pregao' not in st.session_state:
        st.session_state.data_pregao = date.today()

    with st.form('add_negociacao', clear_on_submit=True):

        st.write('## Cadastrar Nova Negociação')

        echo_message()

        wallet_id = st.session_state.wallet['id']

        col_nota, col_data_pregao = st.columns(2)
        nota = col_nota.text_input(
            'Nº da Nota', max_chars=20, value=st.session_state.nota
        )
        data_pregao = col_data_pregao.date_input(
            'Data Pregão',
            format='DD/MM/YYYY',
            value=st.session_state.data_pregao,
        )

        col_ticker, col_mov, col_qtd, col_preco = st.columns(4)

        ticker = col_ticker.text_input('Ticker', max_chars=10, value='')
        movimentacao = col_mov.selectbox(
            'Movimentação', MovimentacaoEnum.names()
        )
        quantidade = col_qtd.number_input(
            'Quantidade', step=1, min_value=1, value=1
        )
        preco_unitario = col_preco.number_input(
            'Preço Unitário', min_value=0.00, format='%0.2f', value=0.00
        )

        observacao = st.text_input('Observação', max_chars=100, value='')

        submit_add_negociacao = st.form_submit_button('Adicionar')

        if submit_add_negociacao:

            st.session_state.nota = nota
            st.session_state.data_pregao = data_pregao

            if ticker == '':
                set_message(st.error, 'Ticker não informado!')
                st.rerun()

            st.session_state.itens_df.append(
                {
                    'wallet_id': wallet_id,
                    'nota': nota,
                    'data_pregao': data_pregao,
                    'observacao': observacao,
                    'ticker': ticker,
                    'movimentacao': movimentacao,
                    'quantidade': quantidade,
                    'preco_unitario': preco_unitario,
                    'valor_total': quantidade * preco_unitario,
                    'selecionado': False,
                }
            )

            set_message(st.success, 'Item adicionado!')
            st.rerun()

    if len(st.session_state.itens_df) > 0:

        df = pd.DataFrame(st.session_state.itens_df)

        df = df[
            [
                'ticker',
                'movimentacao',
                'quantidade',
                'preco_unitario',
                'valor_total',
                'nota',
                'data_pregao',
                'observacao',
                'selecionado',
            ]
        ]

        df = df.rename(
            columns={
                'ticker': 'Ticker',
                'movimentacao': 'Movimentação',
                'quantidade': 'Quantidade',
                'preco_unitario': 'Preço Unitário',
                'valor_total': 'Total',
                'nota': 'Nº Nota',
                'data_pregao': 'Data Pregão',
                'observacao': 'Observação',
                'selecionado': 'Selecionado',
            }
        )

        table = st.data_editor(df, width=2000, hide_index=True)

        col_btn_cadastrar, col_btn_remover_itens = st.columns(2)

        btn_remover_itens = col_btn_remover_itens.button(
            'Remover Itens Selecionados'
        )
        # btn_cadastrar = col_btn_cadastrar.button('Cadastrar Negociação')

        if btn_remover_itens:
            lista = table.query('Selecionado==True')['Ticker'].to_list()
            st.write(lista)

    # st.write(load_negociacoes())

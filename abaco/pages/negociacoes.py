from datetime import date, datetime

import pandas as pd

from abaco.database import Session
from abaco.functions import moeda, render_ticker_links
from abaco.models import MovimentacaoEnum, Negociacoes
from abaco.yfinance import get_stock_info

title = 'Negociações'


def page_negociacoes():

    session = Session()

    import streamlit as st

    if 'action' not in st.session_state:
        st.session_state.action = 'negociacoes.index'

    def btn_goto_index_form_callback():
        st.session_state.action = 'negociacoes.index'
        st.rerun()

    def btn_goto_add_form_callback():
        st.session_state.action = 'negociacoes.add'
        st.rerun()

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
                dataset.append(negociacao.__dict__)
        return dataset

    st.write('# ' + title)
    st.divider()

    def index():

        echo_message()

        st.button(
            'Cadastrar Negociação',
            'btn_goto_add_form',
            on_click=btn_goto_add_form_callback,
        )

        st.divider()

        c = st.container()

        td1, td2, td3, td4, td5, td6, td7, td8 = c.columns(8)

        td1.write('**Movimentação**')
        td2.write('**Ticker**')
        td3.write('**Quantidade**')
        td4.write('**Preço Unitário**')
        td5.write('**Valor Total**')
        td6.write('**Data**')
        td7.write('**Observação**')
        td8.write('**Consultar**')

        for item in load_negociacoes():

            td1, td2, td3, td4, td5, td6, td7, td8 = c.columns(8)

            if item['movimentacao'].name == 'Compra':
                td1.html(
                    '<span style="color: green"><b>{}</b></span>'.format(
                        item['movimentacao'].name
                    )
                )
            else:
                td1.html(
                    '<span style="color: red"><b>{}</b></span>'.format(
                        item['movimentacao'].name
                    )
                )

            td2.html(
                '<img src="{}" style="width: 20px;"> {}'.format(
                    get_stock_info(item['ticker'])['companyIcon'],
                    item['ticker'],
                )
            )

            td3.write('**{}**'.format(item['quantidade']))
            td4.write('**R$ {}**'.format(moeda(item['preco_unitario'])))
            td5.write('**R$ {}**'.format(moeda(item['valor_total'])))
            td6.write(
                '**{}**'.format(item['data_pregao'].strftime('%d/%m/%Y'))
            )
            td7.write(item['observacao'])
            td8.markdown(
                render_ticker_links(item['ticker']), unsafe_allow_html=True
            )

    def add():

        btn_voltar = st.button('Voltar')

        if btn_voltar:

            if 'itens_df' in st.session_state:
                st.session_state.pop('itens_df')
            if 'nota' in st.session_state:
                st.session_state.pop('nota')
            if 'data_pregao' in st.session_state:
                st.session_state.pop('data_pregao')
            if 'message' in st.session_state:
                st.session_state.pop('message')

            btn_goto_index_form_callback()

        if 'itens_df' not in st.session_state:
            st.session_state.itens_df = []
        if 'nota' not in st.session_state:
            st.session_state.nota = ''
        if 'data_pregao' not in st.session_state:
            st.session_state.data_pregao = date.today()

        with st.form('add_negociacao', clear_on_submit=True):

            st.write('## Cadastrar Nova Negociação')

            echo_message()

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

            btn_add_form_submit = st.form_submit_button('Adicionar')

        if btn_add_form_submit:

            st.session_state.nota = nota
            st.session_state.data_pregao = data_pregao

            if ticker == '':
                set_message(st.error, 'Ticker não informado!')
                btn_goto_add_form_callback()

            stock_info = get_stock_info(ticker)

            if stock_info is False:
                set_message(st.error, 'Ticker não listado na B3!')
                btn_goto_add_form_callback()

            st.session_state.itens_df.append(
                {
                    'icon': stock_info['companyIcon'],
                    'nota': nota,
                    'data_pregao': data_pregao,
                    'observacao': observacao,
                    'ticker': ticker.upper(),
                    'movimentacao': movimentacao,
                    'quantidade': quantidade,
                    'preco_unitario': preco_unitario,
                    'valor_total': quantidade * preco_unitario,
                    'selecionado': False,
                }
            )

            set_message(st.success, 'Item adicionado!')
            btn_goto_add_form_callback()

        if len(st.session_state.itens_df) > 0:

            df = pd.DataFrame(st.session_state.itens_df)

            df = df[
                [
                    'icon',
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

            table = st.data_editor(
                df,
                width=2000,
                hide_index=True,
                column_config={'icon': st.column_config.ImageColumn(label='')},
            )

            (
                col_btn_cadastrar,
                col_btn_remover_itens,
            ) = st.columns(2)

            btn_remover_itens = col_btn_remover_itens.button(
                'Remover Itens Selecionados'
            )
            btn_cadastrar = col_btn_cadastrar.button('Cadastrar Negociação')

            if btn_remover_itens:
                lista = table.query('Selecionado==True').index.to_list()
                for index in sorted(lista, reverse=True):
                    del st.session_state.itens_df[index]
                btn_goto_add_form_callback()

            if btn_cadastrar:
                data = []
                for item in st.session_state.itens_df:
                    data.append(
                        Negociacoes(
                            wallet_id=st.session_state.wallet['id'],
                            ticker=item['ticker'],
                            movimentacao=item['movimentacao'],
                            quantidade=item['quantidade'],
                            preco_unitario=item['preco_unitario'],
                            valor_total=item['valor_total'],
                            nota=item['nota'],
                            data_pregao=item['data_pregao'],
                            observacao=item['observacao'],
                            created_at=datetime.now(),
                        )
                    )
                session.add_all(data)
                session.commit()

                st.session_state.pop('itens_df')
                st.session_state.pop('nota')
                st.session_state.pop('data_pregao')

                set_message(st.success, 'Negociação cadastrada com sucesso!')
                btn_goto_index_form_callback()

    if st.session_state.action == 'negociacoes.index':
        index()

    if st.session_state.action == 'negociacoes.add':
        add()

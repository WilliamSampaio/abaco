from datetime import date, datetime

from abaco.database import Session
from abaco.functions import moeda, render_ticker_links
from abaco.models import MovimentacaoEnum, Negociacoes
from abaco.yfinance import get_stock_info

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
                dataset.append(negociacao.__dict__)
        return dataset

    def remove_item(index: int):
        if 'itens_df' in st.session_state:
            if len(st.session_state.itens_df) > 0:
                del st.session_state.itens_df[index]

    if 'itens_df' not in st.session_state:
        st.session_state.itens_df = []
    if 'nota' not in st.session_state:
        st.session_state.nota = ''
    if 'data_pregao' not in st.session_state:
        st.session_state.data_pregao = date.today()

    st.write('# ' + title)
    st.divider()

    with st.expander('Cadastrar Negociação'):

        st.write('## Cadastrar Nova Negociação')

        echo_message()

        row = st.columns(2)
        nota = row[0].text_input(
            'Nº da Nota', max_chars=20, value=st.session_state.nota
        )
        data_pregao = row[1].date_input(
            'Data Pregão',
            format='DD/MM/YYYY',
            value=st.session_state.data_pregao,
        )

        row = st.columns(4)

        ticker = row[0].text_input('Ticker', max_chars=10, value='')
        movimentacao = row[1].selectbox(
            'Movimentação', MovimentacaoEnum.names()
        )
        quantidade = row[2].number_input(
            'Quantidade', step=1, min_value=1, value=1
        )
        preco_unitario = row[3].number_input(
            'Preço Unitário', min_value=0.00, format='%0.2f', value=0.00
        )

        observacao = st.text_input('Observação', max_chars=100, value='')

        if st.button('Adicionar'):

            st.session_state.nota = nota
            st.session_state.data_pregao = data_pregao

            if ticker == '':
                set_message(st.error, 'Ticker não informado!')
                st.rerun()

            stock_info = get_stock_info(ticker)

            if stock_info is False:
                set_message(st.error, 'Ticker não listado na B3!')
                st.rerun()

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
            st.rerun()

        if len(st.session_state.itens_df) > 0:

            c = st.container()

            headers = c.columns(9, gap='small')

            headers[0].write('**Movimentação**')
            headers[1].write('**Ticker**')
            headers[2].write('**Quantidade**')
            headers[3].write('**Preço Unitário**')
            headers[4].write('**Valor Total**')
            headers[5].write('**Nº Nota**')
            headers[6].write('**Data Pregão**')
            headers[7].write('**Observação**')

            for i in range(0, len(st.session_state.itens_df)):

                item = st.session_state.itens_df[i]
                row = c.columns(9, gap='small')

                if item['movimentacao'] == 'Compra':
                    row[0].html(
                        '<span style="color: green"><b>{}</b></span>'.format(
                            item['movimentacao']
                        )
                    )
                elif item['movimentacao'] == 'Venda':
                    row[0].html(
                        '<span style="color: red"><b>{}</b></span>'.format(
                            item['movimentacao']
                        )
                    )
                elif item['movimentacao'] == 'Bonificacao':
                    row[0].html(
                        '<span style="color: yellow"><b>Bonificação</b></span>'
                    )

                row[1].html(
                    '<img src="{}" style="width: 20px;"> {}'.format(
                        get_stock_info(item['ticker'])['companyIcon'],
                        item['ticker'],
                    )
                )

                row[2].write('**{}**'.format(item['quantidade']))
                row[3].write('**R$ {}**'.format(moeda(item['preco_unitario'])))
                row[4].write('**R$ {}**'.format(moeda(item['valor_total'])))
                row[5].write('**{}**'.format(item['nota']))
                row[6].write(
                    '**{}**'.format(item['data_pregao'].strftime('%d/%m/%Y'))
                )
                row[7].write(item['observacao'])
                row[8].button('🗑️', key=i, on_click=remove_item, args=[i])

            st.write('')

            if st.button('Cadastrar Negociação'):

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
                st.rerun()

    st.divider()

    c = st.container()

    row = c.columns(9, gap='small')

    row[0].write('**Movimentação**')
    row[1].write('**Ticker**')
    row[2].write('**Quantidade**')
    row[3].write('**Preço Unitário**')
    row[4].write('**Valor Total**')
    row[5].write('**Data**')
    row[6].write('**Observação**')
    row[7].write('**Consultar**')

    for item in load_negociacoes():

        row = c.columns(9, gap='small')

        if item['movimentacao'].name == 'Compra':
            row[0].html(
                '<span style="color: green"><b>{}</b></span>'.format(
                    item['movimentacao'].name
                )
            )
        elif item['movimentacao'].name == 'Venda':
            row[0].html(
                '<span style="color: red"><b>{}</b></span>'.format(
                    item['movimentacao'].name
                )
            )
        elif item['movimentacao'].name == 'Bonificacao':
            row[0].html(
                '<span style="color: yellow"><b>Bonificação</b></span>'
            )

        row[1].html(
            '<img src="{}" style="width: 20px;"> {}'.format(
                get_stock_info(item['ticker'])['companyIcon'],
                item['ticker'],
            )
        )

        row[2].write('**{}**'.format(item['quantidade']))
        row[3].write('**R$ {}**'.format(moeda(item['preco_unitario'])))
        row[4].write('**R$ {}**'.format(moeda(item['valor_total'])))
        row[5].write('**{}**'.format(item['data_pregao'].strftime('%d/%m/%Y')))
        row[6].write(item['observacao'])
        row[7].markdown(
            render_ticker_links(item['ticker']), unsafe_allow_html=True
        )
        row[8].button(
            '🗑️',
            key=f'id_{item["id"]}',
            on_click=print,
            args=[str(item['id'])],
        )

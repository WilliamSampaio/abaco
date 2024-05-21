from hashlib import md5

from abaco.models import Wallet

from ..database import Session


def page_wallets():

    session = Session()

    import streamlit as st

    if 'action' not in st.session_state:
        st.session_state.action = 'wallets.access'

    from ..config import settings

    def btn_goto_access_form_callback():
        st.session_state.action = 'wallets.access'

    def btn_goto_add_form_callback():
        st.session_state.action = 'wallets.add'

    st.header(f':abacus: Bem-vindo ao {settings.APP_NAME}!')

    def access():

        if 'message' in st.session_state:
            st.session_state.message['func'](st.session_state.message['text'])
            st.session_state.pop('message')

        with st.form('wallet_access_form', True):

            st.header('Acessar carteira')

            options = []
            wallets = session.query(Wallet).all()
            if len(wallets) > 0:
                for wallet in wallets:
                    data = wallet.__dict__
                    options.append(
                        '. '.join([str(data['id']), data['description']])
                    )

            description = st.selectbox('Selecione a carteira', options)
            password = st.text_input('Senha de acesso', type='password')

            btn_wallet_access_form_submit = st.form_submit_button('Acessar')

            if btn_wallet_access_form_submit:

                if description is None or password == '':
                    st.session_state.message = {
                        'func': st.error,
                        'text': 'Carteira ou senha não informada!',
                    }
                else:
                    id = str(description).split('. ')[0]
                    m = md5()
                    m.update(password.encode('utf-8'))
                    pass_md5 = m.hexdigest()
                    wallet = session.query(Wallet).get(int(id))

                    if not wallet or wallet.__dict__['password'] != pass_md5:
                        st.session_state.message = {
                            'func': st.error,
                            'text': 'Carteira não existe ou senha inválida!',
                        }
                    else:
                        st.session_state.wallet = {
                            'id': id,
                            'description': wallet.__dict__['description'],
                        }
                        st.session_state.pop('action')
                        st.rerun()

        st.divider()

        st.button(
            'Add carteira',
            'btn_goto_add_form',
            on_click=btn_goto_add_form_callback,
        )

    def add():

        if 'message' in st.session_state:
            st.session_state.message['func'](st.session_state.message['text'])
            st.session_state.pop('message')

        with st.form('wallet_add_form', True):

            st.header('Cadastrar nova carteira')

            description = st.text_input(
                'Descrição', type='default', max_chars=50
            )
            password1 = st.text_input('Senha de acesso', type='password')
            password2 = st.text_input('Repita a senha', type='password')

            btn_wallet_add_form_submit = st.form_submit_button('Salvar')

            if btn_wallet_add_form_submit:

                if (
                    password1 != password2
                    or password1 == ''
                    or description == ''
                ):
                    st.session_state.message = {
                        'func': st.error,
                        'text': 'Descrição vazia ou senhas não coincidem!',
                    }
                else:
                    m = md5()
                    m.update(password1.encode('utf-8'))
                    pass_md5 = m.hexdigest()

                    wallet = Wallet(description=description, password=pass_md5)
                    session.add(wallet)
                    session.commit()

                    st.session_state.message = {
                        'func': st.success,
                        'text': 'Carteira cadastrada com sucesso!',
                    }

                    btn_goto_access_form_callback()
                    st.rerun()

        st.divider()

        st.button(
            'Voltar',
            'btn_goto_access_form',
            on_click=btn_goto_access_form_callback,
        )

    if st.session_state.action == 'wallets.access':
        access()

    if st.session_state.action == 'wallets.add':
        add()

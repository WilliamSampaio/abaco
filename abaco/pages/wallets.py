from hashlib import md5

from abaco.models import Wallet

from ..config import settings
from ..database import Session

title = 'Acessar carteira'


def page_wallets():

    session = Session()

    import streamlit as st

    if 'action' not in st.session_state:
        st.session_state.action = 'wallets.access'

    def btn_goto_access_form_callback():
        st.session_state.action = 'wallets.access'
        st.rerun()

    def btn_goto_add_form_callback():
        st.session_state.action = 'wallets.add'
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

    st.write(f'# :abacus: Bem-vindo ao {settings.APP_NAME}!')

    def access():

        echo_message()

        with st.form('access_form', True):

            st.write('## ' + title)

            if settings.ENV_FOR_DYNACONF == 'DEVELOPMENT':
                st.info('- Tio Patinhas Wallet **senha**: ```123``` (Dev)')

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

            btn_access_form_submit = st.form_submit_button('Acessar')

            if btn_access_form_submit:

                if description is None or password == '':
                    set_message(st.error, 'Carteira ou senha não informada!')
                    btn_goto_access_form_callback()

                id = str(description).split('. ')[0]
                m = md5()
                m.update(password.encode('utf-8'))
                pass_md5 = m.hexdigest()
                wallet = session.query(Wallet).get(int(id))

                if not wallet or wallet.__dict__['password'] != pass_md5:
                    set_message(
                        st.error, 'Carteira não existe ou senha inválida!'
                    )
                    btn_goto_access_form_callback()

                st.session_state.wallet = {
                    'id': wallet.__dict__['id'],
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

        echo_message()

        with st.form('add_form', True):

            st.header('Cadastrar nova carteira')

            description = st.text_input(
                'Descrição', type='default', max_chars=50
            )
            password1 = st.text_input('Senha de acesso', type='password')
            password2 = st.text_input('Repita a senha', type='password')

            btn_add_form_submit = st.form_submit_button('Salvar')

        if btn_add_form_submit:

            if password1 != password2 or password1 == '' or description == '':
                set_message(
                    st.error, 'Descrição vazia ou senhas não coincidem!'
                )
                btn_goto_add_form_callback()

            m = md5()
            m.update(password1.encode('utf-8'))
            pass_md5 = m.hexdigest()

            wallet = Wallet(description=description, password=pass_md5)
            session.add(wallet)
            session.commit()

            set_message(st.success, 'Carteira cadastrada com sucesso!')
            btn_goto_access_form_callback()

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

    # debug
    # st.write(st.session_state)

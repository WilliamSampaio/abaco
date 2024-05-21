def page_wallets():

    import streamlit as st

    if 'action' not in st.session_state:
        st.session_state.action = 'wallets.access'

    from ..config import settings

    st.header(f':abacus: Bem-vindo ao {settings.APP_NAME}!')

    def access():
        with st.form('wallet_access_form', True):

            st.header('Acessar carteira')

            id = st.selectbox('Selecione a carteira', ['1', '2'])
            password = st.text_input('Senha de acesso', type='password')

            st.form_submit_button('Acessar')
        st.divider()

        def btn_goto_add_form_callback():
            st.session_state.action = 'wallets.add'

        st.button(
            'Add carteira',
            'btn_goto_add_form',
            on_click=btn_goto_add_form_callback,
        )

    def add():
        with st.form('wallet_add_form', True):

            st.header('Cadastrar nova carteira')

            description = st.text_input(
                'Descrição', type='default', max_chars=50
            )
            password1 = st.text_input('Senha de acesso', type='password')
            password2 = st.text_input('Repita a senha', type='password')

            st.form_submit_button('Salvar')

        st.divider()

        def btn_goto_access_form_callback():
            st.session_state.action = 'wallets.access'

        st.button(
            'Voltar',
            'btn_goto_access_form',
            on_click=btn_goto_access_form_callback,
        )

    if st.session_state.action == 'wallets.access':
        access()

    if st.session_state.action == 'wallets.add':
        add()

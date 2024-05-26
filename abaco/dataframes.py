import numpy as np
import pandas as pd

from abaco.database import Session
from abaco.models import Negociacoes
from abaco.yfinance import get_stock_info

session = Session()


def load_negociacoes_df():
    dataset = []
    negociacoes = (
        session.query(Negociacoes).order_by(Negociacoes.data_pregao).all()
    )
    if len(negociacoes) > 0:
        for negociacao in negociacoes:
            dataset.append(negociacao.to_dict())

    df = pd.DataFrame(dataset)

    return df


def load_posicoes_df():
    df = load_negociacoes_df()
    df = df.drop(
        columns=[
            'id',
            'wallet_id',
            'preco_unitario',
            'nota',
            'data_pregao',
            'observacao',
            'created_at',
        ],
        axis=1,
    )
    df['movimentacao'] = ['add' if m.name != 'Venda' else 'sub' for m in df['movimentacao']]

    df = df.groupby(['ticker', 'movimentacao']).sum().reset_index()

    df['tipo_ativo'] = [
        get_stock_info(ticker)['abaco_tipo_ativo'].upper() for ticker in df['ticker']
    ]

    return df

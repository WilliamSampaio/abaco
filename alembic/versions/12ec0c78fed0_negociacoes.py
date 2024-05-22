"""negociacoes

Revision ID: 12ec0c78fed0
Revises: 7ee0bfffcd1d
Create Date: 2024-05-21 22:16:46.361907
"""
import random
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa

from abaco.config import settings
from abaco.models import MovimentacaoEnum
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '12ec0c78fed0'
down_revision: Union[str, None] = '7ee0bfffcd1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tickers = [
    'AFHI11',
    'AURE3',
    'ALZR11',
    'SAPR11',
    'BCFF11',
    'CMIG3',
    'BRCO11',
    'VALE3',
    'BTCI11',
    'VLID3',
    'BTLG11',
    'BBAS3',
    'CPTS11',
    'PFRM3',
    'CVBI11',
    'RAIZ4',
    'GARE11',
    'RANI3',
    'GGRC11',
    'GGBR4',
    'HABT11',
    'SAPR4',
    'HFOF11',
    'JALL3',
    'HGBS11',
    'ROMI3',
    'HGCR11',
    'SANB4',
]


def upgrade() -> None:

    tbl_negociacoes = op.create_table(
        'negociacoes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'wallet_id', sa.Integer, sa.ForeignKey('wallet.id'), nullable=False
        ),
        sa.Column('ticker', sa.String(10), nullable=False),
        sa.Column('movimentacao', sa.Enum(MovimentacaoEnum), nullable=False),
        sa.Column('quantidade', sa.Integer, nullable=False, default=1),
        sa.Column(
            'preco_unitario',
            sa.Float(precision=2),
            nullable=False,
            default=0.0,
        ),
        sa.Column(
            'valor_total', sa.Float(precision=2), nullable=False, default=0.0
        ),
        sa.Column('nota', sa.String(20), nullable=False, default=''),
        sa.Column('data_pregao', sa.Date(), nullable=False),
        sa.Column('observacao', sa.String(100), nullable=False, default=''),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    if settings.ENV_FOR_DYNACONF == 'DEVELOPMENT':

        operacoes_compra = []

        for nota in range(1, 11):
            for qtd in range(5, random.randint(5, 10)):

                str_date = '2023-{}-{}'.format(
                    str(nota).zfill(2), str(qtd).zfill(2)
                )

                operacao = {'wallet_id': 1}
                operacao['ticker'] = random.choice(tickers)
                operacao['movimentacao'] = 'Compra'
                operacao['quantidade'] = random.randint(100, 300)
                operacao['preco_unitario'] = round(
                    random.uniform(9.99, 99.99), 2
                )
                operacao['valor_total'] = (
                    operacao['preco_unitario'] * operacao['quantidade']
                )
                operacao['nota'] = str(nota).zfill(10)
                operacao['data_pregao'] = datetime.strptime(
                    str_date, '%Y-%m-%d'
                ).date()
                operacao['created_at'] = datetime.strptime(
                    str_date, '%Y-%m-%d'
                )
                operacoes_compra.append(operacao)

        op.bulk_insert(tbl_negociacoes, operacoes_compra)


def downgrade() -> None:
    op.drop_table('negociacoes')

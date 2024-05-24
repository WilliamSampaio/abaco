"""negociacoes

Revision ID: 12ec0c78fed0
Revises: 7ee0bfffcd1d
Create Date: 2024-05-21 22:16:46.361907
"""
import os
from datetime import datetime
from typing import Sequence, Union

import numpy as np
import pandas as pd
import sqlalchemy as sa

from abaco.config import settings
from abaco.models import MovimentacaoEnum
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '12ec0c78fed0'
down_revision: Union[str, None] = '7ee0bfffcd1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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

        data = pd.read_excel(
            os.path.join(os.getcwd(), 'data', 'wallet.ods'), engine='odf'
        )

        data.insert(0, 'wallet_id', 1, True)
        data.insert(9, 'created_at', datetime.now(), True)
        data.movimentacao = data.movimentacao.replace({np.nan: None})
        data.nota = data.nota.replace({np.nan: ''})
        data.observacao = data.observacao.replace({np.nan: ''})

        op.bulk_insert(tbl_negociacoes, data.to_dict('records'))


def downgrade() -> None:
    op.drop_table('negociacoes')

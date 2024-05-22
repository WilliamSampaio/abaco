"""create wallet table

Revision ID: 7ee0bfffcd1d
Revises:
Create Date: 2024-05-21 03:02:55.767657
"""

from datetime import datetime
from hashlib import md5
from typing import Sequence, Union

import sqlalchemy as sa

from abaco.config import settings
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7ee0bfffcd1d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    tbl_wallet = op.create_table(
        'wallet',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String(50), nullable=False),
        sa.Column('password', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    if settings.ENV_FOR_DYNACONF == 'DEVELOPMENT':

        m = md5()
        m.update('123'.encode('utf-8'))
        pass_md5 = m.hexdigest()

        op.bulk_insert(
            tbl_wallet,
            [
                {
                    'description': 'Tio Patinhas Wallet',
                    'password': pass_md5,
                    'created_at': datetime.now(),
                }
            ],
        )


def downgrade():
    op.drop_table('wallet')

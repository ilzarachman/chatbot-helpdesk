"""add conversation uuid

Revision ID: 994762c3c8fb
Revises: 6a1b3248e103
Create Date: 2024-07-16 00:27:21.103497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '994762c3c8fb'
down_revision: Union[str, None] = '6a1b3248e103'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conversations', sa.Column('uuid', sa.String(length=255), nullable=False))
    op.create_unique_constraint(None, 'conversations', ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'conversations', type_='unique')
    op.drop_column('conversations', 'uuid')
    # ### end Alembic commands ###
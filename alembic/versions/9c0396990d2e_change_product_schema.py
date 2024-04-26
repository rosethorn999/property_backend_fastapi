"""Change product schema

Revision ID: 9c0396990d2e
Revises: 7e332a1d4af2
Create Date: 2024-04-25 16:49:31.862527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c0396990d2e'
down_revision: Union[str, None] = '7e332a1d4af2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('picture', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'picture')
    # ### end Alembic commands ###

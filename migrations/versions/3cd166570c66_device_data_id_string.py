"""device data id string

Revision ID: 3cd166570c66
Revises: d3d15f7b1fe1
Create Date: 2024-11-20 17:44:45.014168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cd166570c66'
down_revision: Union[str, None] = 'd3d15f7b1fe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device_data', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device_data', 'id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###

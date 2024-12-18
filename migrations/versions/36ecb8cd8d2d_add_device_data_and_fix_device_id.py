"""add device data and fix device id

Revision ID: 36ecb8cd8d2d
Revises: a1e767823b34
Create Date: 2024-11-17 19:44:34.093905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36ecb8cd8d2d'
down_revision: Union[str, None] = 'a1e767823b34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.String(), nullable=False),
    sa.Column('timestamp', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_data_id'), 'device_data', ['id'], unique=False)
    op.alter_column('devices', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('devices', 'id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_index(op.f('ix_device_data_id'), table_name='device_data')
    op.drop_table('device_data')
    # ### end Alembic commands ###

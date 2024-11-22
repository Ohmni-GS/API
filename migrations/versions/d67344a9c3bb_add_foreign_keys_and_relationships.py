"""Add foreign keys and relationships

Revision ID: d67344a9c3bb
Revises: 60824e30c0e6
Create Date: 2024-11-20 14:55:06.048662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd67344a9c3bb'
down_revision: Union[str, None] = '60824e30c0e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('communities', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('device_data', 'device_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    op.create_foreign_key(None, 'device_data', 'devices', ['device_id'], ['id'])
    op.alter_column('devices', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_foreign_key(None, 'devices', 'users', ['owner'], ['id'])
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_foreign_key(None, 'users', 'communities', ['community_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'devices', type_='foreignkey')
    op.alter_column('devices', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'device_data', type_='foreignkey')
    op.alter_column('device_data', 'device_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('communities', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
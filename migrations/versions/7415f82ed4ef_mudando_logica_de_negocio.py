"""mudando logica de negocio

Revision ID: 7415f82ed4ef
Revises: 36ecb8cd8d2d
Create Date: 2024-11-18 21:56:39.795021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7415f82ed4ef'
down_revision: Union[str, None] = '36ecb8cd8d2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

"""verify database

Revision ID: 8d9e812d01c3
Revises: 3a30884cf878
Create Date: 2025-02-21 04:04:40.450986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
#______________________________________________________________________________
#
# à ajouter avant de faire alembic upgrade head
#______________________________________________________________________________
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8d9e812d01c3'
down_revision: Union[str, None] = '3a30884cf878'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

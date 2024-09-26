"""update users table

Revision ID: ec2648c45289
Revises: fc85c1f5b318
Create Date: 2024-09-25 10:35:40.570845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec2648c45289'
down_revision: Union[str, None] = 'fc85c1f5b318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=200), nullable=False))
    op.drop_column('users', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('title', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
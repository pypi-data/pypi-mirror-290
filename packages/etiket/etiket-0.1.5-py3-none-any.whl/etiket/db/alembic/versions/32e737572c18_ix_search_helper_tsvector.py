"""'ix_search_helper_tsvector'

Revision ID: 32e737572c18
Revises: 675fac985b76
Create Date: 2023-10-15 21:21:23.872320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32e737572c18'
down_revision: Union[str, None] = '675fac985b76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy import text, func
from alembic import op

def upgrade():
    # TODO: only if postrges
    op.create_index(
        'ix_search_helper_tsvector', 
        'datasets', 
        [func.to_tsvector(text("'simple'"), text('search_helper'))], 
        postgresql_using='gin',
        if_not_exists=True
    )

def downgrade():
    op.drop_index('ix_search_helper_tsvector', table_name='datasets', if_exists=True)

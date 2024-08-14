"""Add index on scope_id column

Revision ID: 675fac985b76
Revises: dd655830f014
Create Date: 2023-10-14 17:51:58.835011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


#TODO is this needed? this index is not added not sure why check in psql \di

# revision identifiers, used by Alembic.
revision: str = '675fac985b76'
down_revision: Union[str, None] = 'dd655830f014'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create an index on the 'scope_id' column of the 'datasets' table
    op.create_index('idx_scope_id', 'datasets', ['scope_id'], if_not_exists=True)

def downgrade():
    # remove the index
    op.drop_index('idx_scope_id', table_name='datasets', if_exists=True)

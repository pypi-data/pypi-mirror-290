"""Add index to dataset_id column in files table

Revision ID: 12679c2891d7
Revises: 0ba314714736
Create Date: 2024-04-17 19:17:46.280047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12679c2891d7'
down_revision: Union[str, None] = '0ba314714736'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create an index index to dataset_id column in files table
    op.create_index('ix_dataset_id', 'files', ['dataset_id'], if_not_exists=True)


def downgrade() -> None:
    op.drop_index('ix_dataset_id', table_name='files', if_exists=True)


"""update updating types

Revision ID: c14b4c83c043
Revises: 041b93186c29
Create Date: 2023-11-03 15:20:33.492493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c14b4c83c043'
down_revision: Union[str, None] = '041b93186c29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("ALTER TYPE filetype RENAME TO filetype_old")
    op.execute("CREATE TYPE filetype AS ENUM('HDF5', 'HDF5_NETCDF', 'NDARRAY', 'JSON', 'TEXT', 'UNKNOWN')")
    op.execute("ALTER TABLE files ALTER COLUMN type TYPE filetype USING type::text::filetype")


def downgrade() -> None:
    op.execute("ALTER TYPE filetype_old RENAME TO filetype")
    op.execute("ALTER TABLE files ALTER COLUMN type TYPE filetype")
    op.execute("DROP TYPE filetype_old")

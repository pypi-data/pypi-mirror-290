"""version 0.2.0 database schema

Revision ID: dd655830f014
Revises: 
Create Date: 2023-10-10 13:03:59.868756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd655830f014'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('schemas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('schema', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('disable_on', sa.DateTime(), nullable=True),
    sa.Column('user_type', sa.Enum('admin', 'scope_admin', 'standard_user', 'superuser', name='usertype'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('scopes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=False),
    sa.Column('schema_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['schema_id'], ['schemas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('tokens',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('token_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('dataset_attr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scope_id'], ['scopes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key', 'value', 'scope_id')
    )
    op.create_index(op.f('ix_dataset_attr_scope_id'), 'dataset_attr', ['scope_id'], unique=False)
    op.create_table('datasets',
    sa.Column('id', sa.BigInteger().with_variant(sa.BIGINT(), 'postgresql').with_variant(sa.INTEGER(), 'sqlite'), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('alt_uid', sa.String(), nullable=True),
    sa.Column('collected', sa.TIMESTAMP(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.Column('creator', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('keywords', sa.JSON(), nullable=False),
    sa.Column('search_helper', sa.String(), nullable=False),
    sa.Column('ranking', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scope_id'], ['scopes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid', 'alt_uid')
    )
    op.create_index(op.f('ix_datasets_alt_uid'), 'datasets', ['alt_uid'], unique=False)
    op.create_index(op.f('ix_datasets_uuid'), 'datasets', ['uuid'], unique=False)
    op.create_table('scope_user_link',
    sa.Column('scope', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scope'], ['scopes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('scope', 'user_id')
    )
    op.create_table('ds_attr_link',
    sa.Column('dataset_id', sa.BigInteger().with_variant(sa.BIGINT(), 'postgresql').with_variant(sa.INTEGER(), 'sqlite'), nullable=False),
    sa.Column('dataset_attr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_attr_id'], ['dataset_attr.id'], ),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
    sa.PrimaryKeyConstraint('dataset_id', 'dataset_attr_id')
    )
    op.create_table('files',
    sa.Column('id', sa.BigInteger().with_variant(sa.BIGINT(), 'postgresql').with_variant(sa.INTEGER(), 'sqlite'), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('creator', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('notdefined', 'src_code', 'preview', 'raw', 'derived', 'configuration', name='filetype'), nullable=False),
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.BigInteger().with_variant(sa.BIGINT(), 'postgresql').with_variant(sa.INTEGER(), 'sqlite'), nullable=False),
    sa.Column('collected', sa.DateTime(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('etag', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('unavailable', 'pending', 'available', 'secured', name='filestatus'), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('s3_bucket', sa.String(), nullable=True),
    sa.Column('s3_key', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
    sa.ForeignKeyConstraint(['scope_id'], ['scopes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    op.drop_table('ds_attr_link')
    op.drop_table('scope_user_link')
    op.drop_index(op.f('ix_datasets_uuid'), table_name='datasets')
    op.drop_index(op.f('ix_datasets_alt_uid'), table_name='datasets')
    op.drop_table('datasets')
    op.drop_index(op.f('ix_dataset_attr_scope_id'), table_name='dataset_attr')
    op.drop_table('dataset_attr')
    op.drop_table('tokens')
    op.drop_table('scopes')
    op.drop_table('users')
    op.drop_table('schemas')
    # ### end Alembic commands ###

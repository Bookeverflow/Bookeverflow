"""empty message

Revision ID: d77026b1a8e5
Revises: ed8d29f0e0ea
Create Date: 2017-01-22 01:09:22.882516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd77026b1a8e5'
down_revision = 'ed8d29f0e0ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deal_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('record', sa.Integer(), nullable=True),
    sa.Column('requester', sa.Integer(), nullable=True),
    sa.Column('dealer', sa.Integer(), nullable=True),
    sa.Column('processed', sa.Boolean(), nullable=False),
    sa.Column('accepted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['dealer'], ['user.id'], ),
    sa.ForeignKeyConstraint(['record'], ['book_record.id'], ),
    sa.ForeignKeyConstraint(['requester'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('sqlite_stat1')
    op.drop_table('sqlite_stat4')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sqlite_stat4',
    sa.Column('tbl', sa.NullType(), nullable=True),
    sa.Column('idx', sa.NullType(), nullable=True),
    sa.Column('neq', sa.NullType(), nullable=True),
    sa.Column('nlt', sa.NullType(), nullable=True),
    sa.Column('ndlt', sa.NullType(), nullable=True),
    sa.Column('sample', sa.NullType(), nullable=True)
    )
    op.create_table('sqlite_stat1',
    sa.Column('tbl', sa.NullType(), nullable=True),
    sa.Column('idx', sa.NullType(), nullable=True),
    sa.Column('stat', sa.NullType(), nullable=True)
    )
    op.drop_table('deal_request')
    # ### end Alembic commands ###
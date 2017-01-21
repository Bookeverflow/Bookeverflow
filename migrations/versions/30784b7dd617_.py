"""empty message

Revision ID: 30784b7dd617
Revises: 98714b154ea4
Create Date: 2017-01-21 17:48:26.295736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30784b7dd617'
down_revision = '98714b154ea4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_want_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_want_list_name'), 'user_want_list', ['name'], unique=False)
    op.create_table('exchange_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_user', sa.Integer(), nullable=True),
    sa.Column('to_user', sa.Integer(), nullable=True),
    sa.Column('from_start', sa.Integer(), nullable=True),
    sa.Column('to_start', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['from_user'], ['user.id'], ),
    sa.ForeignKeyConstraint(['to_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exchange_record')
    op.drop_index(op.f('ix_user_want_list_name'), table_name='user_want_list')
    op.drop_table('user_want_list')
    # ### end Alembic commands ###

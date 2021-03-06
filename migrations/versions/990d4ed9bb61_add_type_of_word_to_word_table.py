"""Add type of word to Word table.

Revision ID: 990d4ed9bb61
Revises: c2b12030531b
Create Date: 2021-07-22 18:46:25.456849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '990d4ed9bb61'
down_revision = 'c2b12030531b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=56), nullable=True),
    sa.Column('meaning', sa.String(length=280), nullable=True),
    sa.Column('type', sa.String(length=140), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('slang')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('slang',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('word', sa.VARCHAR(length=56), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('meaning', sa.VARCHAR(length=280), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='slang_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='slang_pkey')
    )
    op.drop_table('word')
    # ### end Alembic commands ###

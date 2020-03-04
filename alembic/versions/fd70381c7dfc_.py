"""empty message

Revision ID: fd70381c7dfc
Revises: dcc1c3e4e1ab
Create Date: 2019-10-16 18:19:00.479044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd70381c7dfc'
down_revision = 'dcc1c3e4e1ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('original_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'original_name')
    # ### end Alembic commands ###

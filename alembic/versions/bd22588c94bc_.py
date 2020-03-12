"""empty message

Revision ID: bd22588c94bc
Revises: 73d82e1f5cef
Create Date: 2019-11-06 23:07:25.239178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd22588c94bc'
down_revision = '73d82e1f5cef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'remind',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'remind',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
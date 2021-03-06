"""empty message

Revision ID: 8adb8f369149
Revises: a527015c4a64
Create Date: 2019-11-07 19:52:39.153248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8adb8f369149'
down_revision = 'a527015c4a64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'remind_offset',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'remind_offset',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###

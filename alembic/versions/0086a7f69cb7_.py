"""empty message

Revision ID: 0086a7f69cb7
Revises: f2bd9df0d340
Create Date: 2020-03-15 23:18:39.626396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0086a7f69cb7'
down_revision = 'f2bd9df0d340'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dinamic_items', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'dinamic_items', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'dinamic_items', type_='foreignkey')
    op.drop_column('dinamic_items', 'user_id')
    # ### end Alembic commands ###

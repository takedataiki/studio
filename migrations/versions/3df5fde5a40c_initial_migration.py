"""Initial migration

Revision ID: 3df5fde5a40c
Revises: 
Create Date: 2024-12-03 18:16:54.902650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df5fde5a40c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('original', schema=None) as batch_op:
        batch_op.add_column(sa.Column('count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('original', schema=None) as batch_op:
        batch_op.drop_column('count')

    # ### end Alembic commands ###
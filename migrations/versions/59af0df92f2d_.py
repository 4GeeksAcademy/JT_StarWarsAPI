"""empty message

Revision ID: 59af0df92f2d
Revises: 2e086e42e7ab
Create Date: 2023-06-01 17:41:21.929604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59af0df92f2d'
down_revision = '2e086e42e7ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=80), nullable=False))
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###

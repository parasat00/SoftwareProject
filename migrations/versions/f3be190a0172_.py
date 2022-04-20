"""empty message

Revision ID: f3be190a0172
Revises: 6690fcfb6252
Create Date: 2022-04-21 03:53:59.064228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3be190a0172'
down_revision = '6690fcfb6252'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employee', 'login_id',
               existing_type=sa.VARCHAR(length=9),
               nullable=False)
    op.add_column('flex_status', sa.Column('manually', sa.Boolean(), nullable=True))
    op.alter_column('flex_status', 'enterTime',
               existing_type=sa.DATETIME(),
               nullable=True)
    op.alter_column('flex_status', 'exitTime',
               existing_type=sa.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('flex_status', 'exitTime',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.alter_column('flex_status', 'enterTime',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.drop_column('flex_status', 'manually')
    op.alter_column('employee', 'login_id',
               existing_type=sa.VARCHAR(length=9),
               nullable=True)
    # ### end Alembic commands ###
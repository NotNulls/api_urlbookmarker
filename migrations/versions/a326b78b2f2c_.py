"""empty message

Revision ID: a326b78b2f2c
Revises: 
Create Date: 2023-04-26 23:54:00.805513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a326b78b2f2c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['body'])
        batch_op.create_unique_constraint(None, ['url'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('body',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###

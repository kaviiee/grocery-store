"""Initial migration

Revision ID: e95b423fc43d
Revises: 
Create Date: 2023-07-31 19:52:42.601529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e95b423fc43d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_admin',
               existing_type=sa.String(),
               type_=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###

"""amount type float changed

Revision ID: 1902cebcb14d
Revises: e5e77bb3c6a9
Create Date: 2023-08-04 10:52:23.754003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1902cebcb14d'
down_revision = 'e5e77bb3c6a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.BOOLEAN(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.Float(),
               type_=sa.BOOLEAN(),
               existing_nullable=False)

    # ### end Alembic commands ###

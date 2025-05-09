"""Add order_number field to Order model

Revision ID: ef3810298a86
Revises: b6548b395f9b
Create Date: 2025-04-20 19:12:14.797405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef3810298a86'
down_revision = 'b6548b395f9b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('order_number', sa.String(), nullable=True))
    op.create_index(op.f('ix_orders_order_number'), 'orders', ['order_number'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_order_number'), table_name='orders')
    op.drop_column('orders', 'order_number')
    # ### end Alembic commands ### 
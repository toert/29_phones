"""create new number column

Revision ID: 6c97e951a048
Revises: 
Create Date: 2017-02-10 08:25:14.916344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c97e951a048'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('formatted_contact_phone', sa.String))


def downgrade():
    op.drop_column('orders', 'formatted_contact_phone')

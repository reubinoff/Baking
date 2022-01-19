"""removing test field

Revision ID: 3058a27a234e
Revises: f12b70f3a596
Create Date: 2021-11-10 16:55:23.955742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3058a27a234e'
down_revision = 'f12b70f3a596'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('test', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
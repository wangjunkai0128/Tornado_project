"""create_users_table

Revision ID: 6221568015e2
Revises: 
Create Date: 2018-09-20 14:26:51.507595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6221568015e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('creatime', sa.DateTime(), nullable=True),
    sa.Column('_locked', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
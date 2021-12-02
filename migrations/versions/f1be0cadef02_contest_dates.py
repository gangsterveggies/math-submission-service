"""contest dates

Revision ID: f1be0cadef02
Revises: 179ae2144b43
Create Date: 2021-12-01 23:53:21.443188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1be0cadef02'
down_revision = '179ae2144b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contest', sa.Column('start_date', sa.DateTime(), nullable=True))
    op.add_column('contest', sa.Column('end_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contest', 'end_date')
    op.drop_column('contest', 'start_date')
    # ### end Alembic commands ###
"""Scrap old schema and accomodate feedbacks

Revision ID: fbbcf17397fd
Revises: 
Create Date: 2023-10-17 22:08:29.084940

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fbbcf17397fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=16), nullable=False))
        batch_op.add_column(sa.Column('feed', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('feed')
        batch_op.drop_column('type')

    op.create_table('feedback',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type', mysql.VARCHAR(length=16), nullable=True),
    sa.Column('feed', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###

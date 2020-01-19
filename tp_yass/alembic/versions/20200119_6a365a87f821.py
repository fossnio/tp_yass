"""change value of sysconfig to text

Revision ID: 6a365a87f821
Revises: f0a11c426925
Create Date: 2020-01-19 13:41:08.900996

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6a365a87f821'
down_revision = 'f0a11c426925'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sys_config', 'value',
               existing_type=mysql.VARCHAR(50),
               type_=sa.Text(),
               existing_nullable=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sys_config', 'value',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(50),
               existing_nullable=False,
               existing_server_default=sa.text('0'))
    # ### end Alembic commands ###

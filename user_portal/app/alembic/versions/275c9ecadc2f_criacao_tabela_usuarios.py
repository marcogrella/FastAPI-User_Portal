"""criacao tabela usuarios

Revision ID: 275c9ecadc2f
Revises: 
Create Date: 2022-01-06 16:00:12.457026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '275c9ecadc2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('sobrenome', sa.String(), nullable=False),
        sa.Column('endereco', sa.String(), nullable=False),
        sa.Column('cpf', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('senha', sa.String(), nullable=False),
        sa.Column('data_criacao', sa.TIMESTAMP(timezone=True), 
                server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cpf'),
        sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass



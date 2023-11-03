"""empty message

Revision ID: 5946ac691523
Revises: 
Create Date: 2023-11-03 14:53:31.457629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5946ac691523'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('llm_template',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('docker_image_url', sa.String(length=200), nullable=True),
    sa.Column('type', sa.Enum('OS_LLM', 'Cloud_LLM'), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('version', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('tags', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    with op.batch_alter_table('llm_template', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_llm_template_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('llm_template', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_llm_template_id'))

    op.drop_table('llm_template')
    # ### end Alembic commands ###

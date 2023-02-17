"""empty message

Revision ID: 57d4bbdd15ae
Revises: 
Create Date: 2023-02-18 00:18:30.470795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57d4bbdd15ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('pw', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('vet', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('animals',
    sa.Column('animal_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('animal_name', sa.String(), nullable=False),
    sa.Column('bday', sa.String(length=10), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('neutered', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('animal_id'),
    sa.UniqueConstraint('animal_id')
    )
    op.create_table('Routine',
    sa.Column('index', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('routine_id', sa.Integer(), nullable=True),
    sa.Column('routine_name', sa.String(), nullable=False),
    sa.Column('weekday', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['animal_id'], ['animals.animal_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('index'),
    sa.UniqueConstraint('index')
    )
    op.create_table('checklist_default',
    sa.Column('index', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('currdate', sa.String(), nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('food', sa.String(), nullable=True),
    sa.Column('bowels', sa.String(), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['animal_id'], ['animals.animal_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('index'),
    sa.UniqueConstraint('index')
    )
    op.create_table('health',
    sa.Column('index', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('currdate', sa.String(), nullable=True),
    sa.Column('kind', sa.String(), nullable=True),
    sa.Column('affected_area', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['animal_id'], ['animals.animal_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('index'),
    sa.UniqueConstraint('index')
    )
    op.create_table('journal',
    sa.Column('index', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('currdate', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['animal_id'], ['animals.animal_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('index'),
    sa.UniqueConstraint('index')
    )
    op.create_table('checklist_routine',
    sa.Column('index', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('routine_index', sa.Integer(), nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('currdate', sa.String(), nullable=False),
    sa.Column('routine_name', sa.String(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['animal_id'], ['animals.animal_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['routine_index'], ['Routine.index'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('index'),
    sa.UniqueConstraint('index')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checklist_routine')
    op.drop_table('journal')
    op.drop_table('health')
    op.drop_table('checklist_default')
    op.drop_table('Routine')
    op.drop_table('animals')
    op.drop_table('user')
    # ### end Alembic commands ###

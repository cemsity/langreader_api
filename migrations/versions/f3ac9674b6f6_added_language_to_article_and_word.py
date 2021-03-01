"""added language to Article and Word

Revision ID: f3ac9674b6f6
Revises: 4b1ebb7a5104
Create Date: 2021-02-28 19:22:31.611480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3ac9674b6f6'
down_revision = '4b1ebb7a5104'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.String(), nullable=True))

    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.String(), nullable=True))
        batch_op.drop_constraint('_word_user_uc', type_='unique')
        batch_op.create_unique_constraint('_user_word_lang_uc', ['user_id', 'word', 'language'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.drop_constraint('_user_word_lang_uc', type_='unique')
        batch_op.create_unique_constraint('_word_user_uc', ['user_id', 'word'])
        batch_op.drop_column('language')

    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('language')

    # ### end Alembic commands ###

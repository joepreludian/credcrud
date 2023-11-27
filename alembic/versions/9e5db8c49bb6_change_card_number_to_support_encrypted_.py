"""change Card number to support Encrypted Data

Revision ID: 9e5db8c49bb6
Revises: 652e07fe64ba
Create Date: 2023-11-26 22:59:53.050354

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9e5db8c49bb6"
down_revision: Union[str, None] = "652e07fe64ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cards",
        "card_number",
        existing_type=sa.VARCHAR(length=16),
        type_=sa.Text(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cards",
        "card_number",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=16),
        existing_nullable=False,
    )
    # ### end Alembic commands ###

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision: str = '61d4bf04ffbb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Users Table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), sa.Identity(start=1, increment=1), primary_key=True),
        sa.Column('username', sa.String(150), nullable=False),  # Specified length for username
        sa.Column('email', sa.String(255), nullable=False),  # Specified length for email
        sa.Column('password_hash', sa.String(255), nullable=False),  # Specified length for password_hash
        sa.Column('role', sa.String(50), nullable=False),  # Specified length for role
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text("CAST(0 AS BIT)")),
    )

    # Unique Index on Email
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Optional: Add CHECK Constraint for Role (if predefined roles exist)
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT chk_role CHECK (role IN ('admin', 'user', 'moderator'))"
    )

    # Valid Tokens Table
    op.create_table(
        'valid_tokens',
        sa.Column('id', sa.Integer(), sa.Identity(start=1, increment=1), nullable=False, primary_key=True),
        sa.Column('expires', sa.DateTime(), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),  # Specified length for token
    )

    # Loan Requests Table
    op.create_table(
        'loan_requests',
        sa.Column('id', sa.Integer(), sa.Identity(start=1, increment=1), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('state', sa.String(50), nullable=False),  # Specified length for state
        sa.Column('bank', sa.String(255), nullable=False),  # Specified length for bank
        sa.Column('naics', sa.BigInteger(), nullable=False),
        sa.Column('term', sa.Integer(), nullable=False),
        sa.Column('no_emp', sa.Integer(), nullable=False),
        sa.Column('new_exist', sa.Integer(), nullable=False),
        sa.Column('create_job', sa.Integer(), nullable=False),
        sa.Column('retained_job', sa.Integer(), nullable=False),
        sa.Column('urban_rural', sa.Integer(), nullable=False),
        sa.Column('rev_line_cr', sa.Integer(), nullable=False),
        sa.Column('low_doc', sa.Integer(), nullable=False),
        sa.Column('gr_appv', sa.BigInteger(), nullable=False),
        sa.Column('recession', sa.Integer(), nullable=False),
        sa.Column('has_franchise', sa.Integer(), nullable=False),
        sa.Column('approval_status', sa.String(50), nullable=True),  # Specified length for approval_status
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

def downgrade() -> None:
    op.drop_table('loan_requests')
    op.drop_table('valid_tokens')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')



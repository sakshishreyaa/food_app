"""empty message

Revision ID: 4caa4aabcd5d
Revises: 
Create Date: 2021-12-28 16:39:57.097268

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4caa4aabcd5d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "User",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(80)),
        sa.Column("phone", sa.String(10), nullable=False, index=True),
        sa.Column("role", sa.Unicode(20)),
        sa.Column("password", sa.String(150), nullable=False),
    )
    op.create_table(
        "Location",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("zip", sa.Integer, index=True),
        sa.Column("state", sa.String(50), nullable=False),
        sa.Column("city", sa.String(50), nullable=False),
        sa.Column("country", sa.String(50), nullable=False),
        sa.Column("block_street", sa.String(50), nullable=False),
    )
    op.create_table(
        "Customer",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("User.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("name", sa.String(20), nullable=False),
        sa.Column("occupation", sa.String(80), nullable=False),
        sa.Column("dob", sa.DateTime),
        sa.Column(
            "location", sa.Integer, sa.ForeignKey("Location.id", ondelete="CASCADE")
        ),
    )
    op.create_table(
        "Restaurant",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column(
            "owner",
            sa.Integer,
            sa.ForeignKey("User.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("no_of_staff", sa.Integer, nullable=False),
        sa.Column("seats", sa.Integer, nullable=True),
        sa.Column("extra_seats", sa.Integer, nullable=True),
        sa.Column(
            "location_id", sa.Integer, sa.ForeignKey("Location.id", ondelete="CASCADE")
        ),
        sa.Column("menu", sa.JSON, nullable=False),
    )

    op.create_table(
        "Payment",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("source", sa.String(200)),
        sa.Column("online_payment", sa.Boolean, nullable=False),
        sa.Column("amount", sa.Float),
    )
    op.create_table(
        "Order",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("price", sa.Float),
        sa.Column("paid_status", sa.Boolean, default=False),
        sa.Column(
            "payment_id", sa.Integer, sa.ForeignKey("Payment.id", ondelete="CASCADE")
        ),
        sa.Column("order_details", sa.JSON),
        sa.Column("items", sa.Integer),
    )
    op.create_table(
        "Booking",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("User.id", ondelete="CASCADE"),
            index=True,
        ),
        sa.Column(
            "restaurant_id",
            sa.Integer,
            sa.ForeignKey("Restaurant.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("from_time", sa.DateTime),
        sa.Column("to_time", sa.DateTime),
        sa.Column("no_of_guests", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("Order"),
    op.drop_table("Payment"),
    op.drop_table("Customer"),
    op.drop_table("Location"),
    op.drop_table("Restauratnt"),
    op.drop_table("User"),
    op.drop_table("Booking"),

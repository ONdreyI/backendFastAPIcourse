"""Add cascade update and delete for ORM

Revision ID: e2c7552db986
Revises: 162013befa2f
Create Date: 2024-11-25 14:19:59.543819

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e2c7552db986"
down_revision: Union[str, None] = "162013befa2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("bookings_user_id_fkey", "bookings", type_="foreignkey")
    op.drop_constraint("bookings_room_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(
        None, "bookings", "users", ["user_id"], ["id"], onupdate="CASCADE"
    )
    op.create_foreign_key(
        None, "bookings", "rooms", ["room_id"], ["id"], onupdate="CASCADE"
    )
    op.drop_constraint("rooms_hotel_id_fkey", "rooms", type_="foreignkey")
    op.create_foreign_key(
        None, "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint(
        "rooms_facilities_facility_id_fkey", "rooms_facilities", type_="foreignkey"
    )
    op.drop_constraint(
        "rooms_facilities_room_id_fkey", "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
        onupdate="CASCADE",
    )
    op.create_foreign_key(
        None, "rooms_facilities", "rooms", ["room_id"], ["id"], onupdate="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        "rooms_facilities_room_id_fkey",
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
    )
    op.create_foreign_key(
        "rooms_facilities_facility_id_fkey",
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
    )
    op.drop_constraint(None, "rooms", type_="foreignkey")
    op.create_foreign_key(
        "rooms_hotel_id_fkey", "rooms", "hotels", ["hotel_id"], ["id"]
    )
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(
        "bookings_room_id_fkey", "bookings", "rooms", ["room_id"], ["id"]
    )
    op.create_foreign_key(
        "bookings_user_id_fkey", "bookings", "users", ["user_id"], ["id"]
    )
    # ### end Alembic commands ###

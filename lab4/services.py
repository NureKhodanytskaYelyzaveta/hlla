from datetime import datetime
from sqlalchemy import select, and_, not_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models import Booking, Room, BookingService

async def add_booking(
    session: AsyncSession,
    client_id: int, room_id: int,
    check_in: datetime, check_out: datetime,
    service_ids: list[int] | None = None
) -> Booking:
    overlap = select(Booking).where(
        and_(
            Booking.room_id == room_id,
            Booking.status != "cancelled",
            not_(
                or_(
                    Booking.check_out <= check_in,
                    Booking.check_in >= check_out
                )
            )
        )
    )
    result = await session.execute(overlap)
    if result.scalar_one_or_none():
        raise ValueError("Кімната вже заброньована на цей період.")

    booking = Booking(
        client_id=client_id, room_id=room_id,
        check_in=check_in, check_out=check_out
    )
    session.add(booking)
    await session.flush()

    if service_ids:
        for sid in service_ids:
            session.add(BookingService(booking_id=booking.id, service_id=sid))

    await session.commit()
    await session.refresh(booking)
    return booking

async def delete_booking(session: AsyncSession, booking_id: int):
    result = await session.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise ValueError("Бронювання не знайдено")
    await session.delete(booking)
    await session.commit()

async def get_available_rooms(
    session: AsyncSession, hotel_id: int,
    check_in: datetime, check_out: datetime
):
    query = (
        select(Room)
        .where(
            Room.hotel_id == hotel_id,
            not_(
                Room.id.in_(
                    select(Booking.room_id).where(
                        and_(
                            Booking.status != "cancelled",
                            not_(
                                or_(
                                    Booking.check_out <= check_in,
                                    Booking.check_in >= check_out
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    result = await session.execute(query)
    return result.scalars().all()
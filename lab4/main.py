import asyncio
from datetime import datetime
from sqlalchemy import select

from database import init_db, async_session
from services import add_booking, delete_booking, get_available_rooms
from models import Hotel, Client, Room, Service


async def main():
    await init_db()

    async with async_session() as session:

        existing_hotels = await session.execute(select(Hotel))

        if not existing_hotels.scalar_one_or_none():
            session.add_all([
                Hotel(name="Grand Kyiv", city="Київ"),

                Client(
                    name="Олексій",
                    email="oleksiy@mail.com",
                    phone="+380991112233"
                ),

                Room(
                    hotel_id=1,
                    room_number="101",
                    type="Standard",
                    price=1200
                ),

                Room(
                    hotel_id=1,
                    room_number="202",
                    type="Lux",
                    price=2500
                ),

                Service(name="Сніданок", price=250),
                Service(name="Трансфер", price=400)
            ])

            await session.commit()

        booking = await add_booking(
            session,
            client_id=1,
            room_id=1,
            check_in=datetime(2026, 6, 10),
            check_out=datetime(2026, 6, 13),
            service_ids=[1]
        )

        print(
            f"✅Бронювання #{booking.id} створено "
            f"| Статус: {booking.status}"
        )

        available = await get_available_rooms(
            session,
            hotel_id=1,
            check_in=datetime(2026, 6, 11),
            check_out=datetime(2026, 6, 12)
        )

        print(
            f"Вільні кімнати: "
            f"{[r.room_number for r in available]}"
        )

        try:
            await add_booking(
                session,
                client_id=1,
                room_id=1,
                check_in=datetime(2026, 6, 11),
                check_out=datetime(2026, 6, 12)
            )

        except ValueError as e:
            print(f"❌Помилка бронювання: {e}")

        await delete_booking(session, booking.id)

        print("❌Бронювання видалено")

        available_after_delete = await get_available_rooms(
            session,
            hotel_id=1,
            check_in=datetime(2026, 6, 11),
            check_out=datetime(2026, 6, 12)
        )

        print("✅Кімнати після видалення бронювання:")

        for room in available_after_delete:
            print(room.room_number)

        # SQL-ін'єкція
        malicious_input = "'; DROP TABLE hotels; --"

        result = await session.execute(
            select(Client).where(
                Client.name == malicious_input
            )
        )

        print("SQL-ін'єкція не спрацювала")

        try:
            bad_room = Room(
                hotel_id=1,
                room_number="999",
                type="Hack",
                price=-500
            )

            session.add(bad_room)
            await session.commit()

        except Exception as e:
            print("❌Помилка обмеження:", e)

            await session.rollback()

        results = await asyncio.gather(
            get_available_rooms(
                session,
                1,
                datetime(2026, 6, 11),
                datetime(2026, 6, 12)
            ),

            get_available_rooms(
                session,
                1,
                datetime(2026, 6, 15),
                datetime(2026, 6, 18)
            )
        )

        print("✅Асинхронні запити виконані успішно")

if __name__ == "__main__":
    asyncio.run(main())
from pathlib import Path
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from data_models.models import *
from data_access.data_base import init_db

if __name__ == '__main__':
    database_file = "./data/hotel_reservation.db"

    database_path = Path(database_file)
    if not database_path.parent.exists():
        database_path.parent.mkdir()

    # Tell SQL Alchemy how to connect to the db. In this case it's a sqlite db.
    engine = create_engine(f'sqlite:///{database_path}', echo=False)

    session = scoped_session(sessionmaker(bind=engine))

    # Get all hotels...
    query = select(Hotel)
    print(query)
    result = session.execute(query)
    for hotel in result:
        print(hotel)  # Notice that it will be a tuple, and not the object!
    input("Press Enter to continue...")

    # Therefore we use the sqlalchemy function to get scalars() and all() of them
    result = session.execute(query).scalars().all()
    for hotel in result:
        print(hotel)
    input("Press Enter to continue...")

    # Now lets do a where and like, look how similar it is to sql what you have learned!
    query = select(Hotel).where(Hotel.name.like('%Amaris'))
    print(query)
    result = session.execute(query).scalars().all()
    for hotel in result:
        print(hotel)
        # Rooms can also be accessed, even without the join. Because SQLAlchemy knows how!
        for room in hotel.rooms:
            print(room)
    input("Press Enter to continue...")

    # Let's get a specific hotel by it's id.
    query = select(Hotel).where(Hotel.id == 1)
    result = session.execute(query).scalars().one()  # We use one() instead of all() (only one or raise Error!)
    print(result)
    input("Press Enter to continue...")

    # Let's get all rooms of Hotel 1
    query = select(Room).where(Room.hotel_id == 1)
    result = session.execute(query).scalars().all()
    # how many rooms are there?
    print(len(result))
    input("Press Enter to continue...")

    # Let's get all Bookings
    query = select(Booking)
    result = session.execute(query).scalars().all()
    for booking in result:
        print(booking)
    input("Press Enter to continue...")

    selected_hotel_id = 1  # we want to book a room in hotel with the id 1
    booking_guest = 5  # Laura
    guest_query = select(RegisteredGuest).where(RegisteredGuest.id == booking_guest)
    print(guest_query)
    # We only have the registered guest with id == booking_guest once in db. So we use one().
    laura = session.execute(guest_query).scalars().one()
    print(laura)
    input("Press Enter to continue...")

    query_laura_bookings = select(Booking).where(Booking.guest == laura)
    print(query_laura_bookings)
    laura_bookings = session.execute(query_laura_bookings).scalars().all()
    for booking in laura_bookings:
        print(booking)
    input("Press Enter to continue...")

    # Let's get all Room numbers booked between start and end date. This will be used to exclude these rooms.
    query_booked_rooms = (select(Room.number).
                          join(Hotel).
                          join(Booking).
                          where(Hotel.id == selected_hotel_id,
                                Booking.start_date.between(
                                    date(2024, 2, 19), date(2024, 2, 20))
                                )
                          )
    print(query_booked_rooms)
    result_booked_rooms = session.execute(query_booked_rooms).scalars().all()
    print(result_booked_rooms)
    input("Press Enter to continue...")

    query_available_rooms = (select(Room).
                             join(Hotel).
                             where(Hotel.id == selected_hotel_id,
                                   Room.number.not_in(query_booked_rooms)
                                   )
                             )
    print(query_available_rooms)
    result_available_rooms = session.execute(query_available_rooms).scalars().all()
    print(len(result_available_rooms))
    input("Press Enter to continue...")

    print(result_available_rooms[0])
    input("Press Enter to continue...")

    # create new booking for laura
    booking = Booking(room=result_available_rooms[0], guest=laura, number_of_guests=1, start_date=date.today(),
                      end_date=date.today() + timedelta(days=3), comment="My very new booking!")

    # add the booking
    session.add(booking)
    # commit the adding
    session.commit()

    # test if the booking is saved
    laura_bookings = session.execute(query_laura_bookings).scalars().all()
    for booking in laura_bookings:
        print(booking)
    input("Press Enter to continue...")

    # delete the booking.
    session.delete(booking)
    # commit the deleting.
    session.commit()

    laura_bookings = session.execute(query_laura_bookings).scalars().all()
    for booking in laura_bookings:
        print(booking)
    input("Press Enter to continue...")

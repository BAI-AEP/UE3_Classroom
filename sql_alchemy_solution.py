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

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    init_db(database_file, generate_example_data=True)

    # Let's create a session to connect to the db.
    session = scoped_session(sessionmaker(bind=engine))

    # Get all hotels...
    print("All Hotels:")
    query = select(Hotel)
    print(query)
    result = session.execute(query)
    for hotel in result:
        print(hotel)  # Notice that it will be a tuple, and not the object!
    input("Press Enter to continue...")
    print("\n")

    # Therefore we use the sqlalchemy function to get scalars() and all() of them
    print("All Hotels as objects:")
    result = session.execute(query).scalars().all()
    for hotel in result:
        print(hotel)
    input("Press Enter to continue...")
    print("\n")

    # Now lets do a where and like, look how similar it is to sql what you have learned!
    print("All Hotels where name like '%Amaris':")
    query = select(Hotel).where(Hotel.name.like('%Amaris'))
    print(query)
    result = session.execute(query).scalars().all()
    for hotel in result:
        print(hotel)
        # Rooms can also be accessed, even without the join. Because SQLAlchemy knows how!
        for room in hotel.rooms:
            print(room)
    input("Press Enter to continue...")
    print("\n")

    # Let's get a specific hotel by it's id.
    print("Hotel with id == 1")
    query = select(Hotel).where(Hotel.id == 1)
    result = session.execute(query).scalars().one()  # We use one() instead of all() (only one or raise Error!)
    print(result)
    input("Press Enter to continue...")
    print("\n")

    # Let's get all rooms of Hotel 1
    print("Rooms of Hotel with id == 1")
    query = select(Room).where(Room.hotel_id == 1)
    result = session.execute(query).scalars().all()
    # how many rooms are there?
    print(len(result))
    input("Press Enter to continue...")
    print("\n")

    # Let's get all Bookings
    print("All Bookings")
    query = select(Booking)
    result = session.execute(query).scalars().all()
    for booking in result:
        print(booking)
    input("Press Enter to continue...")
    print("\n")

    # Let's get all Bookings ordered by Hotel
    print("All Bookings ordered by room_hotel_id")
    query = select(Booking).order_by(Booking.room_hotel_id)
    result = session.execute(query).scalars().all()
    for booking in result:
        print(booking)
    input("Press Enter to continue...")
    print("\n")

    print("Laura is booking")
    booking_guest = 5  # Laura
    guest_query = select(RegisteredGuest).where(RegisteredGuest.id == booking_guest)
    print(guest_query)
    # The user with the id == booking_guest only exists once. So we use one().
    laura = session.execute(guest_query).scalars().one()
    print(laura)
    input("Press Enter to continue...")
    print("\n")

    print("Laura wants to book in Hotel 1")
    selected_hotel_id = 1  # we want to book a room in hotel with the id 1
    # Let's get all Room numbers booked between start and end date. This will be used to exclude these rooms.
    query_booked_rooms = (
        select(Room.number).
        join(Hotel).
        join(Booking).
        where(Hotel.id == selected_hotel_id,
              (
                      Booking.start_date.between(date.today(), date.today() + timedelta(days=3))
                      |
                      Booking.end_date.between(date.today(), date.today() + timedelta(days=3))
              )
              )
    )
    print(query_booked_rooms)
    result_booked_rooms = session.execute(query_booked_rooms).scalars().all()
    print(result_booked_rooms)
    input("Press Enter to continue...")
    print("\n")

    print("Available rooms in Hotel")
    # Let's combine the query to get available rooms
    query_available_rooms = (select(Room).
                             join(Hotel).
                             where(Hotel.id == selected_hotel_id,
                                   Room.number.not_in(query_booked_rooms)
                                   )
                             )
    print(query_available_rooms)
    result_available_rooms = session.execute(query_available_rooms).scalars().all()
    for room in result_available_rooms:
        print(room)
    print(len(result_available_rooms))
    input("Press Enter to continue...")
    print("\n")

    print("Laura selects first available room")
    selected_room = result_available_rooms[0]
    print(selected_room)
    input("Press Enter to continue...")
    print("\n")

    # create new booking for laura
    booking = Booking(room=result_available_rooms[0], guest=laura, number_of_guests=1, start_date=date.today(),
                      end_date=date.today() + timedelta(days=3), comment="My very new booking!")

    # add the booking
    session.add(booking)
    # commit the adding
    session.commit()

    print("Get all booking of Laura")
    query_laura_bookings = select(Booking).where(Booking.guest == laura)
    print(query_laura_bookings)
    laura_bookings = session.execute(query_laura_bookings).scalars().all()
    for booking in laura_bookings:
        print(booking)
    input("Press Enter to continue...")
    print("\n")

    # Let's select again the available rooms. The room with the id of selected_room should not be available.
    print(f"Is room with the number {selected_room.number} still available?")
    result_available_rooms = session.execute(query_available_rooms).scalars().all()
    ids = []
    for room in result_available_rooms:
        ids.append(room.number)
    print(ids)
    input("Press Enter to continue...")
    print("\n")

    print("Delete the booking again")
    # delete the booking.
    session.delete(booking)
    # commit the deleting.
    session.commit()

    laura_bookings = session.execute(query_laura_bookings).scalars().all()
    for booking in laura_bookings:
        print(booking)
    input("Press Enter to continue...")

    print("SQLAlchemy is also handeling equality")
    hotel_1_query = select(Hotel).where(Hotel.id == 1)
    hotel_also_1_query = select(Hotel).where(Hotel.id == 1)

    result_1 = session.execute(hotel_1_query).scalars().one()
    result_also_1 = session.execute(hotel_also_1_query).scalars().one()

    print(result_1)
    print(result_also_1)

    input("Press Enter to continue...")
    print("\n")
    print(result_1 == result_also_1)

    print("But Objects not!")
    hotel_1 = Hotel(name="Hotel 1")
    hotel_also_1 = Hotel(name="Hotel 1")
    print(hotel_1 == hotel_also_1)

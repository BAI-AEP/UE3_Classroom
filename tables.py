from models import *


def print_as_table(table: list, layout: list = None, header=None) -> None:
    cols = len(table[0])
    if layout is None:
        layout = [30] * cols
    if cols != len(layout):
        raise ValueError("Layout has to fit columns in table")

    for row in table:
        if len(row) != cols:
            raise ValueError("Layout must be the same for each row")
    if header:
        if len(header) != cols:
            raise ValueError("Header must have fit columns in table")
        print(f"{'#':<5}", end="")
        for i, col in enumerate(range(cols)):
            print(f"{header[col]:<{layout[i]}}", end="")
        print()
        print("-" * (5 + sum(layout)))
    for n, row in enumerate(table, 1):
        print(f"{n:<5}", end="")
        for i, col in enumerate(range(cols)):
            if len(str(row[col])) + 1 > layout[i]:
                text = f"{row[col][0:layout[i] - 4]}..."
                print(f"{text:<{layout[i]}}", end="")
            else:
                print(f"{row[col]:<{layout[i]}}", end="")
        print()


if __name__ == "__main__":
    list_hotels = [
        ["Aria", "Olten", 3],
        ["Dolder", "Zürich", 5]
    ]

    print_as_table(list_hotels, layout=[20, 10, 10], header=["Name", "City", "Stars"])
    print()
    print()
    hotels = [
        Hotel(name="Hotel Amaris", stars=3,
              address=Address(street="Tannwaldstrasse 34", zip="4600", city="Olten")),
        Hotel(name="Leonardo Boutique Hotel Rigihof Zurich", stars=3,
              address=Address(street=" Universitätstrasse 101", zip="8006", city="Zürich"))
    ]
    list_hotels = []
    for hotel in hotels:
        list_hotels.append([hotel.name, hotel.address.city, hotel.stars])

    print_as_table(list_hotels, layout=[20, 10, 10], header=["Name", "City", "Stars"])

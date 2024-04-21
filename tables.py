def print_table(table: list):
    #print(table) # This prints me the list given to the function
    for row in table:
        for column in row:
            print(f"{column:<10} ", end="")
        print()

def print_table_sol(table: list, layout: list = None, header=None, top=0, sort=None) -> None:
    cols = len(table[0])
    if sort:
        if type(sort) is tuple:
            table = sorted(table, key=lambda _row: _row[sort[0]], reverse=sort[1])
    if top != 0:
        table = table[0:top]
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
        print(f"{'#':^5}", end="")
        for i, col in enumerate(range(cols)):
            print(f"{header[col]:<{layout[i]}}", end="")
        print()
        print("-" * (5 + sum(layout)))
    for n, row in enumerate(table, 1):
        print(f"{n:^5}", end="")
        for i, col in enumerate(range(cols)):
            if len(str(row[col])) + 1 > layout[i]:
                text = f"{row[col][0:layout[i] - 4]}..."
                print(f"{text:<{layout[i]}}", end="")
            else:
                print(f"{row[col]:<{layout[i]}}", end="")
        print()


if __name__ == "__main__":

    sort_list = [9, 4, 2]
    print(sort_list)
    sort_list.sort()
    print(sort_list)
    sort_list.sort(reverse=True)
    print(sort_list)
    sort_list.reverse()
    print(sort_list)

    list_hotels = [
        ["Aria", "Olten", 3],
        ["Dolder", "Zürich", 5],
        ["Arte", "Olten", 4],
        ["Oltnerhof", "Olten", 0]
    ]

    print(list_hotels)
    list_hotels.sort(key=lambda hotel: hotel[0])
    print(list_hotels)
    list_hotels.sort(key=lambda hotel: hotel[1])
    print(list_hotels)
    list_hotels.sort(key=lambda hotel: hotel[2])
    print(list_hotels)

    print(list_hotels[0:2])

    print(sort_list)
    print(sort_list[-2:])

    print_table_sol(list_hotels, layout=[20, 10, 10], header=["Name", "City", "Stars"], top=1, sort=(0, True))
    '''print()
    print()
    hotels = [
        Hotel(name="Hotel Amaris", stars=3,
              address=Address(street="Tannwaldstrasse 34", zip="4600", city="Olten")),
        Hotel(name="Leonardo Boutique Hotel Rigihof Zurich", stars=3,
              address=Address(street=" Universitätstrasse 101", zip="8006", city="Zürich"))
    ] # This objects would actually come from the database. (e.g. session.query(Hotel).all())
    list_hotels = []
    for hotel in hotels:
        list_hotels.append([hotel.name, hotel.address.city, hotel.stars])

    print_as_table(list_hotels, layout=[20, 10, 10], header=["Name", "City", "Stars"])'''

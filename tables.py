list_2d = [
    ["Name", "City", "Stars"],
    ["Aria", "Olten", 3],
    ["Dolder", "Zürich", 5]
]

def print_as_table(table : list, layout : list = None) -> None:
    cols = len(table[0])
    if layout is None:
        layout = [30]*cols
    if cols != len(layout):
        raise ValueError("Layout has to fit columns in table")

    print(f"{'#':<5}", end="")
    for i, col in enumerate(range(cols)):
        print(f"{table[0][col]:<{layout[i]}}", end="")
    print()
    print("-"*(5+sum(layout)))
    for n, row in enumerate(table[1:], 1):
        print(f"{n:<5}", end="")
        for i, col in enumerate(range(cols)):
            if len(str(row[col]))+1 > layout[i]:
                text = f"{row[col][0:layout[i] - 4]}..."
                print(f"{text:<{layout[i]}}", end="")
            else:
                print(f"{row[col]:<{layout[i]}}", end="")
        print()

print_as_table(list_2d, layout=[20, 10, 10])
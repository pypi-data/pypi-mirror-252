# print strings in a matrix for easy viewing
def print_matrix(strings, columns):
    max_length = max(len(s) for s in strings)

    format_str = "{:<" + str(max_length + 2) + "}"

    for i, string in enumerate(strings):
        print(format_str.format(string), end="")
        if (i + 1) % columns == 0:
            print()
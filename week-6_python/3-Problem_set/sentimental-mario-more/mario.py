# TODO
# main function to print pyramid
def main():
    N = correct_usage()
    for i in range(1, N + 1):
        print(" " * (N - i), end="")
        print("#" * i, end="")
        print("  ", end="")
        print("#" * i)


# handle ValueError input by user
def correct_usage():
    while True:
        try:
            N = int(input("Height: "))
            if N > 0 and N < 9:
                return N
        except ValueError:
            return correct_usage()


main()
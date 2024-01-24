def str_validate(input_message, options, error_message = "Invalid Input"):
    while True:
        Input = input(input_message)

        if Input in options:
            return Input

        print(error_message)


def int_validate(input_message, range, error_message = "Invalid Input"):
    while True:
        Input = input(input_message)

        if not Input.isnumeric():
            print("Input is not a number!")
            continue

        if int(Input) in range(range[0], range[1] + 1):
            return int(Input)

        print(error_message)

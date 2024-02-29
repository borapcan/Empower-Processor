def remove_after_period(input_string):
    # Find the index of the first period
    index = input_string.find(".")

    # If period found, return string up to that index, otherwise return original string
    if index != -1:
        return input_string[:index]
    else:
        return input_string

import re


def add_termination(address: str) -> str:
    """
    Returns the addresses with potitionnal numbers.

    Parameters:
        address (str): The base address.

    Returns:
        address (str): The new address.
    """
    pattern = "[0-9]+"
    numbers_in_address = re.findall(pattern, address)

    new_numbers = []

    for i in numbers_in_address:
        if i[-1] == "1":
            if i[-2:] == "11":
                i += "th"
                new_numbers += [i]
            else:
                i += "st"
                new_numbers += [i]

        elif i[-1] == "2":
            if i[-2:] == "12":
                i += "th"
                new_numbers += [i]
            else:
                i += "nd"
                new_numbers += [i]

        elif i[-1] == "3":
            if i[-2:] == "13":
                i += "th"
                new_numbers += [i]
            else:
                i += "rd"
                new_numbers += [i]
        else:
            i += "th"
            new_numbers += [i]

    change_dict = dict(zip(numbers_in_address, new_numbers))
    address = address.split(" ")

    for i in range(len(address)):
        word = address[i]
        if word in change_dict.keys():
            address[i] = change_dict[word]

    address = " ".join(address)

    return address


def remove_houses_numbers(address: str) -> str:
    """
    Remove the houses' numbers in the addresses.

    Parameters:
        address (str): The base address.

    Returns:
        address (str): The new address.
    """
    pattern = "[0-9]+-[0-9]*"
    houses_numbers = re.findall(pattern, address)

    for i in houses_numbers:
        address = address.replace(i, "")

    return address

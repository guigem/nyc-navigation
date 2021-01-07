import re


def add_termination(address:str) -> str:
    """
    Returns the addresses with potitionnal numbers.

    Parameters:
        address (str): The base address.

    Returns:
        address (str): The new address.
    """
    pattern = "[0-9]+"
    numbers_in_address = re.findall(pattern, address)

    print(numbers_in_address)

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
    
    print(new_numbers)

    change_dict = dict(zip(numbers_in_address, new_numbers))
    address = address.replace("-", " ")
    address = address.split(" ")
    

    for i in range(len(address)):
        word = address[i]
        if word in change_dict.keys():
            print(word, "ok")
            address[i] = change_dict[word]
        else:
            print(word, "nope")
    
    address = " ".join(address)
    address = address.replace("  ", " ")
    
    return address

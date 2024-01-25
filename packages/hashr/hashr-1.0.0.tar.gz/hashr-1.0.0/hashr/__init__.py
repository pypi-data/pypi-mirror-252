def hashr(input: str, use_salt=False) -> str | tuple[str, str]:
    """
    Custom hashing algorithm to turn a string into a hash string,
    with the option of using salting for increased security.

    Parameters:
        - input : string to be hashed
        - use_salt : bool whether to use a salt or not,
        False by default

    Returns:
        - string or tuple of two strings : without salt, just returns
        the hash, with salt, returns hash and salt as a tuple

    This algorithm uses character folding to produce a different hash
    for every unique string, even if the differences are extremely
    minimal, such as with "Hello World1" and "Hello World2". It adds
    the values of every character in the string up, multiplying each
    by a different prime number for discrete complexity. For enhanced
    security, two passes are done to avoid information clumping. Lastly,
    for maximum safety, salting is optional to produce different hashes
    for two copies of strings, as long as salts are saved along with hashes.
    """

    if not input:
        return ""

    # the hashing algorithm
    def hash(string: str, current_sum: int) -> int:
        primes = [5, 11, 31, 127, 709, 5381, 52711, 648391]
        point = 7

        for char in string:
            current_sum += ord(char)  # gets numerical value of character
            current_sum *= primes[point]  # shuffles values by primes
            point -= 1 if point > 0 else -7
        return current_sum

    salt = str(saltr()) if use_salt else ""
    input += salt  # appends salt to input string if present

    total = 0
    total += hash(input, total)  # first pass
    total += hash(str(total), total)  # second pass
    # modulo total by huge prime number to reduce hash size
    total %= 10888869450418352160768000001

    hashed_string = number_to_letters(total)  # converts big number to letters
    return (hashed_string, salt) if use_salt else hashed_string


def saltr(letters=True) -> str | int:
    """
    Generates a 7 character salt by default,
    only returning an integer in the millions
    if specified.

    Parameters:
        - letters : bool deciding if the salt
        will be characters or not: True == letters,
        False == integer

    Returns:
        - string or integer : salt

    A salt is used to increase complexity of a hash.
    Appending 7 random characters to the end of a
    string causes two copies of the same string to have
    entirely different hashes. Just make sure to store
    salts along with their hashes, as otherwise strings
    can no longer be matched to them.
    """

    from random import randint

    number = randint(1000000, 9999999)
    return number_to_letters(number) if letters else number


def number_to_letters(number: int) -> str:
    """
    Converts an integer to a string, with characters
    ranging from 'a' to 't'. Used to have a human
    readable hash.

    Parameters:
        - number : integer to be converted

    Returns:
        - string : number string converted to letters
    """

    letters = {
        "1": ["a", "k"],
        "2": ["b", "l"],
        "3": ["c", "m"],
        "4": ["d", "n"],
        "5": ["e", "o"],
        "6": ["f", "p"],
        "7": ["g", "q"],
        "8": ["h", "r"],
        "9": ["i", "s"],
        "0": ["j", "t"],
    }

    chars = []
    flip = 0
    for num in str(number):
        chars.append(letters[num][flip])
        flip = 1 - flip
    return "".join(chars)

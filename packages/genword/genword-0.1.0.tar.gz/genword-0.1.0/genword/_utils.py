def _generate_combinations_helper(characters: str, max_length: int):
    if max_length == 0:
        yield ''
    else:
        for char in characters:
            for combo in _generate_combinations_helper(
                characters, max_length - 1
            ):
                yield char + combo


def generate_combinations(characters: str, min_length: int, max_length: int):
    """
    Generate all possible combinations of words of the required length, from a string of characters.

    Args:
        characters: string of characters from which the combinations will be generated
        min_length: minimum amount of characters in each combination
        max_length: maximum number of characters in each combination

    Returns:
        Generator with all possible combinations of words of the required length.

    Examples:
        >>> for x in generate_combinations('ab', 2, 2):
        ...     print(x)
        ...
        aa
        ab
        ba
        bb
    """
    for length in range(min_length, max_length + 1):
        yield from _generate_combinations_helper(characters, length)

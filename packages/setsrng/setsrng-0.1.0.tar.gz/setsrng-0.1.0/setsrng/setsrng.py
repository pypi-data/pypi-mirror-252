import random

def rnGen(num, start=None, end=None):
    """
    Generate random integers based on the specified parameters.

    Parameters:
    - num: Number of random integers to generate.
    - start: Optional. Starting range for random integers (default is None).
    - end: Optional. Ending range for random integers (default is None).

    Returns:
    A list of random integers.
    """
    if start is not None and end is not None:
        if not (isinstance(start, int) and isinstance(end, int)):
            raise ValueError("Start and end must be integers.")
        if start > end:
            raise ValueError("Start must be less than or equal to end.")
        return [random.randint(start, end) for _ in range(num)]
    elif start is None and end is None:
        # Default range if not provided
        return [random.randint(0, 100) for _ in range(num)]
    else:
        raise ValueError("Both start and end must be provided or neither.")

# Example usage:
# random_numbers1 = rnGen(200)
# print("Random Integers (50):", random_numbers1)

# random_numbers2 = rnGen(30, start=1, end=50)
# print("Random Integers (1 to 50):", random_numbers2)

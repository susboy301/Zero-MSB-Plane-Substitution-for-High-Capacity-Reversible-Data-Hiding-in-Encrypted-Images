
def huffman_define(freqs):
    """
    Define a Huffman coding rule based on input frequencies.
    This function assigns predefined codes sorted by frequency ranks in reverse.

    Args:
        freqs (list or np.ndarray): Frequency list of 9 symbols.

    Returns:
        list: Huffman codes assigned according to frequencies.
    """
    code = [
        [0, 1],
        [1, 0],
        [0, 0, 1],
        [1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1]
    ]

    # Sort freqs and get sorting indices (ascending)
    indices_sorted = sorted(range(len(freqs)), key=lambda k: freqs[k])

    # Initialize Huffman rule list
    huffman_rule = [None] * 9

    # Assign code in reverse order according to sorted frequencies
    for i in range(9):
        idx = indices_sorted[i]
        huffman_rule[idx] = code[8 - i]

    return huffman_rule

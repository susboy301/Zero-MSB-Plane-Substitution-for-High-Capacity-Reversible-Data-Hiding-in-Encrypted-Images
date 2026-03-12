import numpy as np

def masked_positions(block_id, slack, key):
    rng = np.random.default_rng(block_id + key)
    return rng.permutation(slack)

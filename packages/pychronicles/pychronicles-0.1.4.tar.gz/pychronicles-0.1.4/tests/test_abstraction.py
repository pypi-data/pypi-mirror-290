    
from pychronicles import TimedSequence, Chronicle
import numpy as np
import pandas as pd

#################################
# Example of sequence
seq = [
    ("a", 1),
    ("c", 2),
    ("b", 3),
    ("a", 8),
    ("a", 10),
    ("b", 12),
    ("a", 15),
    ("c", 17),
    ("b", 20),
    ("c", 23),
    ("c", 25),
    ("b", 26),
    ("c", 28),
    ("b", 30),
]


##########################################################################
# Create a dataframe representing several sequences with complex events, 
# each sequence having its own id, and different columns
grpdf = pd.DataFrame(
    {
        "label": [e[0] for e in seq] * 3,
        "str_val": [e[0] * 2 for e in seq]
        * 3,  # illustration of another columns than "label"
        "num_val": np.random.randint(
            10, size=3 * len(seq)
        ),  # illustration of another columns than "label"
        "id": [1] * len(seq) + [2] * len(seq) + [3] * len(seq),
    },
    index=[int(np.floor(e[1] / 4)) for e in seq] * 3,
)

##########################################################################
# Abstraction example from the dataframe
# - label: name of the column with the events to use
# - id: name of the column corresponding to the sequence id
#
# warning: the dataframe must be indexed by time, and its dtype must be float

chro = grpdf.tpattern.abstract("label", "id")
print(chro)


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
    ("a", 41),
    ("c", 42),
    ("b", 43),
    ("a", 48),
    ("a", 50),
    ("b", 52),
    ("a", 55),
    ("c", 57),
    ("b", 60),
    ("c", 63),
    ("c", 65),
    ("b", 66),
    ("c", 68),
]

dates = np.array(
    [np.datetime64("1970-01-01") + np.timedelta64(e[1], "D") for e in seq],
    dtype="datetime64",
)
data = np.array([e[0] for e in seq])

ts = TimedSequence(dates, data)

c = Chronicle()
c.add_event(0, "a")
c.add_event(1, "b")
c.add_event(2, "c")
c.add_constraint(0, 1, (np.timedelta64(4, "D"), np.timedelta64(10, "D")))
#c.add_constraint(0, 2, (np.timedelta64(2, "D"), np.timedelta64(8, "D")))
c.add_constraint(1, 2, (np.timedelta64(3, "D"), np.timedelta64(13, "D")))


# projection of the timed sequences on the chronicles
ret = c.project( [ts, ts] )

# Build a dataframe from the returned dictionary
df = pd.DataFrame( ret )
print(df)
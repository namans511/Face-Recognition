import os

verbose = os.getenv("VERBOSE")
# print(verbose)
vprint = print if verbose=="TRUE" else lambda *a, **k: None


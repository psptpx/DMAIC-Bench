import os
import sys

BENCH_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BENCH_ROOT not in sys.path:
    sys.path.insert(0, BENCH_ROOT)
